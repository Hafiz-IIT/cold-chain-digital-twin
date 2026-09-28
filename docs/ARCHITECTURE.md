# Architecture

Initial temperature + ambient profile + first-order thermal dynamics + cooling input → time-step simulation → max-temperature and excursion-duration metrics.

## Invariants
1. Hotter ambient conditions should not spontaneously cool cargo without cooling input.
2. Cooling input must reduce temperature relative to no-cooling baseline.
3. Excursion time is accumulated only above the configured threshold.
