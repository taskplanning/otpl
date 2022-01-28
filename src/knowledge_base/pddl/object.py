from pddl.domain_type import DomainType


class Object:
    """
    This class describes a typed object instance.
    """
    
    def __init__(self, name : str, type : str = "object") -> None:
        self.name = name
        self.type = type