from typing import List

from project.route import Route
from project.user import User
from project.vehicles.base_vehicle import BaseVehicle
from project.vehicles.cargo_van import CargoVan
from project.vehicles.passenger_car import PassengerCar


class ManagingApp:
    VEHICLE_TYPE = {
        "CargoVan": CargoVan,
        "PassengerCar": PassengerCar,
    }
    def __init__(self):
        self.users: List[User] = []
        self.vehicles: List[BaseVehicle] = []
        self.routes: List[Route] = []

    def find_route_by_start_end(self, start, end):
        route = [r for r in self.routes if r.start_point == start and r.end_point == end]
        return route[0] if route else None

    def find_route_by_id(self, route_id):
        route = [r for r in self.routes if r.route_id == route_id]
        return route[0] if route else None

    def create_route(self, start_point: str, end_point: str, length: float):
        route_id = len(self.routes) + 1
        return Route(start_point, end_point, length, route_id)

    def create_vehicle(self, vehicle_type, brand: str, model: str, license_plate_number: str):
        return self.VEHICLE_TYPE[vehicle_type](brand, model, license_plate_number)

    @staticmethod
    def create_user(first_name: str, last_name: str, driving_license_number: str):
        return User(first_name, last_name, driving_license_number)

    def find_user_by_driving_license(self, driving_license):
        user = [u for u in self.users if u.driving_license_number == driving_license]
        return user[0] if user else None

    def find_vehicle_by_license_plate(self, license_plate):
        vehicle = [v for v in self.vehicles if v.license_plate_number == license_plate]
        return vehicle[0] if vehicle else None

    def register_user(self, first_name: str, last_name: str, driving_license_number: str):
        user = self.find_user_by_driving_license(driving_license_number)

        if user in self.users:
            return f"{driving_license_number} has already been registered to our platform."

        new_user = self.create_user(first_name, last_name, driving_license_number)

        self.users.append(new_user)
        return f"{first_name} {last_name} was successfully registered under DLN-{driving_license_number}"

    def upload_vehicle(self, vehicle_type: str, brand: str, model: str, license_plate_number: str):
        if vehicle_type not in self.VEHICLE_TYPE:
            return f"Vehicle type {vehicle_type} is inaccessible."

        vehicle = self.find_vehicle_by_license_plate(license_plate_number)

        if vehicle in self.vehicles:
            return f"{license_plate_number} belongs to another vehicle."

        new_vehicle = self.create_vehicle(vehicle_type, brand, model, license_plate_number)

        self.vehicles.append(new_vehicle)
        return f"{brand} {model} was successfully uploaded with LPN-{license_plate_number}."

    def allow_route(self, start_point: str, end_point: str, length: float):
        route = self.find_route_by_start_end(start_point, end_point)

        if route in self.routes:
            if route.length == length:
                return f"{start_point}/{end_point} - {length} km had already been added to our platform."
            if route.length < length:
                return f"{start_point}/{end_point} shorter route had already been added to our platform."
            if route.length > length:
                route.is_locked = True

        new_route = self.create_route(start_point, end_point, length)
        self.routes.append(new_route)
        return f"{start_point}/{end_point} - {length} km is unlocked and available to use."

    def make_trip(self, driving_license_number: str, license_plate_number: str, route_id: int,  is_accident_happened: bool):
        user = self.find_user_by_driving_license(driving_license_number)
        vehicle = self.find_vehicle_by_license_plate(license_plate_number)
        route = self.find_route_by_id(route_id)

        if user.is_blocked:
            return f"User {driving_license_number} is blocked in the platform! This trip is not allowed."

        if vehicle.is_damaged:
            return f"Vehicle {license_plate_number} is damaged! This trip is not allowed."

        if route.is_locked:
            return f"Route {route_id} is locked! This trip is not allowed."

        vehicle.drive(route.length)
        if is_accident_happened:
            vehicle.change_status()
            user.decrease_rating()
        else:
            user.increase_rating()
        return str(vehicle)

    def repair_vehicles(self, count: int):
        damaged_vehicles = [v for v in self.vehicles if v.is_damaged]
        selected_vehicles = sorted(damaged_vehicles, key=lambda vehicle: (vehicle.brand, vehicle.model))[:count]

        for vehicle in selected_vehicles:
            vehicle.is_damaged = False
            vehicle.battery_level = 100

        return f"{len(selected_vehicles)} vehicles were successfully repaired!"

    def users_report(self):
        result = ["*** E-Drive-Rent ***"]
        sorted_users = sorted(self.users, key=lambda user: -user.rating)
        result.append('\n'.join(str(u) for u in sorted_users))

        return '\n'.join(result)





