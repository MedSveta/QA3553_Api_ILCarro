from dataclasses import dataclass

@dataclass
class CarDTO:
    serialNumber: str
    manufacture: str
    model: str
    year: str
    fuel: str
    seats: int
    carClass: str
    pricePerDay: float
    about: str
    city: str

