"""
component-registry-bindings session
"""

import asyncio
import importlib
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Union

import aiohttp

from .bindings.python_client import AuthenticatedClient, models
from .bindings.python_client.types import UNSET
from .constants import (
    ALL_SESSION_OPERATIONS,
    COMPONENT_REGISTRY_API_VERSION,
    COMPONENT_REGISTRY_BINDINGS_API_PATH,
    COMPONENT_REGISTRY_BINDINGS_PLACEHOLDER_FIELD,
    COMPONENT_REGISTRY_BINDINGS_USERAGENT,
    RESOURCE_TO_MODEL_MAPPING,
)
from .exceptions import OperationUnsupported
from .helpers import get_env
from .iterators import Paginator

component_registry_status_retrieve = importlib.import_module(
    f"{COMPONENT_REGISTRY_BINDINGS_API_PATH}.{COMPONENT_REGISTRY_API_VERSION}_status_list",
    package="component_registry_bindings",
)

MAX_CONCURRENCY = get_env(
    "COMPONENT_REGISTRY_BINDINGS_MAX_CONCURRENCY", "10", is_int=True
)


def get_sync_function(api_module: ModuleType) -> Callable:
    """
    Get 'sync' function from API module if available (response example is defined in schema)
    or get basic 'sync_detailed' function (response example is not defined in schema)
    """
    return getattr(api_module, "sync", getattr(api_module, "sync_detailed"))


def get_async_function(api_module: ModuleType) -> Callable:
    """
    Get 'sync' function from API module if available (response example is defined in schema)
    or get basic 'sync_detailed' function (response example is not defined in schema)
    """
    return getattr(api_module, "async_", getattr(api_module, "async_detailed"))


def new_session(
    component_registry_server_uri: str, verify_ssl: Union[str, bool] = True
):
    """Create a new session for selected Component Registry URI"""

    return Session(
        base_url=component_registry_server_uri.strip("/"), verify_ssl=verify_ssl
    )


class Session:
    """Simple session wrapper which encapsulates the client"""

    def __init__(self, base_url: str, verify_ssl: Union[str, bool] = True):

        self.__client = AuthenticatedClient(
            base_url=base_url,
            headers={"User-Agent": COMPONENT_REGISTRY_BINDINGS_USERAGENT},
            verify_ssl=verify_ssl,
        )

        self.builds = SessionOperationsGroup(
            self.__client,
            "builds",
            allowed_operations=("retrieve", "list"),
        )
        self.components = SessionOperationsGroup(
            self.__client,
            "components",
            allowed_operations=("retrieve", "list"),
        )
        self.products = SessionOperationsGroup(
            self.__client,
            "products",
            allowed_operations=("retrieve", "list"),
        )
        self.product_versions = SessionOperationsGroup(
            self.__client,
            "product_versions",
            allowed_operations=("retrieve", "list"),
        )
        self.product_streams = SessionOperationsGroup(
            self.__client,
            "product_streams",
            allowed_operations=("retrieve", "list"),
        )
        self.product_variants = SessionOperationsGroup(
            self.__client,
            "product_variants",
            allowed_operations=("retrieve", "list"),
        )
        self.channels = SessionOperationsGroup(
            self.__client, "channels", allowed_operations=("retrieve", "list")
        )

    def status(self):
        status_fn = get_sync_function(component_registry_status_retrieve)
        return status_fn(client=self.__client)


