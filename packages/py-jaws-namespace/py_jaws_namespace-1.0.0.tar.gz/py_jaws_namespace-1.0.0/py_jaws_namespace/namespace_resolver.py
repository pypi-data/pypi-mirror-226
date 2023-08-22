import importlib
import logging
from py_jaws_namespace.namespace_registry import NamespaceRegistry

class NamespaceResolver:

    def __init__(self, namespace: str):
        self.__namespace = namespace
        self.__ctx = NamespaceRegistry.get_namespace_ctx(self.__namespace)

    def resolve(self, initiator, client: str):
        if self.__ctx is None or client not in self.__ctx:
            logging.error(f"Invalid client {client} or namespace {self.__namespace}")
            return None
        
        handler_obj = self.__resolve_import(self.__ctx[client])
        if handler_obj is not None:
            return handler_obj(initiator)

        return None

    def __resolve_import(self, module: str):
        (module_path, handler_name) = module.split(":")

        try:
            module = importlib.import_module(module_path)
            
            if hasattr(module, handler_name):
                return getattr(module, handler_name)
            else:
                logging.error(f"Handler '{handler_name}' not found in module '{module_path}'")
        except ImportError:
            logging.error(f"Module '{module_path}' not found")

        return None