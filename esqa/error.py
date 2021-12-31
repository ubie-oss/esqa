import dataclasses


@dataclasses.dataclass
class ValidationError:
    message: str
    name: str
