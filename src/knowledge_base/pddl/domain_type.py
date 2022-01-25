class DomainType:
    """
    This class describes a type in the domain with its parent type.
    """

    _root_type = None

    def __init__(self, type_name : str, parent : str = "object") -> None:
        self.name : str = type_name

    def __repr__(self) -> str:
        return self.name

    def get_root_type():
        if DomainType._root_type is None: root_type = DomainType(name="object", parent=None)
        return DomainType._root_type