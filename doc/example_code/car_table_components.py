
class RowCheckbox(PC):
    _find_from_parent = True
    _locator = (By.CSS_SELECTOR, "td:nth-of-type(1) input")
class RowMake(PC):
    _find_from_parent = True
    _locator = (By.CSS_SELECTOR, "td:nth-of-type(2)")
class RowModel(PC):
    _find_from_parent = True
    _locator = (By.CSS_SELECTOR, "td:nth-of-type(3)")
class RowYear(PC):
    _find_from_parent = True
    _locator = (By.CSS_SELECTOR, "td:nth-of-type(4)")
class RowColor(PC):
    _find_from_parent = True
    _locator = (By.CSS_SELECTOR, "td:nth-of-type(5)")

class CarItem(PC):
    _index = None
    _find_from_parent = True
    __locator = "tbody tr:nth-of-type({index})"

    checkbox = RowCheckbox()
    _make = RowMake()
    _model = RowModel()
    _year = RowYear()
    _color = RowColor()

    @property
    def _locator(self) -> tuple:
        return (By.CSS_SELECTOR, self.__locator.format(index=self._index + 1))

    def __init__(self, index: int, parent: PC):
        self._index = index
        self._parent = parent
        self.driver = self._parent.driver

    @property
    def id(self) -> int:
        return int(self.checkbox.get_attribute("value"))
    @property
    def make(self) -> CarMake:
        return CarMake[self._make.text.lower()]
    @property
    def model(self) -> CarModel:
        return CarModel[self._model.text.lower()]
    @property
    def year(self) -> int:
        return int(self._year.text)
    @property
    def color(self) -> Color:
        return  Color[self._color.text.lower()]

class DeleteButton(PC):
    _locator = (By.CSS_SELECTOR, "#delete-button")

class CarTable(PC):
    _locator = (By.CSS_SELECTOR, ".carTable")
    _item_locator = (By.CSS_SELECTOR, "tbody tr")

    delete_button = DeleteButton()

    @property
    def car_count(self) -> int:
        return len(self.find_elements(*self._item_locator))

    @property
    def car_items(self) -> List[CarItem]:
        return list(CarItem(i, self) for i in range(self.car_count))

    @property
    def cars(self) -> List[Car]:
        cars = []
        for car in self.car_items:
            cars.append(Car(car.make, car.model, car.year, car.color, car.id))
        return list(CarItem(i, self) for i in range(self.car_count))

    def remove_car(self, car: Car):
        self.car_items[self.car_items.index(car)].checkbox.click()
        self.delete_button.click()
