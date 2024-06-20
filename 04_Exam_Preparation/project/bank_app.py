from typing import List

from project.clients.adult import Adult
from project.clients.base_client import BaseClient
from project.clients.student import Student
from project.loans.base_loan import BaseLoan
from project.loans.mortgage_loan import MortgageLoan
from project.loans.student_loan import StudentLoan


class BankApp:
    loans_mapper = {
        "StudentLoan": StudentLoan,
        "MortgageLoan": MortgageLoan,
    }

    clients_mapper = {
        "Student": Student,
        "Adult": Adult,
    }

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.loans: List[BaseLoan] = []
        self.clients: List[BaseClient] = []

    def find_client_by_id(self,client_id):
        client = [c for c in self.clients if client_id == c.client_id]
        return client[0] if client else None

    def find_loan_by_type(self, loan_type):
        loan = [l for l in self.loans if loan_type == l.__class__.__name__]
        return loan[0] if loan else None


    def add_loan(self, loan_type: str):
        if loan_type not in self.loans_mapper:
            raise Exception("Invalid loan type!")
        new_loan = self.loans_mapper[loan_type]()
        self.loans.append(new_loan)
        return f"{loan_type} was successfully added."
    def add_client(self, client_type: str, client_name: str, client_id: str, income: float):
        if client_type not in self.clients_mapper:
            raise Exception("Invalid client type!")
        if len(self.clients) >= self.capacity:
            return "Not enough bank capacity."

        new_client = self.clients_mapper[client_type](client_name, client_id, income)
        self.clients.append(new_client)
        return f"{client_type} was successfully added."

    def grant_loan(self, loan_type: str, client_id: str):
        loan = self.find_loan_by_type(loan_type)
        client = self.find_client_by_id(client_id)

        if loan_type != client.POSSIBLE_LOAN_TYPE:
            raise Exception("Inappropriate loan type!")

        self.loans.remove(loan)
        client.loans.append(loan)
        return f"Successfully granted {loan_type} to {client.name} with ID {client_id}."

    def remove_client(self, client_id: str):
        client = self.find_client_by_id(client_id)

        if client == None:
            raise Exception("No such client!")

        if client.loans:
            raise Exception("The client has loans! Removal is impossible!")

        self.clients.remove(client)
        return f"Successfully removed {client.name} with ID {client_id}."

    def increase_loan_interest(self, loan_type: str):
        loans = [l.increase_interest_rate() for l in self.loans if l.__class__.__name__ == loan_type]
        return f"Successfully changed {len(loans)} loans."

    def increase_clients_interest(self, min_rate: float):
        clients = [c.increase_clients_interest() for c in self.clients if c.interest < min_rate]
        return f"Number of clients affected: {len(clients)}."

    def get_statistics(self):
        clients_income = sum([c.income for c in self.clients])
        loans_count_granted_to_clients = sum([len(c.loans) for c in self.clients])
        granted_sum = sum([sum([l.amount for l in c.loans]) for c in self.clients])
        not_granted_sum = sum([l.amount for l in self.loans])
        avg_client_rate = sum([client.interest for client in self.clients]) / len(self.clients) if self.clients else 0

        return f"""Active Clients: {len(self.clients)}
Total Income: {clients_income:.2f}
Granted Loans: {loans_count_granted_to_clients}, Total Sum: {granted_sum:.2f}
Available Loans: {len(self.loans)}, Total Sum: {not_granted_sum:.2f}
Average Client Interest Rate: {avg_client_rate:.2f}
"""







