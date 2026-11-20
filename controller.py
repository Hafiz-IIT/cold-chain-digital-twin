from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from cold_chain_digital_twin import ColdChainState, step


@dataclass(frozen=True)
class ControlledResult:
    states: tuple[ColdChainState, ...]
    cooling_history: tuple[float, ...]
    cooling_energy_proxy: float
    excursion_hours: float


def thermostat_cooling(
    temperature_c: float,
    *,
    target_c: float,
    max_cooling_c_per_hour: float,
    deadband_c: float = 0.5,
) -> float:
    values = (temperature_c, target_c, max_cooling_c_per_hour, deadband_c)
    if not all(isfinite(float(value)) for value in values):
        raise ValueError("thermostat inputs must be finite")
    if max_cooling_c_per_hour < 0 or deadband_c < 0:
        raise ValueError("maximum cooling and deadband must be non-negative")
    return max_cooling_c_per_hour if temperature_c > target_c + deadband_c else 0.0


def simulate_controlled(
    initial_c: float,
    ambient_profile: list[float],
    *,
    target_c: float,
    max_allowed_c: float,
    max_cooling_c_per_hour: float,
    dt_hours: float = 0.25,
) -> ControlledResult:
    numeric_inputs = (initial_c, target_c, max_allowed_c, max_cooling_c_per_hour, dt_hours)
    if not all(isfinite(float(value)) for value in numeric_inputs):
        raise ValueError("controlled simulation inputs must be finite")
    if max_cooling_c_per_hour < 0 or dt_hours <= 0:
        raise ValueError("maximum cooling must be non-negative and dt_hours must be positive")
    state = ColdChainState(initial_c)
    states = [state]
    cooling_history: list[float] = []
    energy = 0.0
    excursion = 0.0

    for ambient in ambient_profile:
        cooling = thermostat_cooling(
            state.temperature_c,
            target_c=target_c,
            max_cooling_c_per_hour=max_cooling_c_per_hour,
        )
        state = step(
            state,
            ambient_c=ambient,
            cooling_c_per_hour=cooling,
            dt_hours=dt_hours,
        )
        cooling_history.append(cooling)
        states.append(state)
        energy += cooling * dt_hours
        if state.temperature_c > max_allowed_c:
            excursion += dt_hours

    return ControlledResult(
        states=tuple(states),
        cooling_history=tuple(cooling_history),
        cooling_energy_proxy=energy,
        excursion_hours=excursion,
    )
