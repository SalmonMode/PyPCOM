class CarMake(Enum):
    @property
    def description(self):
        return self.value.title()

    CHEVROLET = "chevrolet"
    TOYOTA = "toyota"
    FORD = "ford"

class CarModel(Enum):
    @property
    def description(self):
        return self.value.title()

class ChevroletModel(CarModel):
    MALIBU = "malibu"
    IMPALA = "impala"

class ToyotaModel(CarModel):
    COROLA = "corola"
    PRIUS = "prius"

class FordModel(CarModel):
    FIESTA = "fiesta"
    FOCUS = "focus"

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

class Car:

    def __init__(
        self,
        make: CarMake,
        model: CarModel,
        year: int,
        color: Color,
        id: int = None,
    ):
        self._id = id
        self.make = make
        self.model = model
        self.year = year
        self.color = color

    def __eq__(self, other):
        if all(self._id is not None, other._id is not None):
            return self._id == other._id
        return all(
            self.make == other.make,
            self.model == other.model,
            self.year == other.year,
            self.color == other.color,
        )
