from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ColdChainState:
    temperature_c: float
    elapsed_hours: float = 0.0


@dataclass(frozen=True)
class SimulationResult:
    states: tuple[ColdChainState, ...]
    max_temperature_c: float
    excursion_hours: float


def step(state: ColdChainState, *, ambient_c: float, cooling_c_per_hour: float, thermal_rate: float = 0.20, dt_hours: float = 0.25) -> ColdChainState:
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
        if state.temperature_c > max_allowed_c:
            excursion += dt_hours

    return SimulationResult(
        states=tuple(states),
        max_temperature_c=max(s.temperature_c for s in states),
        excursion_hours=round(excursion, 6),
    )


if __name__ == "__main__":
    result = simulate(4.0, [30.0] * 12, cooling_c_per_hour=3.0, max_allowed_c=8.0)
    print(result)
