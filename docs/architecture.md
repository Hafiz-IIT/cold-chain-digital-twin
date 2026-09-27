# Architecture

```mermaid
flowchart LR
    N0[initial temperature] --> N1
    N1[ambient profile] --> N2
    N2[thermal drift] --> N3
    N3[cooling] --> N4
    N4[state trajectory] --> N5
    N5[excursion summary]
```

## State
Temperature and elapsed time form the simulated cold-chain state.

## Dynamics
Ambient temperature pulls the package toward environmental temperature while active cooling offsets drift.

## Simulation
Repeated time steps produce a trajectory.

## Excursion analysis
Time above a chosen threshold and maximum temperature summarize risk.

## Principle
Keep the physical assumptions visible and simple enough to challenge before adding ML or IoT complexity.
