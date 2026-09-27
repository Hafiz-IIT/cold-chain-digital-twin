# Cold Chain Digital Twin

> **A software-only thermal twin for studying temperature drift, cooling control, and excursion risk.**

Cold-chain failures are time-dependent: ambient heat, cooling capacity, and duration interact. This repository turns the old cold-chain IoT/logistics idea into a reproducible thermal simulation without pretending real sensors exist.

## Implemented
- cold-chain state model
- first-order ambient thermal drift
- configurable cooling power
- discrete time-step simulation
- temperature excursion tracking
- maximum-temperature summary

## Run
```bash
python -m unittest discover -s tests -v
python cold_chain_digital_twin.py
```

## Repository map
`cold_chain_digital_twin.py` core · `tests/` tests · `examples/` fixtures · `docs/architecture.md` design · `docs/research-agenda.md` experiments · `STATUS.md` claims · `CITATION.cff` citation

## Pipeline
**initial temperature → ambient profile → thermal drift → cooling → state trajectory → excursion summary**

## Research lineage
This repository consolidates the older cold-chain IoT, logistics digital-twin, shipment-monitoring, and predictive-operations themes.

## Evaluation direction
Sweep ambient profiles, cooling capacity, time step, and thermal rate. Later calibrate only if a legitimate real sensor dataset becomes available.

## Maturity
**Research prototype.** This is a simplified simulator, not a calibrated food/pharmaceutical model, regulatory compliance tool, real IoT ingestion system, or hardware digital twin.
