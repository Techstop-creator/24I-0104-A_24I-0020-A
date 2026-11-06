# LIFELINE: Iteration 1 Approach Note (`approach.md`)

**Course:** Design and Analysis of Algorithms | FAST-NUCES Islamabad  
**Degree:** BS Artificial Intelligence (AI)  
**Project:** LIFELINE — Algorithmic Relief-Command Engine (Phase 1)  
**Group Number:** 66 | **Section:** AI-A  
**Team Members:**  
* **Member 1:** Irtaza Shahid | Roll No: `24I-0104` | Section: `AI-A`  
* **Member 2:** Muhammad Harris | Roll No: `24I-0020` | Section: `AI-A`  

---

## Part 1: From Story to Numbers

Every numerical bound, probability distribution, and graph topology implemented in our synthetic generator directly mirrors the narrative physics of the 6 disaster scenarios:

### 1. Delta Flood (Scenario 1)
* **Narrative Anchor:** *"A river has burst its embankments. A flat delta of small villages joined by raised roads. Roads go under water in waves. Food and water matter most."*
* **Numerical & Algorithmic Choices:**
  * **Graph Topology:** Average degree $2E/V \in [2.2, 3.2]$. This models a planar mesh of raised embankments crossing flat marshland with low-degree local junctions.
  * **Node Penalties:** At least $40\%$ of locations have $\text{penalty} \ge 2$ (assigned values from $\{2, 4, 6\}$). This represents waterlogged, submerged terrain where vehicles must slow down or navigate flooded access roads.
  * **Dynamic Closures:** At least 3 disjoint closure waves simulate the progressive, multi-stage rise of flood waters cutting off embankments.
  * **Cargo Distribution:** Food and Water crates (categories 0 and 1) constitute $\ge 55\%$ of all relief inventory, reflecting basic survival necessities over tools or rare equipment.

### 2. Mountain Earthquake (Scenario 2)
* **Narrative Anchor:** *"A valley town with a few roads and almost no alternatives. The injured need medicine and tools. Bursts of urgent calls follow each aftershock."*
* **Numerical & Algorithmic Choices:**
  * **Graph Topology:** Sparse, tree-like canyon topology with average degree $2E/V \in [2.0, 2.6]$. This strictly reflects valley geography where towns have minimal or single-path road connectivity.
  * **Cargo Distribution:** Medicine and Tool crates (categories 2 and 3) constitute $\ge 45\%$ of all relief cargo to treat crushing trauma and excavate rubble.
  * **Urgency & Alarms:** Mean alarm priority is constrained to $\ge 6.0$ (sampled heavily from $\{7, 8, 9, 10\}$), capturing the acute distress and casualty spikes that follow successive aftershocks.

### 3. Coastal Cyclone (Scenario 3)
* **Narrative Anchor:** *"A port city and fishing villages. Storm surge closes roads in waves. Rescue windows are short and overlap. The radio is full of noise."*
* **Numerical & Algorithmic Choices:**
  * **Shelter Capacity:** At least $25\%$ of all locations are designated as Shelters (`type = 'S'`) to absorb evacuating coastal populations.
  * **Surge Severance:** At least 3 disjoint road closure waves model incoming tidal surges.
  * **Window Contention:** Evacuation and rescue time windows are generated in temporal clusters such that every window overlaps at least 2 other windows on average ($\ge 2.0$), creating dense interval scheduling conflict graphs.
  * **Signal Noise:** Radio log strings utilize $\ge 30$ of the 38 allowable alphabet characters (`A-Z`, `0-9`, `_`, `-`), reflecting high ambient atmospheric radio noise and broad spectrum degradation.

### 4. Urban Flash Flood (Scenario 4)
* **Narrative Anchor:** *"A dense city with many alternative routes. Calls arrive faster than anyone can answer them. Rare equipment is available."*
* **Numerical & Algorithmic Choices:**
  * **Graph Topology:** Dense urban street grid with average degree $2E/V \ge 3.5$, providing abundant detour routes.
  * **Incident Throughput:** High population density and rapid inundation create arrival rates between $1.2$ and $1.8$ alarms per tick on Tiers M and L (averaging $\ge 1.5$ alarms/tick).
  * **Cargo Availability:** Specialized technical assets (high-capacity drainage pumps, inflatable boats) result in Rare Equipment crates (category 4) comprising $\ge 10\%$ of all crates.

