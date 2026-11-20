# Evaluation

## Question
How can a transparent first-order thermal simulator quantify temperature excursions and cooling-control trade-offs under varying ambient profiles?

## Metrics
- Maximum temperature
- Excursion duration, linearly interpolated within each discrete step
- Cooling-energy proxy (not measured electrical energy)
- Temperature trajectory
- Sensitivity to ambient regime and timestep

## Model assumptions and limitations
- The state update is an explicit-Euler approximation of a first-order lumped thermal model.
- The thermal-rate and cooling parameters are user-supplied; they are not calibrated against a physical shipment or logger dataset.
- Linear interpolation estimates threshold-crossing time within each timestep; accuracy still depends on timestep size and the assumed linear trajectory.
- The cooling-energy value is a proxy, not a compressor power or battery-energy model.

## Falsification
- Cooling increases temperature under identical conditions.
- Excursion time is counted for an interval entirely below threshold.
- A threshold crossing is charged as a full timestep when only part of the step is above threshold.
- State time fails to advance consistently.
