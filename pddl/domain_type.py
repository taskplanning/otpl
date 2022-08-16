class DomainType:
    
    def __init__(self, type_name : str, parent : str = "object") -> None:
        self.name : str = type_name
        self.parent : str = parent

    def __repr__(self) -> str:
        return self.name

    def visit(self, visit_function : callable, valid_types : tuple[type] = None, args=(), kwargs={}):
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)
