from functools import partial
from .namespace_resolver import NamespaceResolver

def namespaced(namespace: str):
    resolver = NamespaceResolver(namespace)

    return partial(namespaced_inst, namespace)

def namespaced_getattr(namespace: str):
    resolver = NamespaceResolver(namespace)
    
    def __getattr__(self, attr):
        return resolver.resolve(self, attr)

    return __getattr__

def namespaced_inst(namespace: str, attached_class):
    resolver = NamespaceResolver(namespace)

    attached_getattr = None
    if callable(getattr(attached_class, "__getattr__", None)):
        attached_getattr = attached_class.__getattr__

    def __getattr__(self, attr):
        if attached_getattr:
            attached_getattr(self, attr)
        return resolver.resolve(self, attr)

    attached_class.__getattr__ = __getattr__
    return attached_class