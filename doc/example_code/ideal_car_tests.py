@pytest.fixture(scope="class", autouse=True)
def page(driver, url):
    driver.get(url)
    return CarTablePage(driver)

@pytest.fixture(scope="class")
def car():
    return Car(CarMake.CHEVROLET, ChevroletModel.IMPALA, 1995, Color.RED)

class TestTableIsEmptyOnLoad:
    def test_table_has_no_entries(self, page):
        assert len(page.cars) == 0

class TestCarIsAdded:
    @pytest.fixture(scope="class", autouse=True)
    def add_car(self, car, page):
        page.add_car(car)

    def test_car_is_in_table(self, page, car):
        assert car in page.cars

class TestCarIsRemoved:
    @pytest.fixture(scope="class", autouse=True)
    def add_car(self, car, page):
        page.add_car(car)

    @pytest.fixture(scope="class", autouse=True)
    def remove_car(self, car, page):
        page.remove_car(car)

    def test_car_is_not_in_table(self, page, car):
        assert car not in page.cars
