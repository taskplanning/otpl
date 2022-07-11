class DomainType:
    
    def __init__(self, type_name : str, parent : str = "object") -> None:
        self.name : str = type_name
        self.parent : str = parent

    def __repr__(self) -> str:
        return self.name
