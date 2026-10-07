# Cold Chain Digital Twin

<p align="center"><strong>Thermal Dynamics Before Physical Deployment</strong><br/><sub>A transparent software-only model of temperature drift, cooling and excursion risk.</sub></p>

<p align="center"><img src="https://img.shields.io/badge/status-reproducible%20simulation-blue" alt="Simulation"/> <img src="https://img.shields.io/badge/model-first--order%20thermal%20dynamics-orange" alt="Model"/></p>

## Question

**How do ambient conditions and active cooling change cold-chain excursion behavior over time?**

```
Initial cargo state
      +
Ambient profile
      +
Cooling control
      ↓
Thermal time-step simulation
      ↓
Temperature trajectory
      ↓
Excursion duration + energy proxy
```

## Try it

```bash
python cold_chain_digital_twin.py
python -m unittest discover -s tests -v
```

`controller.py` adds a closed-loop thermostat experiment so controlled and uncontrolled trajectories can be compared.

## Implemented

- cold-chain state model
- first-order thermal drift
- ambient profiles
- configurable timestep
- cooling input
- excursion tracking
- thermostat controller
- cooling-energy proxy
- deterministic CI

## Research boundary

Software simulation only. No physical sensor/IoT deployment or validated refrigerated-container model is claimed.

Related: [Logistics Optimization Lab](https://github.com/Hafiz-IIT/logistics-optimization-lab) · [Port Operations Simulator](https://github.com/Hafiz-IIT/port-operations-simulator)
