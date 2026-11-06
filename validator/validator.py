"""
LIFELINE Independent Validator Engine
Design and Analysis of Algorithms - Project Phase 1
Checks V1 through V8 against the LIFELINE specification.
"""

import sys
import os
import math
import openpyxl
from collections import deque
import itertools

SHEET_CONFIG = [
    ('cases', [
        'case_id', 'group_seed', 'case_no', 'tier', 'scenario', 'capacity',
        'target_0', 'target_1', 'target_2', 'edit_bound', 'tour_length',
        'sensor_nodes', 'sensor_k', 'safety_vars', 'rations_target'
    ]),
    ('crates', [
        'case_id', 'crate_id', 'cat', 'weight', 'value', 'expiry', 'serial'
    ]),
    ('locations', [
        'case_id', 'loc_id', 'type', 'penalty'
    ]),
    ('roads', [
        'case_id', 'road_no', 'u', 'v', 'minutes', 'cable'
    ]),
    ('waves', [
        'case_id', 'wave_no', 'road_no'
    ]),
    ('radio_log', [
        'case_id', 'part', 'text'
    ]),
    ('radio_patterns', [
        'case_id', 'pattern_no', 'pattern', 'count'
    ]),
    ('radio_reports', [
        'case_id', 'report_a', 'report_b'
    ]),
    ('windows', [
        'case_id', 'window_id', 'start', 'finish', 'value'
    ]),
    ('incidents', [
        'case_id', 'alarm_id', 'tick', 'priority'
    ]),
    ('sites', [
        'case_id', 'site_no', 'x', 'y'
    ]),
    ('tour', [
        'case_id', 'step', 'site_no'
    ]),
    ('pipeline_dims', [
        'case_id', 'idx', 'dim'
    ]),
    ('drum_prices', [
        'case_id', 'length', 'price'
    ]),
    ('sensor_edges', [
        'case_id', 'u', 'v'
    ]),
    ('sensor_cover', [
        'case_id', 'node'
    ]),
    ('safety_rules', [
        'case_id', 'rule_no', 'lit_1', 'lit_2', 'lit_3'
    ]),
    ('safety_planted', [
        'case_id', 'switch', 'value'
    ]),
    ('rations', [
        'case_id', 'item', 'value', 'planted'
    ]),
    ('claims', [
        'case_id', 'cargo_opt', 'window_count_opt', 'window_value_opt', 'drum_opt', 'tour_opt', 'cover_min'
    ])
]

EXPECTED_SHEETS = [s[0] for s in SHEET_CONFIG]
EXPECTED_HEADERS = {s[0]: s[1] for s in SHEET_CONFIG}

def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def compute_levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def solve_knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[capacity]

def solve_greedy_knapsack(weights, values, capacity):
    items = [(v / w, w, v) for w, v in zip(weights, values)]
    items.sort(key=lambda x: (-x[0], x[1]))
    cur_cap = capacity
    tot_val = 0
    for ratio, w, v in items:
        if w <= cur_cap:
            cur_cap -= w
            tot_val += v
    return tot_val

def solve_interval_count(windows):
    sorted_w = sorted(windows, key=lambda x: (x[1], x[0]))
    count = 0
    last_finish = -1
    for s, f, val in sorted_w:
        if s >= last_finish:
            count += 1
            last_finish = f
    return count

def solve_interval_value(windows):
    sorted_w = sorted(windows, key=lambda x: x[1])
    n = len(sorted_w)
    dp = [0] * (n + 1)
    finishes = [w[1] for w in sorted_w]
    for i in range(1, n + 1):
        s, f, val = sorted_w[i - 1]
        low, high, p = 0, i - 1, 0
        while low <= high:
            mid = (low + high) // 2
            if finishes[mid] <= s:
                p = mid + 1
                low = mid + 1
            else:
                high = mid - 1
        dp[i] = max(dp[i - 1], dp[p] + val)
    return dp[n]

def solve_rod_cutting(prices, L):
    dp = [0] * (L + 1)
    for i in range(1, L + 1):
        max_v = -1
        for j in range(1, i + 1):
            val = prices[j - 1] + dp[i - j]
            if val > max_v:
                max_v = val
        dp[i] = max_v
    return dp[L]

def solve_exact_tsp(sites):
    n = len(sites)
    if n <= 1:
        return 0
    dist = [[manhattan_dist(sites[i], sites[j]) for j in range(n)] for i in range(n)]
    memo = {}
    def tsp(mask, u):
        if mask == (1 << n) - 1:
            return dist[u][0]
        state = (mask, u)
        if state in memo:
            return memo[state]
        ans = float('inf')
        for v in range(n):
            if not (mask & (1 << v)):
                ans = min(ans, dist[u][v] + tsp(mask | (1 << v), v))
        memo[state] = ans
        return ans
    return tsp(1, 0)

def solve_exact_vertex_cover(n, edges):
    if not edges:
        return 0
    for k in range(1, n + 1):
        for combo in itertools.combinations(range(n), k):
            c_set = set(combo)
            if all(u in c_set or v in c_set for u, v in edges):
                return k
    return n

def compute_nn_tour(sites):
    n = len(sites)
    visited = [False] * n
    visited[0] = True
    cur = 0
    total = 0
    for _ in range(n - 1):
        best_d = float('inf')
        best_nxt = -1
        for nxt in range(n):
            if not visited[nxt]:
                d = manhattan_dist(sites[cur], sites[nxt])
                if d < best_d:
                    best_d = d
                    best_nxt = nxt
        visited[best_nxt] = True
        total += best_d
        cur = best_nxt
    total += manhattan_dist(sites[cur], sites[0])
    return total

