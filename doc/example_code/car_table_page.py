class CarTablePage(Page):
    add_car_form = AddCarForm()
    car_table = CarTable()

    def add_car(self, car: Car):
        self.add_car_form.add_car(car)

    def remove_car(self, car: Car):
        self.car_table.remove_car(car)

    @property
    def cars(self) -> List[Car]:
        return self.car_table.cars
