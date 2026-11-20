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

    def test_controlled_excursion_interpolates_threshold_crossing(self):
        result = simulate_controlled(
            7.0, [40.0],
            target_c=100.0, max_allowed_c=8.0,
            max_cooling_c_per_hour=0.0, dt_hours=1.0,
        )
        self.assertGreater(result.excursion_hours, 0.0)
        self.assertLess(result.excursion_hours, 1.0)

    def test_controlled_simulation_preserves_sub_microhour_excursion(self):
        result = simulate_controlled(
            7.0, [40.0], target_c=100.0, max_allowed_c=7.0000001,
            max_cooling_c_per_hour=0.0, dt_hours=1e-7,
        )
        self.assertGreater(result.excursion_hours, 0.0)
        self.assertLess(result.excursion_hours, 1e-7)

    def test_invalid_thermostat_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            thermostat_cooling(4.0, target_c=4.0, max_cooling_c_per_hour=3.0, deadband_c=-1.0)
        with self.assertRaises(ValueError):
            simulate_controlled(
                4.0, [30.0], target_c=4.0, max_allowed_c=8.0,
                max_cooling_c_per_hour=3.0, dt_hours=0.0,
            )


if __name__ == "__main__":
    unittest.main()
