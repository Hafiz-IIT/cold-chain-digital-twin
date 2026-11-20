import unittest

from cold_chain_digital_twin import ColdChainState, simulate, step


class ColdChainTests(unittest.TestCase):
    def test_hot_ambient_warms_without_cooling(self):
        s = step(ColdChainState(4.0), ambient_c=30.0, cooling_c_per_hour=0.0)
        self.assertGreater(s.temperature_c, 4.0)

    def test_cooling_reduces_temperature(self):
        no = step(ColdChainState(8.0), ambient_c=20.0, cooling_c_per_hour=0.0)
        yes = step(ColdChainState(8.0), ambient_c=20.0, cooling_c_per_hour=4.0)
        self.assertLess(yes.temperature_c, no.temperature_c)

    def test_negative_timestep_and_cooling_are_rejected(self):
        with self.assertRaises(ValueError):
            step(ColdChainState(4.0), ambient_c=30.0, cooling_c_per_hour=0.0, dt_hours=-0.25)
        with self.assertRaises(ValueError):
            step(ColdChainState(4.0), ambient_c=30.0, cooling_c_per_hour=-1.0)

    def test_nonfinite_ambient_is_rejected(self):
        with self.assertRaises(ValueError):
            step(ColdChainState(4.0), ambient_c=float("nan"), cooling_c_per_hour=0.0)

    def test_excursion_is_tracked(self):
        result = simulate(4.0, [35.0] * 20, cooling_c_per_hour=0.0, max_allowed_c=8.0)
        self.assertGreater(result.excursion_hours, 0)


if __name__ == "__main__":
    unittest.main()
