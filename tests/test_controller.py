import unittest

from controller import simulate_controlled, thermostat_cooling


class ControllerTests(unittest.TestCase):
    def test_thermostat_turns_on_above_deadband(self):
        self.assertEqual(
            thermostat_cooling(7.0, target_c=4.0, max_cooling_c_per_hour=3.0),
            3.0,
        )

    def test_thermostat_stays_off_near_target(self):
        self.assertEqual(
            thermostat_cooling(4.2, target_c=4.0, max_cooling_c_per_hour=3.0),
            0.0,
        )

    def test_control_reduces_hot_ambient_excursion(self):
        no_control = simulate_controlled(
            4.0, [35.0] * 40,
            target_c=4.0, max_allowed_c=8.0, max_cooling_c_per_hour=0.0,
        )
        controlled = simulate_controlled(
            4.0, [35.0] * 40,
            target_c=4.0, max_allowed_c=8.0, max_cooling_c_per_hour=5.0,
        )
        self.assertLessEqual(controlled.excursion_hours, no_control.excursion_hours)
        self.assertGreater(controlled.cooling_energy_proxy, 0.0)


if __name__ == "__main__":
    unittest.main()
