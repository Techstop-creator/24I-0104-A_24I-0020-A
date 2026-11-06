# LIFELINE Data Generator

This program generates `cases.xlsx` for Group 66 (Roll Nos: 24i-0104, 24i-0020), strictly following all rules, schemas, tier bounds, case signatures, planted objects, and trap specifications of the LIFELINE project (Phase 1).

## Reproduction Command

Run the following single command from this directory:

```bash
python main.py --seed 66 --output ../cases.xlsx
```

Or from the project root:

```bash
python generator/main.py --seed 66 --output cases.xlsx
```

## Structure
- `main.py`: Entry point and Excel workbook serialization with 20 sheets and strict sorting.
- `case_generator.py`: Algorithmic builder for all 50 cases (Tiers S, M, L, X) enforcing signatures, planted solutions, and hostile traps.
- `algorithms.py`: Exact solvers (Knapsack DP, Interval Scheduling, Rod Cutting DP, TSP DP, Minimum Vertex Cover bitmask search, Levenshtein distance) used for generating verifiable Tier S claims and signature properties.

