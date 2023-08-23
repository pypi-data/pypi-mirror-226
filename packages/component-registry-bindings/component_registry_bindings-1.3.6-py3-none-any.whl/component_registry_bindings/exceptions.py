"""
component-registry-bindings exceptions
"""


class ComponentRegistryBindingsException(Exception):
    """Base component-registry-bindings exception"""


class OperationUnsupported(ComponentRegistryBindingsException):
    """Session operation is unsupported exception"""
