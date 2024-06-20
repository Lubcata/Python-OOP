from unittest import TestCase, main

from project.restaurant import Restaurant


class TestRestaurant(TestCase):
    def setUp(self):
        self.restaurant = Restaurant("Lubo", 100)

    def test_init_correct(self):
        self.assertEqual("Lubo", self.restaurant.name)
        self.assertEqual(100, self.restaurant.capacity)
        self.assertEqual([], self.restaurant.waiters)

    def test_name_is_empty(self):
        with self.assertRaises(ValueError) as ex:
            self.restaurant.name = ""

        self.assertEqual("Invalid name!", str(ex.exception))

    def test_name_is_correct(self):
        self.restaurant.name = "Hello"
        self.assertEqual("Hello", self.restaurant.name)

    def test_capacity_is_less_than_zero(self):
        with self.assertRaises(ValueError) as ex:
            self.restaurant.capacity = -1

        self.assertEqual("Invalid capacity!", str(ex.exception))

    def test_capacity_is_correct(self):
        self.restaurant.capacity = 0
        self.assertEqual(0, self.restaurant.capacity)

    def test_get_waiters_is_empty(self):
        self.restaurant.waiters = []
        result = self.restaurant.get_waiters(1, 2)

        self.assertEqual([], result)

    def test_get_waiters(self):
        self.restaurant.waiters = [{"name": "Lubo",'total_earnings': 1}, {"name": "Liza", 'total_earnings': 2}, {"name": "Gosho", 'total_earnings': 3}]
        result = self.restaurant.get_waiters(1, 2)
        expected_result = [{'name': 'Lubo', 'total_earnings': 1}, {'name': 'Liza', 'total_earnings': 2}]
        self.assertEqual(expected_result, result)

    def test_add_waiter_if_no_more_capacity(self):
        self.restaurant.capacity = 0
        result = self.restaurant.add_waiter("Lubo")

        self.assertEqual("No more places!", result)

    def test_add_waiter_if_waiter_already_exist(self):
        self.restaurant.waiters = [{"name": "Lubo",'total_earnings': 1}, {"name": "Liza", 'total_earnings': 2}, {"name": "Gosho", 'total_earnings': 3}]

        result = self.restaurant.add_waiter("Lubo")

        self.assertEqual(f"The waiter Lubo already exists!", result)

    def test_add_waiter(self):
        self.restaurant.waiters = []

        result = self.restaurant.add_waiter("Lubo")
        message = f"The waiter Lubo has been added."

        self.assertEqual(message, result)
        self.assertEqual([{"name": "Lubo"}], self.restaurant.waiters)

    def test_remove_waiter_if_waiter_name_is_not_in_collection(self):
        self.restaurant.waiters = []
        result = self.restaurant.remove_waiter("Lubo")
        message = f"No waiter found with the name Lubo."

        self.assertEqual(message, result)

    def test_remove_waiter_if_waiter_is_in_collection(self):
        self.restaurant.waiters = [{"name": "Lubo", 'total_earnings': 1},
                                   {"name": "Liza", 'total_earnings': 2},
                                   {"name": "Gosho", 'total_earnings': 3}]

        new_waiter_collection = [{"name": "Liza", 'total_earnings': 2},
                                   {"name": "Gosho", 'total_earnings': 3}]
        result = self.restaurant.remove_waiter("Lubo")
        message = f"The waiter Lubo has been removed."

        self.assertEqual(message, result)
        self.assertEqual(new_waiter_collection, self.restaurant.waiters)

    def test_get_total_earnings_if_no_total_earnings(self):
        self.restaurant.waiters = [{"name": "Lubo"},
                                   {"name": "Liza"},
                                   {"name": "Gosho"}]

        expected_collection = [{"name": "Lubo"},
                            {"name": "Liza"},
                            {"name": "Gosho"}]
        result = self.restaurant.get_total_earnings()
        self.assertEqual(0, result)
        self.assertEqual(expected_collection, self.restaurant.waiters)

    def test_get_total_earnings_return_correct_sum(self):
        self.restaurant.waiters = [{"name": "Lubo", 'total_earnings': 1},
                                   {"name": "Liza", 'total_earnings': 2},
                                   {"name": "Gosho", 'total_earnings': 3}]
        result = self.restaurant.get_total_earnings()
        self.assertEqual(6, result)


if __name__ == "__main__":
    main()