import unittest

from cold_chain_digital_twin import ColdChainState, simulate, step, threshold_excursion_hours


class ColdChainTests(unittest.TestCase):
    def test_hot_ambient_warms_without_cooling(self):
        s = step(ColdChainState(4.0), ambient_c=30.0, cooling_c_per_hour=0.0)
        self.assertGreater(s.temperature_c, 4.0)

    def test_cooling_reduces_temperature(self):
        no = step(ColdChainState(8.0), ambient_c=20.0, cooling_c_per_hour=0.0)
        yes = step(ColdChainState(8.0), ambient_c=20.0, cooling_c_per_hour=4.0)
        self.assertLess(yes.temperature_c, no.temperature_c)

    def test_excursion_is_tracked(self):
        result = simulate(4.0, [35.0] * 20, cooling_c_per_hour=0.0, max_allowed_c=8.0)
        self.assertGreater(result.excursion_hours, 0)

    def test_threshold_crossing_is_interpolated_within_step(self):
        result = simulate(
            7.0, [40.0], cooling_c_per_hour=0.0,
            max_allowed_c=8.0, dt_hours=1.0,
        )
        self.assertGreater(result.excursion_hours, 0.0)
        self.assertLess(result.excursion_hours, 1.0)

    def test_extreme_threshold_crossing_is_interpolated_without_overflow(self):
        self.assertAlmostEqual(
            threshold_excursion_hours(-1e308, 1e308, 0.0, 1.0), 0.5
        )

    def test_sub_microhour_excursion_is_not_rounded_to_zero(self):
        result = simulate(
            7.0, [40.0], cooling_c_per_hour=0.0,
            max_allowed_c=7.0000001, dt_hours=1e-7,
        )
        self.assertGreater(result.excursion_hours, 0.0)
        self.assertLess(result.excursion_hours, 1e-7)

    def test_unrepresentably_large_integer_and_unstable_euler_step_rejected(self):
        with self.assertRaises(ValueError):
            ColdChainState(10 ** 10000)
        with self.assertRaises(ValueError):
            step(
                ColdChainState(4.0), ambient_c=30.0, cooling_c_per_hour=0.0,
                thermal_rate=2.0, dt_hours=1.0,
            )

    def test_invalid_thermal_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            step(ColdChainState(4), ambient_c=30, cooling_c_per_hour=-1)
        with self.assertRaises(ValueError):
            step(ColdChainState(4), ambient_c=30, cooling_c_per_hour=0, dt_hours=0)
        with self.assertRaises(ValueError):
            simulate(4, [float("nan")], cooling_c_per_hour=0, max_allowed_c=8)
        with self.assertRaises(ValueError):
            simulate(4, [], cooling_c_per_hour=0, max_allowed_c=8, dt_hours=0)


if __name__ == "__main__":
    unittest.main()
