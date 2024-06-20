from typing import List

from project.clients.base_client import BaseClient
from project.clients.regular_client import RegularClient
from project.clients.vip_client import VIPClient
from project.waiters.base_waiter import BaseWaiter
from project.waiters.full_time_waiter import FullTimeWaiter
from project.waiters.half_time_waiter import HalfTimeWaiter


class SphereRestaurantApp:
    WAITERS_MAPPER = {
        "FullTimeWaiter": FullTimeWaiter,
        "HalfTimeWaiter": HalfTimeWaiter,
    }

    CLIENTS_MAPPER = {
        "RegularClient": RegularClient,
        "VIPClient": VIPClient,
    }

    def __init__(self):
        self.waiters: List[BaseWaiter] = []
        self.clients: List[BaseClient] = []

    def _find_client_by_name(self, name):
        client = [c for c in self.clients if c.name == name]
        return client[0] if client else None

    def _find_waiter_by_name(self, name):
        waiter = [w for w in self.waiters if w.name == name]
        return waiter[0] if waiter else None

    def hire_waiter(self, waiter_type: str, waiter_name: str, hours_worked: int):
        if waiter_type not in self.WAITERS_MAPPER:
            return f"{waiter_type} is not a recognized waiter type."

        waiter = self._find_waiter_by_name(waiter_name)

        if waiter in self.waiters:
            return f"{waiter_name} is already on the staff."

        new_waiter = self.WAITERS_MAPPER[waiter_type](waiter_name, hours_worked)
        self.waiters.append(new_waiter)
        return f"{waiter_name} is successfully hired as a {waiter_type}."

    def admit_client(self, client_type: str, client_name: str):
        if client_type not in self.CLIENTS_MAPPER:
            return f"{client_type} is not a recognized client type."

        client = self._find_client_by_name(client_name)

        if client in self.clients:
            return f"{client_name} is already a client."

        new_client = self.CLIENTS_MAPPER[client_type](client_name)
        self.clients.append(new_client)
        return f"{client_name} is successfully admitted as a {client_type}."

    def process_shifts(self, waiter_name: str):
        waiter = self._find_waiter_by_name(waiter_name)

        if waiter is None:
            return f"No waiter found with the name {waiter_name}."
        return waiter.report_shift()


    def process_client_order(self, client_name: str, order_amount: float):
        client = self._find_client_by_name(client_name)

        if client is None:
            return f"{client_name} is not a registered client."
        return f"{client_name} earned {client.earning_points(order_amount)} points from the order."

    def apply_discount_to_client(self, client_name: str):
        client = self._find_client_by_name(client_name)

        if client is None:
            return f"{client_name} cannot get a discount because this client is not admitted!"

        discount_percentage = client.apply_discount()[0]
        remaining_points = client.apply_discount()[1]
        return f"{client_name} received a {discount_percentage}% discount. Remaining points {remaining_points}"

    def generate_report(self):
        total_earnings = sum([w.calculate_earnings() for w in self.waiters])
        total_client_points = sum([c.points for c in self.clients])
        clients_count = len(self.clients)

        result = [f"""$$ Monthly Report $$
Total Earnings: ${total_earnings:.2f}
Total Clients Unused Points: {total_client_points}
Total Clients Count: {clients_count}
** Waiter Details **"""]

        waiters = [w for w in self.waiters]
        sorted_waiters = sorted(waiters, key=lambda waiter: -waiter.total_earning)
        result.append('\n'.join(str(w) for w in sorted_waiters))

        return '\n'.join(result)





