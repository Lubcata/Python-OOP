from abc import ABC, abstractmethod


class Vehicle(ABC):

    @abstractmethod
    def drive(self, distance):
        ...

    @abstractmethod
    def refuel(self, fuel):
        ...


class ConditionerOn:

    @staticmethod
    def car_conditioner():
        car_conditioner_on = 0.9
        return car_conditioner_on

    @staticmethod
    def truck_conditioner():
        truck_conditioner_on = 1.6
        return truck_conditioner_on


class Car(Vehicle, ConditionerOn):
    def __init__(self, fuel_quantity: int, fuel_consumption: int):
        self.fuel_quantity = fuel_quantity
        self.fuel_consumption = fuel_consumption

    def drive(self, distance):
        consumption = (ConditionerOn.car_conditioner() + self.fuel_consumption) * distance

        if self.fuel_quantity >= consumption:
            self.fuel_quantity -= consumption

    def refuel(self, fuel):
        self.fuel_quantity += fuel


class Truck(Vehicle, ConditionerOn):
    TANK_PERCENTAGE_FILL = 0.95

    def __init__(self, fuel_quantity: int, fuel_consumption: int):
        self.fuel_quantity = fuel_quantity
        self.fuel_consumption = fuel_consumption

    def drive(self, distance):
        consumption = (ConditionerOn.truck_conditioner() + self.fuel_consumption) * distance

        if self.fuel_quantity >= consumption:
            self.fuel_quantity -= consumption

    def refuel(self, fuel):
        self.fuel_quantity += fuel * Truck.TANK_PERCENTAGE_FILL


car = Car(20, 5)
car.drive(3)
print(car.fuel_quantity)
car.refuel(10)
print(car.fuel_quantity)