### 5. Landslide Corridor (Scenario 5)
* **Narrative Anchor:** *"A single mountain highway along a gorge. A collapse cuts off whole communities."*
* **Numerical & Algorithmic Choices:**
  * **Linear Topology:** Strict gorge constraints enforce max node degree $\le 4$ (implemented as $\le 3$) and average degree $\le 2.4$. The graph features a long central highway spine where the farthest location from the HQ (Node 0) is at least $\lfloor V/4 \rfloor$ roads away.
  * **Complete Isolation:** Generated in $\ge 3$ closure waves. Crucially, the union of all waves severs all incident edges to at least one designated relief target (`target_0`), leaving it completely unreachable from the HQ.

### 6. Outbreak Camp (Scenario 6)
* **Narrative Anchor:** *"A relief camp with an outbreak. Medicine and water count and supplies spoil. Radio beacons repeat the same messages."*
* **Numerical & Algorithmic Choices:**
  * **Epidemic Supply Profile:** Medicine (cat 2) and Water (cat 1) crates account for $\ge 55\%$ of inventory to hydrate patients and administer antibiotics.
  * **Spoilage Expiration:** Rapid degradation of vaccines and sterile supplies requires at least $50\%$ of all crates to expire within the first 300 hours ($\text{expiry} \le 300$).
  * **Repetitive Transmissions:** Automated emergency radio beacons transmitting repetitive telemetry cause a single dominant alphabet character to occupy $\ge 25\%$ of the entire radio log.

---

## Part 2: Planted Objects and Claims (Correct by Construction)

To provide reliable ground truth for NP-hard and combinatorial sub-problems, the generator synthesizes planted objects using mathematically guaranteed construction invariants:

### 1. Planted Closed TSP Tour (Sites & Tour)
* **Construction:** Sites are plotted on a $1000 \times 1000$ integer grid. For Tiers L and X ($n \in [200, 500]$), the generator runs a greedy Nearest Neighbor (NN) heuristic starting from Site 0 to construct a closed tour permutation. Because the planted tour is identical to or locally refined from this heuristic path, its closed Manhattan length:
  $$\text{tour\_length} = \sum_{i=0}^{n-2} \Big(|x_{\pi_i} - x_{\pi_{i+1}}| + |y_{\pi_i} - y_{\pi_{i+1}}|\Big) + \Big(|x_{\pi_{n-1}} - x_0| + |y_{\pi_{n-1}} - y_0|\Big)$$
  is **guaranteed by construction to be $\le$ the Nearest Neighbor tour length**.
* **Zero-Trust Verification:** Validator check `V6` recalculates the closed Manhattan distance from scratch and verifies that $\text{tour\_length} \le \text{NN\_tour}$.

### 2. Planted Minimum Vertex Cover (Sensors)
* **Construction:** The generator first selects a subset of $k$ distinct nodes ($2 \le k \le n/2$) to designate as the planted cover set $C$. Every edge $(u, v)$ in `sensor_edges` is subsequently generated by requiring that at least one endpoint belongs to $C$ (i.e. $u \in C$ or $v \in C$).
* **Guarantee:** By construction, every edge in the graph touches at least one node in $C$.
* **Zero-Trust Verification:** Validator check `V6` checks every edge $(u, v)$ against `sensor_cover`, confirming $0$ uncovered edges.

### 3. Planted 3-SAT Assignment (Safety Rules)
* **Construction:** A random boolean truth assignment vector $A \in \{0, 1\}^N$ across all variables $1 \dots \text{safety\_vars}$ is sampled first. Each of the $M$ clauses in `safety_rules` is constructed by selecting 3 distinct variables and forcing at least one literal to agree with assignment $A$ (i.e. $+x$ if $A[x]=1$, $-x$ if $A[x]=0$).
* **Guarantee:** Every clause has at least one true literal under assignment $A$; hence, the entire 3-CNF formula is satisfiable by construction.
* **Zero-Trust Verification:** Validator check `V6` substitutes `safety_planted` values into all clauses, confirming $100\%$ clause satisfaction.

### 4. Planted Subset Sum (Rations Target)
* **Construction:** Given $M$ ration items with positive integer values, the generator randomly selects a non-empty subset $S \subset \{0 \dots M-1\}$, marks their records with `planted = 1` (and `0` otherwise), and sets:
  $$\text{rations\_target} = \sum_{i \in S} \text{value}_i$$
* **Guarantee:** The subset sum problem has an exact solution that sums to `rations_target` by definition.
* **Zero-Trust Verification:** Validator check `V6` sums all values where `planted == 1` and asserts exact equality with `rations_target`.

