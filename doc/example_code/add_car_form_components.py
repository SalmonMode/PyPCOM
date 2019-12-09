class SelectComponent(PC):
    @property
    def _el(self) -> Select:
        el = self._reference_node.find_element(*self._locator)
        return Select(el)
    def __set__(self, instance, value: Any):
        self.driver = instance.driver
        self._parent = instance
        self._select(value)

class MakeSelect(SelectComponent):
    _locator = (By.CSS_SELECTOR, "[name=make]")
    def _select(self, value: CarMake):
        self.select_by_value(value)

class ModelSelect(SelectComponent):
    _locator = (By.CSS_SELECTOR, "[name=model]")
    def _select(self, value: CarModel):
        self.select_by_value(value)

class YearInput(PC):
    _locator = (By.CSS_SELECTOR, "[name=year]")

class ColorSelect(SelectComponent):
    _locator = (By.CSS_SELECTOR, "[name=color]")
    def _select(self, value: Color):
        self.select_by_value(value)

class AddCarButton(PC):
    _locator = (By.CSS_SELECTOR, "#add-button")

def count_greater_than(
    component: PC,
    count: int,
    **kwargs: dict
) -> Callable[[RemoteWebDriver], bool]:
    """Given a number, checks that the car message count in the list is greater."""
    def callable(driver: RemoteWebDriver) -> bool:
        return len(component._parent.cars) > count
    return callable

class AddCarForm(PC):
    _locator = (By.CSS_SELECTOR, "#add-car-form")

    make = MakeSelect()
    model = ModelSelect()
    year = YearInput()
    color = ColorInput()
    add_car_button = AddCarButton()

    _expected_conditions = {
        "count_greater_than": count_greater_than,
    }

    def add_car(self, car: Car):
        current_car_count = len(self._parent.cars)
        self.make = car.make
        self.model = car.model
        self.year = car.year
        self.color = car.color
        self.add_car_button.click()
        self.wait_until("count_greater_than", count=current_car_count)

