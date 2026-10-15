from dataclasses import dataclass

@dataclass
class UserDTO:
    username: str
    password: str
    firstName: str = "Sveta"
    lastName: str = "QA"