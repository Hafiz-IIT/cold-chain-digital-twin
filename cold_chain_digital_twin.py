from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ColdChainState:
    temperature_c: float
    elapsed_hours: float = 0.0

    def __post_init__(self):
        if not math.isfinite(self.temperature_c) or not math.isfinite(self.elapsed_hours) or self.elapsed_hours < 0:
            raise ValueError("temperature and elapsed time must be finite; elapsed time cannot be negative")


@dataclass(frozen=True)
class SimulationResult:
    states: tuple[ColdChainState, ...]
    max_temperature_c: float
    excursion_hours: float


def step(state: ColdChainState, *, ambient_c: float, cooling_c_per_hour: float, thermal_rate: float = 0.20, dt_hours: float = 0.25) -> ColdChainState:
    values = (ambient_c, cooling_c_per_hour, thermal_rate, dt_hours)
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) for value in values):
        raise ValueError("thermal inputs must be finite numbers")
    if cooling_c_per_hour < 0 or thermal_rate < 0 or dt_hours <= 0:
        raise ValueError("cooling and thermal rate must be non-negative; dt_hours must be positive")
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
    if not math.isfinite(dt_hours) or dt_hours <= 0:
        raise ValueError("dt_hours must be finite and positive")
    if not math.isfinite(cooling_c_per_hour) or cooling_c_per_hour < 0:
        raise ValueError("cooling_c_per_hour must be finite and non-negative")
    if not math.isfinite(initial_c) or not math.isfinite(max_allowed_c):
        raise ValueError("initial and maximum allowed temperatures must be finite")
    state = ColdChainState(initial_c)
    states = [state]
    excursion = 0.0
    for ambient in ambient_profile:
        state = step(
            state,
            ambient_c=ambient,
            cooling_c_per_hour=cooling_c_per_hour,
            dt_hours=dt_hours,
        )
        states.append(state)
        previous_c = states[-2].temperature_c
        current_c = state.temperature_c
        # Estimate threshold-crossing time by linear interpolation within the
        # discrete step instead of counting an entire interval from its endpoint.
        if previous_c > max_allowed_c and current_c > max_allowed_c:
            excursion += dt_hours
        elif previous_c <= max_allowed_c < current_c:
            excursion += dt_hours * (current_c - max_allowed_c) / (current_c - previous_c)
        elif previous_c > max_allowed_c >= current_c:
            excursion += dt_hours * (previous_c - max_allowed_c) / (previous_c - current_c)

    return SimulationResult(
        states=tuple(states),
        max_temperature_c=max(s.temperature_c for s in states),
        excursion_hours=round(excursion, 6),
    )


if __name__ == "__main__":
    result = simulate(4.0, [30.0] * 12, cooling_c_per_hour=3.0, max_allowed_c=8.0)
    print(result)