class Validator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []
        self.wb = None
        self.raw_data = {}
        self.cases_by_id = {}

    def log_error(self, check, msg):
        self.errors.append(f"[{check}] {msg}")

    def load_workbook(self):
        try:
            self.wb = openpyxl.load_workbook(self.filepath, data_only=True)
        except Exception as e:
            self.log_error("V1", f"Cannot load Excel file: {e}")
            return False

        # V1: Exact sheet names and order
        sheet_names = self.wb.sheetnames
        if sheet_names != EXPECTED_SHEETS:
            self.log_error("V1", f"Sheet names or order mismatch. Found: {sheet_names}")
            return False

        # Headers and data ingestion
        for s_name in EXPECTED_SHEETS:
            ws = self.wb[s_name]
            rows = list(ws.iter_rows(values_only=True))
            if not rows:
                self.log_error("V1", f"Sheet {s_name} is empty.")
                return False
            header = list(rows[0])
            if header != EXPECTED_HEADERS[s_name]:
                self.log_error("V1", f"Headers mismatch in {s_name}. Expected {EXPECTED_HEADERS[s_name]}, got {header}")
                return False

            cols = EXPECTED_HEADERS[s_name]
            sheet_rows = []
            for r_idx, r_vals in enumerate(rows[1:], start=2):
                if all(v is None for v in r_vals):
                    self.log_error("V1", f"Empty row found at row {r_idx} in sheet {s_name}")
                row_dict = {col: val for col, val in zip(cols, r_vals)}
                sheet_rows.append(row_dict)
            self.raw_data[s_name] = sheet_rows

        return True

    def build_case_indexes(self):
        cases_list = self.raw_data.get('cases', [])
        if len(cases_list) != 50:
            self.log_error("V1", f"Expected exactly 50 cases in 'cases' sheet, found {len(cases_list)}")

        seen_ids = set()
        for c in cases_list:
            cid = str(c['case_id'])
            if cid in seen_ids:
                self.log_error("V1", f"Duplicate case_id {cid} in 'cases' sheet")
            seen_ids.add(cid)
            self.cases_by_id[cid] = {'cases': c}

        # Index all other sheets by case_id
        for s_name in EXPECTED_SHEETS[1:]:
            for row in self.raw_data.get(s_name, []):
                cid = str(row['case_id'])
                if cid not in self.cases_by_id:
                    self.log_error("V3", f"Unknown case_id {cid} referenced in sheet {s_name}")
                    continue
                if s_name not in self.cases_by_id[cid]:
                    self.cases_by_id[cid][s_name] = []
                self.cases_by_id[cid][s_name].append(row)

    def validate_v1(self):
        # Format of case_id: group_seed-kk
        for cid, c_data in self.cases_by_id.items():
            c = c_data['cases']
            k = c['case_no']
            gseed = c['group_seed']
            expected_cid = f"{gseed}-{k:02d}"
            if cid != expected_cid:
                self.log_error("V1", f"Invalid case_id format {cid}, expected {expected_cid}")

            expected_tier = 'S' if k <= 19 else 'M' if k <= 39 else 'L' if k <= 45 else 'X'
            if c['tier'] != expected_tier:
                self.log_error("V1", f"Case {cid}: Tier mismatch. Expected {expected_tier}, got {c['tier']}")

            expected_scen = (k % 6) + 1
            if c['scenario'] != expected_scen:
                self.log_error("V1", f"Case {cid}: Scenario mismatch. Expected {expected_scen}, got {c['scenario']}")

    def validate_v2_and_v3(self):
        for cid, c_data in self.cases_by_id.items():
            c = c_data['cases']
            k = c['case_no']
            tier = c['tier']

            # Crates
            crates = c_data.get('crates', [])
            if k == 46:
                if not (1500 <= len(crates) <= 3000):
                    self.log_error("V2", f"Case {cid} (Trap 46): Crates count {len(crates)} not in [1500, 3000]")
            elif k == 47:
                if not (12 <= len(crates) <= 60):
                    self.log_error("V2", f"Case {cid} (Trap 47): Crates count {len(crates)} not in [12, 60]")
            elif tier == 'S':
                if not (8 <= len(crates) <= 20):
                    self.log_error("V2", f"Case {cid}: Tier S crates {len(crates)} not in [8, 20]")
            elif tier == 'M':
                if not (40 <= len(crates) <= 200):
                    self.log_error("V2", f"Case {cid}: Tier M crates {len(crates)} not in [40, 200]")
            elif tier in ('L', 'X'):
                if not (500 <= len(crates) <= 1500):
                    self.log_error("V2", f"Case {cid}: Tier L/X crates {len(crates)} not in [500, 1500]")

            crate_ids = [cr['crate_id'] for cr in crates]
            if crate_ids != list(range(1, len(crates) + 1)):
                self.log_error("V3", f"Case {cid}: crate_id must run consecutively 1, 2, ...")

            tot_crate_weight = sum(cr['weight'] for cr in crates)
            cap = c['capacity']
            if not (1 <= cap and 0.10 * tot_crate_weight <= cap <= 0.70 * tot_crate_weight + 1e-5):
                self.log_error("V2", f"Case {cid}: capacity {cap} not in [10%, 70%] of total weight {tot_crate_weight}")

            serials = set()
            for cr in crates:
                if cr['cat'] not in (0, 1, 2, 3, 4):
                    self.log_error("V2", f"Case {cid}: Invalid crate cat {cr['cat']}")
                if not (1 <= cr['weight'] <= 20):
                    self.log_error("V2", f"Case {cid}: Crate weight {cr['weight']} not in [1, 20]")
                if not (10 <= cr['value'] <= 100):
                    self.log_error("V2", f"Case {cid}: Crate value {cr['value']} not in [10, 100]")
                if not (0 <= cr['expiry'] <= 999):
                    self.log_error("V2", f"Case {cid}: Crate expiry {cr['expiry']} not in [0, 999]")
                ser = cr['serial']
                if not (10000000 <= ser <= 99999999):
                    self.log_error("V2", f"Case {cid}: Serial {ser} is not an 8-digit integer")
                if ser in serials:
                    self.log_error("V3", f"Case {cid}: Duplicate crate serial {ser}")
                serials.add(ser)

            # Locations
            locs = c_data.get('locations', [])
            V = len(locs)
            if k == 48:
                if not (1500 <= V <= 3000):
                    self.log_error("V2", f"Case {cid} (Trap 48): V={V} not in [1500, 3000]")
            elif tier == 'S' and not (6 <= V <= 12):
                self.log_error("V2", f"Case {cid}: Tier S locations {V} not in [6, 12]")
            elif tier == 'M' and not (30 <= V <= 150):
                self.log_error("V2", f"Case {cid}: Tier M locations {V} not in [30, 150]")
            elif tier in ('L', 'X') and not (500 <= V <= 2000):
                self.log_error("V2", f"Case {cid}: Tier L/X locations {V} not in [500, 2000]")

            loc_ids = [l['loc_id'] for l in locs]
            if loc_ids != list(range(V)):
                self.log_error("V3", f"Case {cid}: loc_id must run 0 to V-1")

            types = set(l['type'] for l in locs)
            if locs[0]['loc_id'] != 0 or locs[0]['type'] != 'D' or locs[0]['penalty'] != 0:
                self.log_error("V2", f"Case {cid}: Loc 0 must be HQ (type D, penalty 0)")
            if 'S' not in types or 'H' not in types:
                self.log_error("V2", f"Case {cid}: Locations must have at least one S and one H")

            loc_map = {l['loc_id']: l for l in locs}
            for t_idx in (c['target_0'], c['target_1'], c['target_2']):
                if t_idx not in loc_map:
                    self.log_error("V3", f"Case {cid}: Target {t_idx} not in locations")
                elif loc_map[t_idx]['type'] not in ('S', 'H'):
                    self.log_error("V2", f"Case {cid}: Target {t_idx} must be shelter or hospital")
                elif t_idx == 0:
                    self.log_error("V2", f"Case {cid}: Target cannot be HQ")
            if len({c['target_0'], c['target_1'], c['target_2']}) != 3:
                self.log_error("V2", f"Case {cid}: The three targets must be distinct")

            # Roads
            roads = c_data.get('roads', [])
            E = len(roads)
            if not (V - 1 <= E <= 3 * V):
                self.log_error("V2", f"Case {cid}: Roads count {E} not in [V-1, 3V] (V={V})")

            road_ids = [r['road_no'] for r in roads]
            if road_ids != list(range(E)):
                self.log_error("V3", f"Case {cid}: road_no must run 0, 1, ...")

            seen_edges = set()
            for r in roads:
                u, v = r['u'], r['v']
                if not (0 <= u < v < V):
                    self.log_error("V3", f"Case {cid}: Invalid road endpoints ({u}, {v})")
                if (u, v) in seen_edges:
                    self.log_error("V3", f"Case {cid}: Repeated road pair ({u}, {v})")
                seen_edges.add((u, v))
                if not (1 <= r['minutes'] <= 60):
                    self.log_error("V2", f"Case {cid}: Road minutes {r['minutes']} not in [1, 60]")
                if not (1 <= r['cable'] <= 100):
                    self.log_error("V2", f"Case {cid}: Road cable {r['cable']} not in [1, 100]")

            # Windows
            wins = c_data.get('windows', [])
            if tier == 'S' and not (8 <= len(wins) <= 20):
                self.log_error("V2", f"Case {cid}: Tier S windows {len(wins)} not in [8, 20]")
            touching_pairs = 0
            for i in range(len(wins)):
                w1 = wins[i]
                if not (0 <= w1['start'] < w1['finish'] <= 1440):
                    self.log_error("V2", f"Case {cid}: Window {w1['window_id']} invalid start/finish")
                if not (5 <= w1['finish'] - w1['start'] <= 480):
                    self.log_error("V2", f"Case {cid}: Window duration not in [5, 480]")
                for j in range(i + 1, len(wins)):
                    w2 = wins[j]
                    if w1['finish'] == w2['start'] or w2['finish'] == w1['start']:
                        touching_pairs += 1
            if len(wins) >= 8 and touching_pairs < 2:
                self.log_error("V2", f"Case {cid}: Expected at least 2 touching window pairs, found {touching_pairs}")

            # Incidents
            alarms = c_data.get('incidents', [])
            last_t = -1
            prios = set()
            for al in alarms:
                if al['tick'] < last_t:
                    self.log_error("V2", f"Case {cid}: Alarm ticks must never decrease")
                last_t = al['tick']
                prios.add(al['priority'])
                if not (1 <= al['priority'] <= 10):
                    self.log_error("V2", f"Case {cid}: Alarm priority {al['priority']} not in [1, 10]")

            if tier in ('M', 'L'):
                rate = len(alarms) / (last_t + 1)
                if not (1.2 <= rate <= 1.8):
                    self.log_error("V2", f"Case {cid}: Alarm rate {rate:.2f} not in [1.2, 1.8]")
                if len(prios) < 6 or 1 not in prios:
                    self.log_error("V2", f"Case {cid}: Must have at least 6 distinct priorities including 1")

    def validate_v4(self):
        for cid, c_data in self.cases_by_id.items():
            locs = c_data.get('locations', [])
            roads = c_data.get('roads', [])
            waves = c_data.get('waves', [])
            V = len(locs)
            E = len(roads)

            # Check network connectivity before closures
            adj = {i: [] for i in range(V)}
            for r in roads:
                adj[r['u']].append(r['v'])
                adj[r['v']].append(r['u'])

            visited = set()
            queue = deque([0])
            visited.add(0)
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)
            if len(visited) != V:
                self.log_error("V4", f"Case {cid}: Network disconnected before closure ({len(visited)}/{V} reachable)")

            # Check waves
            wave_nums = set(w['wave_no'] for w in waves)
            if not (2 <= len(wave_nums) <= 5):
                self.log_error("V2", f"Case {cid}: Waves count {len(wave_nums)} not in [2, 5]")

            max_wave_size = max(1, E // 4)
            wave_roads = {}
            for w in waves:
                wn = w['wave_no']
                rn = w['road_no']
                if rn not in wave_roads:
                    wave_roads[rn] = []
                wave_roads[rn].append(wn)

            # Check waves are disjoint
            for rn, wlist in wave_roads.items():
                if len(wlist) > 1:
                    self.log_error("V4", f"Case {cid}: Road {rn} closed in multiple waves {wlist}")

            # Check wave sizes
            wave_counts = {}
            for w in waves:
                wn = w['wave_no']
                wave_counts[wn] = wave_counts.get(wn, 0) + 1
            for wn, cnt in wave_counts.items():
                if not (1 <= cnt <= max_wave_size):
                    self.log_error("V4", f"Case {cid}: Wave {wn} has {cnt} roads, not in [1, max(1, E//4)={max_wave_size}]")

    def validate_v5(self):
        for cid, c_data in self.cases_by_id.items():
            c = c_data['cases']
            tier = c['tier']

            # Radio Log parts
            log_rows = c_data.get('radio_log', [])
            parts = [r['part'] for r in log_rows]
            if parts != list(range(1, len(log_rows) + 1)):
                self.log_error("V5", f"Case {cid}: Radio log parts not in consecutive order 1, 2, ...")

            full_log = ""
            for r in log_rows:
                txt = str(r['text'])
                if len(txt) > 10000:
                    self.log_error("V5", f"Case {cid}: Log cell exceeds 10,000 symbols ({len(txt)})")
                full_log += txt

            # Radio Patterns
            pats = c_data.get('radio_patterns', [])
            if len(pats) != 6:
                self.log_error("V5", f"Case {cid}: Must have exactly 6 patterns, found {len(pats)}")
            exp_lens = [2, 4, 8, 12, 20, 40]
            counts = []
            for p_idx, p_entry in enumerate(pats):
                p_str = p_entry['pattern']
                if len(p_str) != exp_lens[p_idx]:
                    self.log_error("V5", f"Case {cid}: Pattern {p_idx} length {len(p_str)} != {exp_lens[p_idx]}")
                # Exact occurrence count with overlaps
                true_cnt = 0
                st = 0
                while True:
                    idx = full_log.find(p_str, st)
                    if idx == -1:
                        break
                    true_cnt += 1
                    st = idx + 1
                if p_entry['count'] != true_cnt:
                    self.log_error("V5", f"Case {cid}: Pattern '{p_str}' reported count {p_entry['count']} != true count {true_cnt}")
                counts.append(true_cnt)

            occ = [cnt for cnt in counts if cnt > 0]
            non_occ = [cnt for cnt in counts if cnt == 0]
            if len(occ) < 2 or len(non_occ) < 1:
                self.log_error("V5", f"Case {cid}: Patterns must have at least 2 occurring and at least 1 non-occurring")

            # Radio reports & edit_bound
            reps = c_data.get('radio_reports', [])
            if reps:
                rep_a = reps[0]['report_a']
                rep_b = reps[0]['report_b']
                true_ed = compute_levenshtein(rep_a, rep_b)
                eb = c['edit_bound']
                if not (true_ed <= eb <= len(rep_a) + len(rep_b)):
                    self.log_error("V5", f"Case {cid}: edit_bound {eb} invalid (true {true_ed}, max {len(rep_a)+len(rep_b)})")

            # Tier S Claims
            if tier == 'S':
                claims_rows = c_data.get('claims', [])
                if not claims_rows:
                    self.log_error("V5", f"Case {cid}: Missing claims row for Tier S")
                else:
                    cl = claims_rows[0]
                    crates = c_data.get('crates', [])
                    cap = c['capacity']
                    wts = [cr['weight'] for cr in crates]
                    vals = [cr['value'] for cr in crates]
                    true_cargo = solve_knapsack(wts, vals, cap)
                    if cl['cargo_opt'] != true_cargo:
                        self.log_error("V5", f"Case {cid}: cargo_opt {cl['cargo_opt']} != true {true_cargo}")

                    wins = [(w['start'], w['finish'], w['value']) for w in c_data.get('windows', [])]
                    true_w_cnt = solve_interval_count(wins)
                    if cl['window_count_opt'] != true_w_cnt:
                        self.log_error("V5", f"Case {cid}: window_count_opt {cl['window_count_opt']} != true {true_w_cnt}")

                    true_w_val = solve_interval_value(wins)
                    if cl['window_value_opt'] != true_w_val:
                        self.log_error("V5", f"Case {cid}: window_value_opt {cl['window_value_opt']} != true {true_w_val}")

                    drum = c_data.get('drum_prices', [])
                    prices = [d['price'] for d in drum]
                    true_drum = solve_rod_cutting(prices, len(drum))
                    if cl['drum_opt'] != true_drum:
                        self.log_error("V5", f"Case {cid}: drum_opt {cl['drum_opt']} != true {true_drum}")

                    sites = [(s['x'], s['y']) for s in c_data.get('sites', [])]
                    true_tour = solve_exact_tsp(sites)
                    if cl['tour_opt'] != true_tour:
                        self.log_error("V5", f"Case {cid}: tour_opt {cl['tour_opt']} != true {true_tour}")

                    s_edges = [(e['u'], e['v']) for e in c_data.get('sensor_edges', [])]
                    n_s_nodes = c['sensor_nodes']
                    true_cover = solve_exact_vertex_cover(n_s_nodes, s_edges)
                    if cl['cover_min'] != true_cover:
                        self.log_error("V5", f"Case {cid}: cover_min {cl['cover_min']} != true {true_cover}")

    def validate_v6(self):
        for cid, c_data in self.cases_by_id.items():
            c = c_data['cases']
            tier = c['tier']

            # Planted Tour
            tour_rows = c_data.get('tour', [])
            sites = c_data.get('sites', [])
            n = len(sites)
            if len(tour_rows) != n:
                self.log_error("V6", f"Case {cid}: Planted tour length {len(tour_rows)} != num sites {n}")
            steps = [t['step'] for t in tour_rows]
            if steps != list(range(n)):
                self.log_error("V6", f"Case {cid}: Tour steps not consecutive")
            tour_perm = [t['site_no'] for t in tour_rows]
            if tour_perm[0] != 0 or set(tour_perm) != set(range(n)):
                self.log_error("V6", f"Case {cid}: Tour must be permutation of sites starting at 0")

            site_coords = {s['site_no']: (s['x'], s['y']) for s in sites}
            calc_tlen = 0
            for i in range(n):
                u = tour_perm[i]
                v = tour_perm[(i + 1) % n]
                calc_tlen += manhattan_dist(site_coords[u], site_coords[v])

            if calc_tlen != c['tour_length']:
                self.log_error("V6", f"Case {cid}: Calculated tour length {calc_tlen} != cases.tour_length {c['tour_length']}")

            if tier in ('L', 'X'):
                nn_len = compute_nn_tour([(s['x'], s['y']) for s in sites])
                if calc_tlen > nn_len:
                    self.log_error("V6", f"Case {cid}: Planted tour {calc_tlen} longer than NN tour {nn_len}")

            # Planted Sensor Cover
            cover_rows = c_data.get('sensor_cover', [])
            k = c['sensor_k']
            if len(cover_rows) != k:
                self.log_error("V6", f"Case {cid}: Planted cover size {len(cover_rows)} != sensor_k {k}")
            cover_set = set(cr['node'] for cr in cover_rows)
            for e in c_data.get('sensor_edges', []):
                if e['u'] not in cover_set and e['v'] not in cover_set:
                    self.log_error("V6", f"Case {cid}: Edge ({e['u']}, {e['v']}) not covered by planted cover")

            # Planted 3-SAT Assignment
            planted_sw = {sp['switch']: sp['value'] for sp in c_data.get('safety_planted', [])}
            for r in c_data.get('safety_rules', []):
                satisfied = False
                for lit in (r['lit_1'], r['lit_2'], r['lit_3']):
                    var = abs(lit)
                    val = planted_sw.get(var, 0)
                    if lit > 0 and val == 1:
                        satisfied = True
                        break
                    elif lit < 0 and val == 0:
                        satisfied = True
                        break
                if not satisfied:
                    self.log_error("V6", f"Case {cid}: Safety rule {r['rule_no']} unsatisfied by planted assignment")

            # Planted Rations
            rat_rows = c_data.get('rations', [])
            sum_planted = sum(r['value'] for r in rat_rows if r['planted'] == 1)
            if sum_planted != c['rations_target']:
                self.log_error("V6", f"Case {cid}: Sum of planted rations {sum_planted} != rations_target {c['rations_target']}")

    def validate_v7(self):
        # Scenario signatures (cases 0 to 45)
        for cid, c_data in self.cases_by_id.items():
            c = c_data['cases']
            k = c['case_no']
            if k >= 46:
                continue
            scen = c['scenario']
            tier = c['tier']
            locs = c_data.get('locations', [])
            roads = c_data.get('roads', [])
            crates = c_data.get('crates', [])
            waves = c_data.get('waves', [])
            V = len(locs)
            E = len(roads)
            avg_deg = (2 * E) / V

            if scen == 1: # Delta Flood
                if not (2.2 <= avg_deg <= 3.2):
                    self.log_error("V7", f"Case {cid} (Scen 1): Avg degree {avg_deg:.2f} not in [2.2, 3.2]")
                pen_ge_2 = sum(1 for l in locs if l['penalty'] >= 2)
                if pen_ge_2 / V < 0.40:
                    self.log_error("V7", f"Case {cid} (Scen 1): Locations with penalty >= 2 ({pen_ge_2/V:.2%}) < 40%")
                num_waves = len(set(w['wave_no'] for w in waves))
                if num_waves < 3:
                    self.log_error("V7", f"Case {cid} (Scen 1): Waves {num_waves} < 3")
                cat_01 = sum(1 for cr in crates if cr['cat'] in (0, 1))
                if cat_01 / len(crates) < 0.55:
                    self.log_error("V7", f"Case {cid} (Scen 1): Food & Water crates ({cat_01/len(crates):.2%}) < 55%")

            elif scen == 2: # Mountain Earthquake
                if not (2.0 <= avg_deg <= 2.6):
                    self.log_error("V7", f"Case {cid} (Scen 2): Avg degree {avg_deg:.2f} not in [2.0, 2.6]")
                cat_23 = sum(1 for cr in crates if cr['cat'] in (2, 3))
                if cat_23 / len(crates) < 0.45:
                    self.log_error("V7", f"Case {cid} (Scen 2): Medicine & Tool crates ({cat_23/len(crates):.2%}) < 45%")
                alarms = c_data.get('incidents', [])
                mean_prio = sum(a['priority'] for a in alarms) / len(alarms)
                if mean_prio < 6.0:
                    self.log_error("V7", f"Case {cid} (Scen 2): Mean alarm priority {mean_prio:.2f} < 6.0")

            elif scen == 3: # Coastal Cyclone
                num_shelters = sum(1 for l in locs if l['type'] == 'S')
                if num_shelters / V < 0.25:
                    self.log_error("V7", f"Case {cid} (Scen 3): Shelter ratio ({num_shelters/V:.2%}) < 25%")
                num_waves = len(set(w['wave_no'] for w in waves))
                if num_waves < 3:
                    self.log_error("V7", f"Case {cid} (Scen 3): Waves {num_waves} < 3")
                wins = c_data.get('windows', [])
                tot_overlaps = 0
                for i in range(len(wins)):
                    for j in range(len(wins)):
                        if i != j:
                            if not (wins[i]['finish'] <= wins[j]['start'] or wins[j]['finish'] <= wins[i]['start']):
                                tot_overlaps += 1
                avg_overlap = tot_overlaps / len(wins)
                if avg_overlap < 2.0:
                    self.log_error("V7", f"Case {cid} (Scen 3): Window avg overlap {avg_overlap:.2f} < 2.0")
                log_syms = set("".join(r['text'] for r in c_data.get('radio_log', [])))
                if len(log_syms) < 30:
                    self.log_error("V7", f"Case {cid} (Scen 3): Log symbols used {len(log_syms)} < 30")

            elif scen == 4: # Urban Flash Flood
                if avg_deg < 3.5:
                    self.log_error("V7", f"Case {cid} (Scen 4): Avg degree {avg_deg:.2f} < 3.5")
                cat_4 = sum(1 for cr in crates if cr['cat'] == 4)
                if cat_4 / len(crates) < 0.10:
                    self.log_error("V7", f"Case {cid} (Scen 4): Rare crates ({cat_4/len(crates):.2%}) < 10%")

            elif scen == 5: # Landslide Corridor
                if avg_deg > 2.4:
                    self.log_error("V7", f"Case {cid} (Scen 5): Avg degree {avg_deg:.2f} > 2.4")
                deg_map = {i: 0 for i in range(V)}
                for r in roads:
                    deg_map[r['u']] += 1
                    deg_map[r['v']] += 1
                if any(d > 4 for d in deg_map.values()):
                    self.log_error("V7", f"Case {cid} (Scen 5): Location with degree > 4 exists")
                # Farthest location from HQ at least floor(V / 4) roads away
                adj = {i: [] for i in range(V)}
                for r in roads:
                    adj[r['u']].append(r['v'])
                    adj[r['v']].append(r['u'])
                dist = {0: 0}
                q = deque([0])
                while q:
                    u = q.popleft()
                    for v in adj[u]:
                        if v not in dist:
                            dist[v] = dist[u] + 1
                            q.append(v)
                max_hops = max(dist.values())
                if max_hops < math.floor(V / 4):
                    self.log_error("V7", f"Case {cid} (Scen 5): Farthest node hops {max_hops} < floor(V/4)={math.floor(V/4)}")
                # Union of waves leaves at least one target unreachable
                closed_union = set(w['road_no'] for w in waves)
                adj_closed = {i: [] for i in range(V)}
                for r in roads:
                    if r['road_no'] not in closed_union:
                        adj_closed[r['u']].append(r['v'])
                        adj_closed[r['v']].append(r['u'])
                reach = {0}
                q = deque([0])
                while q:
                    u = q.popleft()
                    for v in adj_closed[u]:
                        if v not in reach:
                            reach.add(v)
                            q.append(v)
                targets = [c['target_0'], c['target_1'], c['target_2']]
                if all(t in reach for t in targets):
                    self.log_error("V7", f"Case {cid} (Scen 5): Union of waves did not disconnect any target")

            elif scen == 6: # Outbreak Camp
                cat_12 = sum(1 for cr in crates if cr['cat'] in (1, 2))
                if cat_12 / len(crates) < 0.55:
                    self.log_error("V7", f"Case {cid} (Scen 6): Med & Water crates ({cat_12/len(crates):.2%}) < 55%")
                exp_300 = sum(1 for cr in crates if cr['expiry'] <= 300)
                if exp_300 / len(crates) < 0.50:
                    self.log_error("V7", f"Case {cid} (Scen 6): Crates expiring by 300 ({exp_300/len(crates):.2%}) < 50%")
                log_txt = "".join(r['text'] for r in c_data.get('radio_log', []))
                char_counts = {}
                for ch in log_txt:
                    char_counts[ch] = char_counts.get(ch, 0) + 1
                max_sym_ratio = max(char_counts.values()) / len(log_txt)
                if max_sym_ratio < 0.25:
                    self.log_error("V7", f"Case {cid} (Scen 6): Dominant symbol ratio {max_sym_ratio:.2%} < 25%")

        # Variety rules
        # 1. In at least 5 Tier S cases, greedy knapsack is not optimal
        greedy_fail_cnt = 0
        for k in range(20):
            cid = f"{self.raw_data['cases'][k]['group_seed']}-{k:02d}"
            c_data = self.cases_by_id[cid]
            crates = c_data.get('crates', [])
            cap = c_data['cases']['capacity']
            wts = [cr['weight'] for cr in crates]
            vals = [cr['value'] for cr in crates]
            opt = solve_knapsack(wts, vals, cap)
            gr = solve_greedy_knapsack(wts, vals, cap)
            if gr < opt:
                greedy_fail_cnt += 1
        if greedy_fail_cnt < 5:
            self.log_error("V7", f"Variety 1: Greedy knapsack failed in {greedy_fail_cnt} cases, expected >= 5")

        # 2. In at least 5 Tier S cases, BFS fewest roads costs more than Dijkstra cheapest route
        bfs_fail_cnt = 0
        for k in range(20):
            cid = f"{self.raw_data['cases'][k]['group_seed']}-{k:02d}"
            c_data = self.cases_by_id[cid]
            locs = c_data.get('locations', [])
            roads = c_data.get('roads', [])
            V = len(locs)
            pen_map = {l['loc_id']: l['penalty'] for l in locs}
            # Directed step cost u -> v: minutes + penalty(v)
            adj = {i: [] for i in range(V)}
            for r in roads:
                adj[r['u']].append((r['v'], r['minutes'] + pen_map[r['v']]))
                adj[r['v']].append((r['u'], r['minutes'] + pen_map[r['u']]))

            # Dijkstra from 0
            import heapq
            dist = {i: float('inf') for i in range(V)}
            dist[0] = 0
            pq = [(0, 0)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                for v, cost in adj[u]:
                    if dist[u] + cost < dist[v]:
                        dist[v] = dist[u] + cost
                        heapq.heappush(pq, (dist[v], v))

            # BFS unweighted shortest path (fewest roads)
            # Find min hop count and min cost among paths with fewest roads
            t0 = c_data['cases']['target_0']
            q = deque([(0, [0])])
            min_hops = None
            fewest_road_paths = []
            while q:
                u, path = q.popleft()
                if min_hops is not None and len(path) - 1 > min_hops:
                    break
                if u == t0:
                    if min_hops is None:
                        min_hops = len(path) - 1
                    fewest_road_paths.append(path)
                    continue
                for v, _ in adj[u]:
                    if v not in path:
                        q.append((v, path + [v]))

            if fewest_road_paths:
                costs = []
                for p in fewest_road_paths:
                    p_cost = 0
                    for i_p in range(len(p) - 1):
                        u_p, v_p = p[i_p], p[i_p + 1]
                        # find edge minutes
                        for r in roads:
                            if (r['u'] == u_p and r['v'] == v_p) or (r['u'] == v_p and r['v'] == u_p):
                                p_cost += r['minutes'] + pen_map[v_p]
                                break
                    costs.append(p_cost)
                if min(costs) > dist[t0]:
                    bfs_fail_cnt += 1
        if bfs_fail_cnt < 5:
            self.log_error("V7", f"Variety 2: BFS path more expensive in {bfs_fail_cnt} Tier S cases, expected >= 5")

        # 3. Across 26 cases of M & L: rules/switches in [2.5, 6.0], >=5 <3.5, >=8 in [3.5, 4.8], >=5 >4.8
        ml_ratios = []
        for k in range(20, 46):
            cid = f"{self.raw_data['cases'][k]['group_seed']}-{k:02d}"
            c_data = self.cases_by_id[cid]
            rules = c_data.get('safety_rules', [])
            n_vars = c_data['cases']['safety_vars']
            rat = len(rules) / n_vars
            ml_ratios.append(rat)

        cnt_low = sum(1 for r in ml_ratios if r < 3.5)
        cnt_mid = sum(1 for r in ml_ratios if 3.5 <= r <= 4.8)
        cnt_high = sum(1 for r in ml_ratios if r > 4.8)
        if cnt_low < 5 or cnt_mid < 8 or cnt_high < 5:
            self.log_error("V7", f"Variety 3: 3-SAT ratios: <3.5: {cnt_low} (exp >=5), [3.5, 4.8]: {cnt_mid} (exp >=8), >4.8: {cnt_high} (exp >=5)")

    def validate_v8(self):
        # Case 46: Monotone in at least 3 of 5 fields
        c46_id = f"{self.raw_data['cases'][46]['group_seed']}-46"
        c46 = self.cases_by_id[c46_id]
        crates46 = c46.get('crates', [])
        fields = {
            'value': [c['value'] for c in crates46],
            'weight': [c['weight'] for c in crates46],
            'expiry': [c['expiry'] for c in crates46],
            'serial': [c['serial'] for c in crates46],
            'value_per_kg': [c['value'] / c['weight'] for c in crates46]
        }
        mono_cnt = 0
        for f_name, vals in fields.items():
            non_dec = all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))
            non_inc = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
            if non_dec or non_inc:
                mono_cnt += 1
        if mono_cnt < 3:
            self.log_error("V8", f"Case 46: Monotone in {mono_cnt} fields, expected >= 3")

        # Case 47: Greedy reaches at most 60% of optimum
        c47_id = f"{self.raw_data['cases'][47]['group_seed']}-47"
        c47 = self.cases_by_id[c47_id]
        crates47 = c47.get('crates', [])
        cap47 = c47['cases']['capacity']
        wts47 = [c['weight'] for c in crates47]
        vals47 = [c['value'] for c in crates47]
        opt47 = solve_knapsack(wts47, vals47, cap47)
        gr47 = solve_greedy_knapsack(wts47, vals47, cap47)
        ratio47 = gr47 / opt47 if opt47 > 0 else 1.0
        if ratio47 > 0.60:
            self.log_error("V8", f"Case 47: Greedy achieved {ratio47:.2%} of optimum, expected <= 60%")

        # Case 48: Longest distance >= 500 roads; fewest roads cost >= 1.5x cheapest
        c48_id = f"{self.raw_data['cases'][48]['group_seed']}-48"
        c48 = self.cases_by_id[c48_id]
        locs48 = c48.get('locations', [])
        roads48 = c48.get('roads', [])
        V48 = len(locs48)
        adj48 = {i: [] for i in range(V48)}
        pen48 = {l['loc_id']: l['penalty'] for l in locs48}
        for r in roads48:
            adj48[r['u']].append((r['v'], r['minutes'] + pen48[r['v']]))
            adj48[r['v']].append((r['u'], r['minutes'] + pen48[r['u']]))

        # BFS hop count from node 4 (end of chain)
        dist_hops = {4: 0}
        q = deque([4])
        while q:
            u = q.popleft()
            for v, _ in adj48[u]:
                if v not in dist_hops:
                    dist_hops[v] = dist_hops[u] + 1
                    q.append(v)
        if max(dist_hops.values()) < 500:
            self.log_error("V8", f"Case 48: Longest shortest path {max(dist_hops.values())} < 500 roads")

        # Target 0 check
        t0 = c48['cases']['target_0']
        # Dijkstra
        import heapq
        d_cost = {i: float('inf') for i in range(V48)}
        d_cost[0] = 0
        pq = [(0, 0)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > d_cost[u]:
                continue
            for v, cst in adj48[u]:
                if d_cost[u] + cst < d_cost[v]:
                    d_cost[v] = d_cost[u] + cst
                    heapq.heappush(pq, (d_cost[v], v))

        # BFS for target 0
        q = deque([(0, [0])])
        min_hops = None
        fewest_paths = []
        while q:
            u, path = q.popleft()
            if min_hops is not None and len(path) - 1 > min_hops:
                break
            if u == t0:
                if min_hops is None:
                    min_hops = len(path) - 1
                fewest_paths.append(path)
                continue
            for v, _ in adj48[u]:
                if v not in path:
                    q.append((v, path + [v]))

        fewest_costs = []
        for p in fewest_paths:
            cst = 0
            for ip in range(len(p) - 1):
                up, vp = p[ip], p[ip + 1]
                for r in roads48:
                    if (r['u'] == up and r['v'] == vp) or (r['u'] == vp and r['v'] == up):
                        cst += r['minutes'] + pen48[vp]
                        break
            fewest_costs.append(cst)
        
        min_fewest_cost = min(fewest_costs)
        if min_fewest_cost < 1.5 * d_cost[t0]:
            self.log_error("V8", f"Case 48: Fewest roads cost {min_fewest_cost} < 1.5x cheapest {d_cost[t0]}")

        # Case 49: Near-miss trap
        c49_id = f"{self.raw_data['cases'][49]['group_seed']}-49"
        c49 = self.cases_by_id[c49_id]
        log_txt49 = "".join(r['text'] for r in c49.get('radio_log', []))
        if len(log_txt49) < 50000:
            self.log_error("V8", f"Case 49: Log symbols {len(log_txt49)} < 50,000")
        
        # Check repetition of block of <= 8 symbols
        # Count dominant 1-char repetition
        ch_cnt = {}
        for ch in log_txt49:
            ch_cnt[ch] = ch_cnt.get(ch, 0) + 1
        if max(ch_cnt.values()) / len(log_txt49) < 0.90:
            self.log_error("V8", f"Case 49: Dominant block repetition < 90%")

        # Check at least 4 patterns have length - 1 prefix matching >= 50% start positions
        pats49 = c49.get('radio_patterns', [])
        pref_match_cnt = 0
        N = len(log_txt49)
        for p_entry in pats49:
            p = p_entry['pattern']
            pref = p[:-1]
            # Match prefix against log
            m_cnt = 0
            for st in range(N - len(pref) + 1):
                if log_txt49[st:st + len(pref)] == pref:
                    m_cnt += 1
            if m_cnt / (N - len(pref) + 1) >= 0.50:
                pref_match_cnt += 1
        if pref_match_cnt < 4:
            self.log_error("V8", f"Case 49: Only {pref_match_cnt} patterns have prefix match >= 50%, expected >= 4")

    def run_all(self):
        print(f"Running validator on {self.filepath}...")
        if not self.load_workbook():
            return False, self.errors

        self.build_case_indexes()
        self.validate_v1()
        self.validate_v2_and_v3()
        self.validate_v4()
        self.validate_v5()
        self.validate_v6()
        self.validate_v7()
        self.validate_v8()

        if self.errors:
            print(f"FAILED! Found {len(self.errors)} error(s):")
            for err in self.errors[:20]:
                print(f"  {err}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors.")
            return False, self.errors
        else:
            print("PASS! All 50 cases strictly comply with V1 through V8.")
            return True, []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        target = 'cases.xlsx'
    else:
        target = sys.argv[1]
    val = Validator(target)
    success, _ = val.run_all()
    sys.exit(0 if success else 1)

