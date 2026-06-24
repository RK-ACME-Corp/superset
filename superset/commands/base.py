# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, ClassVar, Optional, TYPE_CHECKING

from flask_appbuilder.security.sqla.models import User

from superset.commands.utils import compute_owner_list, populate_owner_list
from superset.utils.decorators import on_error, transaction

if TYPE_CHECKING:
    from superset.commands.exceptions import CommandException
    from superset.daos.base import BaseDAO


class BaseCommand(ABC):
    """
    Base class for all Command like Superset Logic objects
    """

    @abstractmethod
    def run(self) -> Any:
        """
        Run executes the command. Can raise command exceptions
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate is normally called by run to validate data.
        Will raise exception if validation fails
        :raises: CommandException
        """


class BaseBulkDeleteCommand(BaseCommand):
    """
    Base class for bulk delete commands that follow the common pattern of:
    1. Accept a list of model IDs
    2. Validate models exist via DAO.find_by_ids
    3. Run optional additional validation (ownership, integrity, etc.)
    4. Delete via DAO.delete

    Subclasses must define ``dao_class``, ``not_found_error``, and
    ``delete_failed_error`` as class attributes. Override
    ``validate_additional`` for extra validation logic.
    """

    dao_class: ClassVar[type["BaseDAO[Any]"]]
    not_found_error: ClassVar[type["CommandException"]]
    delete_failed_error: ClassVar[type["CommandException"]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "delete_failed_error") and "run" not in cls.__dict__:
            cls.run = transaction(  # type: ignore[method-assign]
                on_error=partial(on_error, reraise=cls.delete_failed_error)
            )(BaseBulkDeleteCommand._run_delete)

    def __init__(self, model_ids: list[int]) -> None:
        self._model_ids = model_ids
        self._models: list[Any] = []

    def _run_delete(self) -> None:
        self.validate()
        self.dao_class.delete(self._models)

    def run(self) -> None:
        self._run_delete()

    def validate(self) -> None:
        self._models = self.dao_class.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise self.not_found_error()
        self.validate_additional()

    def validate_additional(self) -> None:
        """Override in subclasses for additional validation."""

    def check_ownership(self, forbidden_error: type["CommandException"]) -> None:
        """Check ownership of all models, raising the given error on failure."""
        from superset import security_manager
        from superset.exceptions import SupersetSecurityException

        for model in self._models:
            try:
                security_manager.raise_for_ownership(model)
            except SupersetSecurityException as ex:
                raise forbidden_error() from ex


class CreateMixin:  # pylint: disable=too-few-public-methods
    @staticmethod
    def populate_owners(owner_ids: Optional[list[int]] = None) -> list[User]:
        """
        Populate list of owners, defaulting to the current user if `owner_ids` is
        undefined or empty. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owner_list(owner_ids, default_to_user=True)


class UpdateMixin:
    @staticmethod
    def populate_owners(owner_ids: Optional[list[int]] = None) -> list[User]:
        """
        Populate list of owners. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owner_list(owner_ids, default_to_user=False)

    @staticmethod
    def compute_owners(
        current_owners: Optional[list[User]],
        new_owners: Optional[list[int]],
    ) -> list[User]:
        """
        Handle list of owners for update events.

        :param current_owners: list of current owners
        :param new_owners: list of new owners specified in the update payload
        :returns: Final list of owners
        """
        return compute_owner_list(current_owners, new_owners)