### 5. Tier S Exact Optima (`claims` sheet)
* **Construction:** For Tier S cases ($k = 0 \dots 19$), the generator executes exact combinatorial solvers:
  * `cargo_opt`: Exact 0/1 Knapsack via dynamic programming ($O(N \cdot W)$).
  * `window_count_opt`: Maximum non-overlapping intervals via earliest finish time greedy ($O(M \log M)$).
  * `window_value_opt`: Maximum weighted intervals via dynamic programming with binary search predecessors ($O(M \log M)$).
  * `drum_opt`: Unbounded rod cutting dynamic programming ($O(L^2)$).
  * `tour_opt`: Exact closed Manhattan TSP via Held-Karp dynamic programming / branch-and-bound ($O(n^2 2^n)$ for $n \le 8$).
  * `cover_min`: Exact minimum vertex cover via exhaustive bitmask search ($O(2^n \cdot E)$ for $n \le 10$).
* **Zero-Trust Verification:** Validator check `V5` re-solves all 6 problems independently and asserts exact equivalence with the recorded claims.

---

## Part 3: The Four Hostile Traps (Cases 46 to 49)

Cases 46 to 49 (Tier X) are deliberately engineered adversarial stress tests designed to expose and break naive algorithmic implementations:

### Case 46: Dock-Order Trap (Story 5: Landslide Corridor)
* **What We Built:** A dataset of $1,600$ crates where all five crate attributes are monotonically non-decreasing:
  * `weight` is constant ($10$ kg for all crates; trivially non-decreasing and non-increasing).
  * `value` is ordered non-decreasing ($10 \to 100$).
  * `expiry` is ordered non-decreasing ($0 \to 999$).
  * `serial` is ordered non-decreasing ($10^7 \dots 10^7 + 1600$).
  * `value_per_kg` ($=\text{value}/10$) is monotonically non-decreasing.
* **Why It Is Hostile:** Naive implementations of Quicksort that pick the first or last element as the pivot partition the array into subarrays of size $0$ and $N-1$ at every step. This triggers the **worst-case $O(N^2)$ running time** and causes recursion depth limit exceptions on large crate arrays ($N = 1,600$).
* **Validator Check:** Check `V8` evaluates array monotonicity across all 5 fields and asserts that at least 3 fields are strictly monotone.

### Case 47: Best-Looking-Crate Trap (Story 6: Outbreak Camp)
* **What We Built:** A knapsack instance with capacity $W = 20$ and 12 crates:
  * Crate 1: Weight $w_1 = 11$, Value $v_1 = 55 \implies \text{value/kg ratio} = \mathbf{5.0}$.
  * Crate 2: Weight $w_2 = 10$, Value $v_2 = 48 \implies \text{value/kg ratio} = \mathbf{4.8}$.
  * Crate 3: Weight $w_3 = 10$, Value $v_3 = 48 \implies \text{value/kg ratio} = \mathbf{4.8}$.
  * Crates 4 to 12: Weight $w_i = 10$, Value $v_i = 10 \implies \text{value/kg ratio} = 1.0$.
* **Why It Is Hostile:** A greedy density heuristic sorts crates by value-per-kg descending. It greedily selects Crate 1 ($w=11$), leaving remaining capacity $20 - 11 = 9$ kg. Because all other crates have weight $10$ kg, none can fit in the remaining $9$ kg. Greedy yields total value $\mathbf{55}$. The optimal 0/1 knapsack dynamic program skips Crate 1 and selects Crates 2 & 3 ($w = 10 + 10 = 20 \le W$), yielding total value $\mathbf{96}$.  
  $$\text{Greedy Ratio} = \frac{55}{96} = \mathbf{57.29\% \le 60\%}$$
* **Validator Check:** Check `V8` runs both greedy density and 0/1 knapsack DP, asserting $\text{greedy} \le 0.60 \times \text{optimal}$.

### Case 48: Shortest-Looks-Cheapest Trap (Story 1: Delta Flood)
* **What We Built:** A 1,600-location network with a 600-node linear chain ($4 \to 5 \to \dots \to 604$), ensuring a longest distance $\ge 500$ roads. Between HQ (Node 0) and `target_0`:
  * Direct 1-road path $(0 \to \text{target}_0)$: $\text{minutes} = 60$, destination $\text{penalty} = 6 \implies \text{total cost} = \mathbf{66}$.
  * Alternate 3-road path $(0 \to 2 \to 3 \to \text{target}_0)$: Each edge has $\text{minutes} = 1$, intermediate junctions have $\text{penalty} = 0$, destination has $\text{penalty} = 6 \implies \text{total cost} = 1 + 1 + (1 + 6) = \mathbf{9}$.
