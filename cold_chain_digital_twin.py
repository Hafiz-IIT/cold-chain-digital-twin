from __future__ import annotations

from dataclasses import dataclass
import math


def _finite_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, TypeError, ValueError):
        return False


def threshold_excursion_hours(previous_c: float, current_c: float, threshold_c: float, dt_hours: float) -> float:
    """Linearly interpolate the time above a threshold during one simulation step."""
    if not all(_finite_number(value) for value in (previous_c, current_c, threshold_c, dt_hours)):
        raise ValueError("excursion inputs must be finite numbers")
    if dt_hours <= 0:
        raise ValueError("dt_hours must be positive")
    if previous_c > threshold_c and current_c > threshold_c:
        return dt_hours
    scale = max(abs(previous_c), abs(current_c), abs(threshold_c))
    if scale == 0:
        return 0.0
    previous_scaled = previous_c / scale
    current_scaled = current_c / scale
    threshold_scaled = threshold_c / scale
    if previous_scaled <= threshold_scaled < current_scaled:
        fraction = (current_scaled - threshold_scaled) / (current_scaled - previous_scaled)
        return dt_hours * fraction
    if previous_scaled > threshold_scaled >= current_scaled:
        fraction = (previous_scaled - threshold_scaled) / (previous_scaled - current_scaled)
        return dt_hours * fraction
    return 0.0


@dataclass(frozen=True)
class ColdChainState:
    temperature_c: float
    elapsed_hours: float = 0.0

    def __post_init__(self):
        if not _finite_number(self.temperature_c) or not _finite_number(self.elapsed_hours) or self.elapsed_hours < 0:
            raise ValueError("temperature and elapsed time must be finite numbers; elapsed time cannot be negative")


@dataclass(frozen=True)
class SimulationResult:
    states: tuple[ColdChainState, ...]
    max_temperature_c: float
    excursion_hours: float


def step(state: ColdChainState, *, ambient_c: float, cooling_c_per_hour: float, thermal_rate: float = 0.20, dt_hours: float = 0.25) -> ColdChainState:
    values = (ambient_c, cooling_c_per_hour, thermal_rate, dt_hours)
    if any(not _finite_number(value) for value in values):
        raise ValueError("thermal inputs must be finite numbers")
    if not isinstance(state, ColdChainState):
        raise TypeError("state must be a ColdChainState")
    if cooling_c_per_hour < 0 or thermal_rate < 0 or dt_hours <= 0:
        raise ValueError("cooling and thermal rate must be non-negative; dt_hours must be positive")
    if not math.isfinite(thermal_rate * dt_hours) or thermal_rate * dt_hours > 1.0:
        raise ValueError("thermal_rate * dt_hours must be <= 1 for a monotone explicit-Euler step")
    drift = thermal_rate * (ambient_c - state.temperature_c)
    next_temp = state.temperature_c + (drift - cooling_c_per_hour) * dt_hours
    return ColdChainState(next_temp, state.elapsed_hours + dt_hours)


def simulate(
    initial_c: float,
    ambient_profile: list[float],
    *,
    cooling_c_per_hour: float,
    max_allowed_c: float,
    dt_hours: float = 0.25,
) -> SimulationResult:
    if not isinstance(ambient_profile, list):
        raise ValueError("ambient_profile must be a list of temperatures")
    if not all(_finite_number(value) for value in (dt_hours, cooling_c_per_hour, initial_c, max_allowed_c)):
        raise ValueError("simulation inputs must be finite numbers")
    if dt_hours <= 0 or cooling_c_per_hour < 0:
        raise ValueError("dt_hours must be positive and cooling_c_per_hour non-negative")
    state = ColdChainState(initial_c)
    states = [state]
    excursion = 0.0
    for ambient in ambient_profile:
        previous_c = state.temperature_c
        state = step(
            state,
            ambient_c=ambient,
            cooling_c_per_hour=cooling_c_per_hour,
            dt_hours=dt_hours,
        )
        states.append(state)
        excursion += threshold_excursion_hours(previous_c, state.temperature_c, max_allowed_c, dt_hours)
        if not math.isfinite(excursion):
            raise OverflowError("simulation excursion total is not finite")

    return SimulationResult(
        states=tuple(states),
        max_temperature_c=max(s.temperature_c for s in states),
        excursion_hours=excursion,
    )


if __name__ == "__main__":
    result = simulate(4.0, [30.0] * 12, cooling_c_per_hour=3.0, max_allowed_c=8.0)
    print(result)
