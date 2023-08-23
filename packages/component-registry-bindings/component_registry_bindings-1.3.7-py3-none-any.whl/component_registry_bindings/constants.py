"""
component-registry-bindings constants
"""

from typing import Dict, List

COMPONENT_REGISTRY_API_VERSION: str = "v1"
COMPONENT_REGISTRY_BINDINGS_VERSION: str = "1.3.7"
COMPONENT_REGISTRY_BINDINGS_USERAGENT: str = (
    f"component-registry-bindings-{COMPONENT_REGISTRY_BINDINGS_VERSION}"
)
COMPONENT_REGISTRY_BINDINGS_API_PATH: str = (
    f".bindings.python_client.api.{COMPONENT_REGISTRY_API_VERSION}"
)
COMPONENT_REGISTRY_BINDINGS_PLACEHOLDER_FIELD = (
    f'__placeholder_field{COMPONENT_REGISTRY_BINDINGS_VERSION.replace(".","")}'
)

# all available session operations
ALL_SESSION_OPERATIONS: List[str] = (
    "retrieve",
    "update",
    "list",
    "create",
    "destroy",
    "search",
)

# mapping for resources which model names are different from the endpoint name
RESOURCE_TO_MODEL_MAPPING: Dict[str, str] = {
    "builds": "SoftwareBuild",
}
