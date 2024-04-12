from project.trip import Trip
from unittest import TestCase, main

class TestTrip(TestCase):

    def setUp(self):
        self.trip = Trip(10_000, 3, True)

    def test_init_trip(self):
        self.assertEqual(10_000, self.trip.budget)
        self.assertEqual(3, self.trip.travelers)
        self.assertEqual(True, self.trip.is_family)
        self.assertEqual({}, self.trip.booked_destinations_paid_amounts)

    def test_if_travelers_less_than_one(self):
        with self.assertRaises(ValueError) as ex:
            self.trip.travelers = 0

        self.assertEqual('At least one traveler is required!', str(ex.exception))

    def test_if_travelers_are_more_than_two(self):
        self.trip.travelers = 2
        self.assertEqual(2, self.trip.travelers)

    def test_if_is_family_is_false_and_travelers_less_than_two_return_false(self):
        self.trip.travelers = 1
        self.trip.is_family = False
        self.assertEqual(False, self.trip.is_family)

    def test_if_is_family_is_true_and_travelers_less_than_two_return_false(self):
        self.trip.travelers = 1
        self.trip.is_family = True
        self.assertEqual(False, self.trip.is_family)

    def test_if_is_family_is_true_and_travelers_more_than_two_return_false(self):
        self.trip.travelers = 3
        self.trip.is_family = True
        self.assertEqual(True, self.trip.is_family)

    def test_book_trip_if_destination_is_not_in_offers(self):
        result = self.trip.book_a_trip("Thailand")
        self.assertEqual('This destination is not in our offers, please choose a new one!', result)

    def test_book_trip_correct_destination_without_enough_budget(self):
        self.trip.budget = 400
        result = self.trip.book_a_trip("Bulgaria")

        self.assertEqual('Your budget is not enough!', result)

    def test_book_trip_with_correct_destination_and_enough_budged_and_is_family_get_discount(self):
        message = self.trip.book_a_trip("Bulgaria")
        price = 450
        self.trip.is_family = True
        expected_price = self.trip.DESTINATION_PRICES_PER_PERSON["Bulgaria"] * 0.9

        self.assertEqual(expected_price, price)

        budget = self.trip.budget
        expected_budget = 8_650
        self.assertEqual(expected_budget, budget)
        self.assertEqual({"Bulgaria": 1350.0}, self.trip.booked_destinations_paid_amounts)
        self.assertEqual(f'Successfully booked destination Bulgaria! Your budget left is 8650.00', message)

    def test_booking_status_if_not_booked_destinations_paid_amounts_return_message(self):
        self.trip.booked_destinations_paid_amounts = {}

        self.assertEqual(f'No bookings yet. Budget: 10000.00', self.trip.booking_status())

    def test_booking_status_with_booked_destination_return_correct_message(self):
        self.trip.booked_destinations_paid_amounts = {"Bulgaria": 1350.0}

        message = """Booked Destination: Bulgaria
Paid Amount: 1350.00
Number of Travelers: 3
Budget Left: 10000.00"""

        self.assertEqual(message, self.trip.booking_status())
if __name__ == '__main__':
    main()
