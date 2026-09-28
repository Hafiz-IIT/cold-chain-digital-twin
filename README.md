# Cold Chain Digital Twin

> Software-only cold-chain digital twin for temperature drift, active cooling and excursion analysis.

## Status
**Reproducible simulation/research prototype** with tests, CI, architecture, evaluation and roadmap documentation.

## Problem
Cold-chain decisions depend on dynamic interaction between cargo temperature, ambient conditions and cooling. A transparent simulator enables controlled experiments before real IoT integration.

## Architecture
Initial temperature + ambient profile + first-order thermal dynamics + cooling input → time-step simulation → max-temperature and excursion-duration metrics.

## Run
```bash
python -m unittest discover -s tests -v
python cold_chain_digital_twin.py
```

## Implemented
- Cold-chain state model
- First-order thermal drift
- Cooling control input
- Configurable time step
- Ambient profile simulation
- Excursion tracking
- Summary metrics
- Tests and CI

## Research lineage
- *Digital Twins for Healthcare and Wellness Applications*
- *AI for Climate Change: Modeling Micro-Level Energy Efficiency*
- *AI in Energy Efficiency Management*

## Evaluation
Tests establish qualitative thermal behavior; future work should calibrate against real sensors and compare control strategies.

## Limitations
- Simplified first-order physics
- No real IoT ingestion
- No product-specific thermal mass model
- No compliance certification claim

## License
MIT.

## Extended implementation

- `controller.py` adds thermostat control, closed-loop simulation, excursion tracking, and a cooling-energy proxy.
