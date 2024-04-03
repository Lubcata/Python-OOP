from unittest import TestCase, main

from project.climbing_robot import ClimbingRobot


class TestClimbingRobot(TestCase):
    ALLOWED_CATEGORIES = ['Mountain', 'Alpine', 'Indoor', 'Bouldering']

    def setUp(self):
        self.robot = ClimbingRobot(
            "Mountain",
            "Helper",
            100,
            200,
        )

        self.robot_with_software = ClimbingRobot(
            "Mountain",
            "Helper",
            100,
            200,
        )

        self.robot_with_software.installed_software = [
            {"name": "PyCharm", "capacity_consumption": 50, "memory_consumption": 49},
            {"name": "CLion", "capacity_consumption": 49, "memory_consumption": 51}
        ]

    def test_init(self):
        self.assertEqual("Mountain", self.robot.category)
        self.assertEqual("type", self.robot.part_type)
        self.assertEqual(10, self.robot.capacity)
        self.assertEqual(10, self.robot.memory)

    def test_if_category_is_not_allowed_raise_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.robot.category = "Incorrect"

        self.assertEqual(f"Category should be one of {self.ALLOWED_CATEGORIES}", str(ve.exception))

    def test_get_capacity_return_correct_sum(self):
        expected_result = sum(s['capacity_consumption'] for s in self.robot_with_software.installed_software)
        result = self.robot_with_software.get_used_capacity()

        self.assertEqual(expected_result, result)

    def test_available_capacity_return_correct_result(self):
        expected_result = self.robot.capacity - self.robot.get_used_capacity()
        result = self.robot.get_available_capacity()

        self.assertEqual(expected_result, result)

    def test_install_software_if_available_capacity_is_more_or_equal_to_capacity_consumption_and_memory_consumption(
            self):
        result = self.robot.install_software(
            {"name": "PyCharm", "capacity_consumption": 100, "memory_consumption": 200},
        )

        self.assertEqual(
            f"Software 'PyCharm' successfully installed on Mountain part.",
            result
        )

        self.assertEqual(self.robot.installed_software,
                         [{"name": "PyCharm", "capacity_consumption": 100, "memory_consumption": 200}])

    def test_install_software_with_lower_capacity_and_enough_memory(self):
        result = self.robot.install_software(
            {"name": "PyCharm", "capacity_consumption": 50, "memory_consumption": 2000},
        )

        self.assertEqual(f"Software 'PyCharm' cannot be installed on Mountain part.", result)

        self.assertEqual(self.robot.installed_software, [])

    def test_install_software_with_both_capacity_and_memory_are_lower_than_needed(self):
        result = self.robot_with_software.install_software(
            {"name": "PyCharm", "capacity_consumption": 49, "memory_consumption": 50},
        )

        self.assertEqual(
            f"Software 'PyCharm' cannot be installed on Mountain part.",
            result
        )

        self.assertEqual(
            self.robot.installed_software,
            []
        )


if __name__ == "__main__":
    main()
