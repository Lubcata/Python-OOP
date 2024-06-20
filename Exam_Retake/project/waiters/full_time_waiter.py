from project.waiters.base_waiter import BaseWaiter


class FullTimeWaiter(BaseWaiter):

    def calculate_earnings(self):
        result = self.hours_worked * 15.0
        self.total_earning += result
        return result

    def report_shift(self):
        return f"{self.name} worked a full-time shift of {self.hours_worked} hours."