class SessionOperationsGroup:
    """
    Group of the CRUD and extra operations for one specific resource
    """

    def __init__(
        self,
        client: AuthenticatedClient,
        resource_name: str,
        allowed_operations: List[str] = ALL_SESSION_OPERATIONS,
    ):
        self.client = client
        self.resource_name = resource_name
        self.allowed_operations = allowed_operations

    @property
    def model_name(self) -> str:
        if self.resource_name in RESOURCE_TO_MODEL_MAPPING:
            # from mapping
            return RESOURCE_TO_MODEL_MAPPING[self.resource_name]
        else:
            # parse it from the resource name
            name_components = self.resource_name.split("_")
            name_components[-1] = name_components[-1][:-1]
            return "".join(name_component.title() for name_component in name_components)

    @property
    def model(self):
        return getattr(models, self.model_name)

    def __raise_operation_unsupported(self, operation_name: str):
        """Operation unsupported exception shortcut"""

        raise OperationUnsupported(
            f'Operation "{operation_name}" is not supported for the '
            f'"{self.resource_name}" resource.'
        )

    def __get_method_module(self, resource_name: str, method: str) -> ModuleType:
        # import endpoint module based on a method
        return importlib.import_module(
            f"{COMPONENT_REGISTRY_BINDINGS_API_PATH}.{COMPONENT_REGISTRY_API_VERSION}_{resource_name}_{method}",
            package="component_registry_bindings",
        )

    # CRUD operations

    def retrieve(self, id, **kwargs):
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            self.__raise_operation_unsupported("retrieve")

    def retrieve_list(self, *args, **kwargs):
        if "list" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            sync_fn = get_sync_function(method_module)
            response = sync_fn(*args, client=self.client, **kwargs)
            return Paginator.make_response_iterable(
                response, self.retrieve_list, *args, **kwargs
            )
        else:
            self.__raise_operation_unsupported("retrieve_list")

    def create(self, form_data: Dict[str, Any]):
        if "create" in self.allowed_operations:
            transformed_data = self.model.from_dict(form_data)

            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="create"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                client=self.client,
                form_data=transformed_data,
                multipart_data=UNSET,
                json_body=UNSET,
            )
        else:
            self.__raise_operation_unsupported("create")

    def update(self, id, form_data: Dict[str, Any]):
        if "update" in self.allowed_operations:
            transformed_data = self.model.from_dict(form_data)

            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="update"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                id,
                client=self.client,
                form_data=transformed_data,
                multipart_data=UNSET,
                json_body=UNSET,
            )
        else:
            self.__raise_operation_unsupported("update")

    def delete(self, id):
        if "destroy" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="destroy"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(
                id,
                client=self.client,
            )
        else:
            self.__raise_operation_unsupported("delete")

    # Extra operations

    def count(self, *args, **kwargs):
        if "list" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            sync_fn = get_sync_function(method_module)
            kwargs.pop("offset", None)
            kwargs["limit"] = 1
            kwargs["include_fields"] = COMPONENT_REGISTRY_BINDINGS_PLACEHOLDER_FIELD

            response = sync_fn(*args, client=self.client, **kwargs)
            return response.count
        else:
            self.__raise_operation_unsupported("retrieve_list")

    def search(self, searched_text: str):
        if "search" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(client=self.client, search=searched_text)
        else:
            self.__raise_operation_unsupported("search")

    def retrieve_list_iterator(self, *args, **kwargs):
        if "list" in self.allowed_operations:
            paginator = Paginator(
                *args,
                retrieve_list_fn=self.retrieve_list,
                **kwargs,
            )

            for page in paginator:
                for resource in page.results:
                    yield resource
        else:
            self.__raise_operation_unsupported("retrieve_list")

    def retrieve_list_iterator_async(
        self, *args, max_results: Optional[int] = None, **kwargs
    ):
        if "list" in self.allowed_operations:
            for page in asyncio.run(
                self.__retrieve_list_async(*args, max_results=max_results, **kwargs)
            ):
                for resource in page.results:
                    yield resource
        else:
            self.__raise_operation_unsupported("retrieve_list")

    async def __retrieve_list_async(
        self, *args, max_results: Optional[int] = None, **kwargs
    ):
        if "list" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="list"
            )
            async_fn = get_async_function(method_module)

            kwargs.pop("offset", None)
            limit = kwargs.pop("limit", 50)
            results_count = max_results or self.count(*args, **kwargs)

            connector = aiohttp.TCPConnector(limit=MAX_CONCURRENCY)
            async with aiohttp.ClientSession(connector=connector) as async_session:
                client = self.client.with_async_session(async_session)
                tasks = [
                    async_fn(*args, limit=limit, offset=offset, client=client, **kwargs)
                    for offset in range(0, results_count, limit)
                ]
                results = await asyncio.gather(*tasks)

            return results
        else:
            self.__raise_operation_unsupported("retrieve_list")

    def retrieve_provides(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve_provides" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="provides_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            self.__raise_operation_unsupported("retrieve_provides")

    def retrieve_taxonomy(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="taxonomy_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            self.__raise_operation_unsupported("retrieve_taxonomy")

    def retrieve_manifest(self, id, **kwargs):
        # TODO: Once the schema in Component Registry is adjusted, allow this for the
        # particular resources
        if "retrieve" in self.allowed_operations:
            method_module = self.__get_method_module(
                resource_name=self.resource_name, method="manifest_retrieve"
            )
            sync_fn = get_sync_function(method_module)
            return sync_fn(id, client=self.client, **kwargs)
        else:
            self.__raise_operation_unsupported("retrieve_manifest")