* **Why It Is Hostile:** An unweighted shortest-path algorithm (BFS) seeks the minimum road count (hop count) and selects the 1-road direct edge with cost $66$. Dijkstra's weighted shortest-path algorithm identifies the 3-road detour with cost $9$. Every fewest-roads path is $\mathbf{7.33\times}$ more expensive than the cheapest path ($\ge 1.5\times$).
* **Validator Check:** Check `V8` computes hop counts from Node 4 (asserting max distance $\ge 500$) and compares all fewest-roads paths against Dijkstra's cheapest cost, verifying ratio $\ge 1.5$.

### Case 49: Near-Miss Trap (Story 2: Mountain Earthquake)
* **What We Built:** A 60,000-character radio log composed entirely of the symbol `'A'`. Search patterns of lengths 2, 4, 8, 12, 20, 40 are generated:
  * Pattern 0 (len 2): `"AB"` (Prefix `"A"` matches at $100\%$ of positions).
  * Pattern 1 (len 4): `"AAAB"` (Prefix `"AAA"` matches at $100\%$ of positions).
  * Pattern 2 (len 8): `"AAAAAAAB"` (Prefix `"AAAAAAA"` matches at $100\%$ of positions).
  * Pattern 3 (len 12): `"AAAAAAAAAAAB"` (Prefix `"AAAAAAAAAAA"` matches at $100\%$ of positions).
* **Why It Is Hostile:** Naive string matching compares characters sequentially. At every start position $0 \dots 59,998$, the naive matcher performs $(L - 1)$ successful character comparisons before failing on the terminal character `'B'`. This induces worst-case **$O(N \cdot M)$ comparison thrashing**. Linear algorithms (KMP, Boyer-Moore) are required to avoid backtracking.
* **Validator Check:** Check `V8` asserts log block repetition $\ge 90\%$ and confirms that $\ge 4$ patterns match their length-1 prefix at $\ge 50\%$ of all starting positions.

---

## Part 4: What Will Be Hard in Iteration 2

For each case study, two relief decision modules will present severe computational hurdles during Iteration 2 implementation:

| Case Study | Decision 1: Hardest Relief Challenge | Decision 2: Hardest Relief Challenge |
| :--- | :--- | :--- |
| **1. Delta Flood** | **Module B (Route Planning):** Roads close in sequential waves, requiring dynamic time-dependent graph search (re-running Dijkstra or updating reachability matrices dynamically) rather than static routing. | **Module A (Relief Inventory):** Waterlogged relief demands high volumes of low-weight food/water crates, creating tight knapsack packing states where fractional branch-and-bound bounds fail to prune efficiently. |
| **2. Mountain Earthquake** | **Module D (Emergency Queue):** High mean alarm priority ($\ge 6.0$) causes extreme heap tie-breaking and priority inversion, requiring strict secondary FIFO timestamp tie-breaking in priority queues. | **Module I (Nearest Sites):** Branching canyon topologies invalidate Euclidean straight-line heuristics, necessitating full graph distance lookups rather than spatial quad-trees. |
| **3. Coastal Cyclone** | **Module C (Rescue Scheduling):** Densely clustered rescue windows (average overlap $\ge 2.0$) create dense interval graphs where greedy fails completely and weighted DP requires $O(M \log M)$ predecessor binary searches. | **Module E (Radio Logs):** Broad alphabet distribution ($\ge 30$ symbols) maximizes signal entropy, deepening Huffman coding trees and requiring adaptive prefix coding. |
| **4. Urban Flash Flood** | **Module D (Emergency Queue):** Sustained alarm arrival rates of $1.5$ to $1.8$ alarms/tick overwhelm linear buffers, making binary min/max-heap operations mandatory to prevent queue starvation. | **Module B (Route Planning):** High graph density (average degree $\ge 3.5$) expands priority queue size and relaxation overhead during shortest-path exploration. |
| **5. Landslide Corridor** | **Module B (Route Planning):** Multi-wave rockslides isolate entire target communities, requiring cut-detection algorithms (Tarjan's bridges / articulation points) to detect unreachable nodes early. | **Module G (Chains & Cuts):** Extreme highway diameter forces high hop counts, significantly increasing dynamic programming state spaces for pipeline signal stages. |
| **6. Outbreak Camp** | **Module A (Relief Inventory):** Over $50\%$ of crates expire by hour 300, converting standard 0/1 knapsack into a 2D time-constrained knapsack problem with expiration penalties. | **Module E (Radio Logs):** Dominant beacon repetition ($\ge 25\%$ single symbol) creates highly skewed symbol frequencies, requiring prefix trees or run-length encoding. |
