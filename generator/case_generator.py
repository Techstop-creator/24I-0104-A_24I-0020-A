"""
Case Generator Implementation (Refined & Fully Compliant)
Generates all 50 cases strictly according to the LIFELINE specification.
"""

import random
import math
import itertools
from collections import deque
from algorithms import (
    ALPHABET, get_tier, get_scenario,
    compute_edit_distance, solve_knapsack, solve_greedy_knapsack,
    solve_interval_count, solve_interval_value, solve_rod_cutting,
    solve_exact_tsp, solve_exact_vertex_cover, compute_nn_tour_length,
    manhattan_dist
)

def generate_case(group_seed, case_no):
    rng = random.Random(group_seed * 1000 + case_no)
    tier = get_tier(case_no)
    scenario = get_scenario(case_no)
    case_id = f"{group_seed}-{case_no:02d}"

    data = {
        'case_id': case_id,
        'group_seed': group_seed,
        'case_no': case_no,
        'tier': tier,
        'scenario': scenario,
    }

    # =========================================================================
    # 1. CRATES & CAPACITY
    # =========================================================================
    if case_no == 46: # Trap 46: 1500 to 3000 crates, monotone in >=3 fields
        num_crates = 1600
        crates = []
        base_serial = 10000000 + rng.randint(0, 10000000)
        for i in range(1, num_crates + 1):
            val = min(100, 10 + (i * 90) // num_crates)
            exp = min(999, (i * 999) // num_crates)
            ser = base_serial + i
            crates.append({
                'case_id': case_id, 'crate_id': i, 'cat': rng.choice([0, 1, 2, 3, 4]),
                'weight': 10, 'value': val, 'expiry': exp, 'serial': ser
            })
    elif case_no == 47: # Trap 47: 12 to 60 crates, greedy reaches <= 60% of optimum
        num_crates = 12
        crates = [
            {'case_id': case_id, 'crate_id': 1, 'cat': 2, 'weight': 11, 'value': 55, 'expiry': 200, 'serial': 12345670},
            {'case_id': case_id, 'crate_id': 2, 'cat': 1, 'weight': 10, 'value': 48, 'expiry': 250, 'serial': 12345671},
            {'case_id': case_id, 'crate_id': 3, 'cat': 2, 'weight': 10, 'value': 48, 'expiry': 280, 'serial': 12345672},
        ]
        base_ser = 12345680
        for i in range(4, num_crates + 1):
            crates.append({
                'case_id': case_id, 'crate_id': i, 'cat': rng.choice([1, 2]),
                'weight': 10, 'value': 10, 'expiry': rng.randint(50, 290), 'serial': base_ser + i
            })
    else:
        if tier == 'S':
            num_crates = 10 if case_no in [0, 1, 2, 3, 4, 5] else rng.randint(8, 20)
        elif tier == 'M':
            num_crates = rng.randint(40, 90)
        else: # L or X (48, 49)
            num_crates = rng.randint(500, 700)

        serials = set()
        crates = []
        for i in range(1, num_crates + 1):
            while True:
                ser = rng.randint(10000000, 99999999)
                if ser not in serials:
                    serials.add(ser)
                    break
            
            w = rng.randint(1, 20)
            v = rng.randint(10, 100)
            exp = rng.randint(0, 999)
            crates.append({
                'case_id': case_id, 'crate_id': i, 'cat': 0,
                'weight': w, 'value': v, 'expiry': exp, 'serial': ser
            })

        # Apply Scenario signatures on crates
        if case_no < 46:
            if scenario == 1: # Delta Flood: cat 0, 1 >= 55%
                req_cnt = int(math.ceil(0.60 * num_crates))
                for i in range(req_cnt):
                    crates[i]['cat'] = rng.choice([0, 1])
                for i in range(req_cnt, num_crates):
                    crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])
            elif scenario == 2: # Mountain Earthquake: cat 2, 3 >= 45%
                req_cnt = int(math.ceil(0.50 * num_crates))
                for i in range(req_cnt):
                    crates[i]['cat'] = rng.choice([2, 3])
                for i in range(req_cnt, num_crates):
                    crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])
            elif scenario == 4: # Urban Flash Flood: Rare crates (cat 4) >= 10%
                req_cnt = max(1, int(math.ceil(0.15 * num_crates)))
                for i in range(req_cnt):
                    crates[i]['cat'] = 4
                for i in range(req_cnt, num_crates):
                    crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])
            elif scenario == 6: # Outbreak Camp: cat 1, 2 >= 55%, >= 50% expire <= 300
                req_cnt = int(math.ceil(0.60 * num_crates))
                for i in range(req_cnt):
                    crates[i]['cat'] = rng.choice([1, 2])
                for i in range(req_cnt, num_crates):
                    crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])
                exp_cnt = int(math.ceil(0.55 * num_crates))
                for i in range(exp_cnt):
                    crates[i]['expiry'] = rng.randint(0, 300)
            else:
                for i in range(num_crates):
                    crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])
        else:
            for i in range(num_crates):
                crates[i]['cat'] = rng.choice([0, 1, 2, 3, 4])

        # Variety Rule 1: In at least 5 Tier S cases, greedy knapsack is NOT optimal
        if tier == 'S' and case_no in [0, 1, 2, 3, 4, 5]:
            crates[0]['weight'] = 11
            crates[0]['value'] = 55
            crates[1]['weight'] = 10
            crates[1]['value'] = 48
            crates[2]['weight'] = 10
            crates[2]['value'] = 48
            for idx in range(3, len(crates)):
                crates[idx]['weight'] = 10
                crates[idx]['value'] = 10

    total_weight = sum(c['weight'] for c in crates)
    if case_no == 47 or (tier == 'S' and case_no in [0, 1, 2, 3, 4, 5]):
        capacity = 20
    else:
        capacity = max(1, int(total_weight * rng.uniform(0.25, 0.50)))

    data['crates'] = crates
    data['capacity'] = capacity

    # =========================================================================
    # 2. LOCATIONS & ROADS & WAVES
    # =========================================================================
    if case_no == 48: # Trap 48: 1500 to 3000 locations, longest dist >= 500 roads
        V = 1600
    elif tier == 'S':
        V = rng.randint(8, 12)
    elif tier == 'M':
        V = rng.randint(35, 60)
    else: # L or X
        V = rng.randint(500, 650)

    locations = [{'case_id': case_id, 'loc_id': 0, 'type': 'D', 'penalty': 0}]
    for i in range(1, V):
        locations.append({'case_id': case_id, 'loc_id': i, 'type': 'J', 'penalty': 0})

    # Location type signatures
    if case_no < 46 and scenario == 3: # Coastal Cyclone: >= 25% shelters
        shelter_cnt = int(math.ceil(0.32 * V))
        for i in range(1, shelter_cnt + 1):
            locations[i]['type'] = 'S'
        locations[shelter_cnt + 1]['type'] = 'H'
        for i in range(shelter_cnt + 2, V):
            locations[i]['type'] = rng.choice(['H', 'J'])
    else:
        # Guarantee at least one S and one H
        locations[1]['type'] = 'S'
        locations[2]['type'] = 'H'
        for i in range(3, V):
            locations[i]['type'] = rng.choice(['S', 'H', 'J'])

    # Penalties
    if case_no < 46 and scenario == 1: # Delta Flood: at least 40% penalty >= 2
        pen_cnt = int(math.ceil(0.48 * V))
        for i in range(1, pen_cnt + 1):
            locations[i]['penalty'] = rng.choice([2, 4, 6])
        for i in range(pen_cnt + 1, V):
            locations[i]['penalty'] = rng.choice([0, 1])
    else:
        for i in range(1, V):
            locations[i]['penalty'] = rng.choice([0, 1, 2, 4, 6])

    # Distinct targets S or H, not HQ
    if case_no == 48:
        locations[1]['type'] = 'S'
        locations[2]['type'] = 'H'
        locations[3]['type'] = 'S'
        target_0, target_1, target_2 = 1, 2, 3
    else:
        cand_targets = [l['loc_id'] for l in locations if l['loc_id'] != 0 and l['type'] in ('S', 'H')]
        if len(cand_targets) < 3:
            locations[1]['type'] = 'S'
            locations[2]['type'] = 'H'
            locations[3]['type'] = 'S'
            cand_targets = [1, 2, 3]
        targets = rng.sample(cand_targets, 3)
        target_0, target_1, target_2 = targets[0], targets[1], targets[2]

    # ROADS GENERATION
    roads = []
    road_set = set()
    def add_edge(u, v, mins, cable):
        if u > v:
            u, v = v, u
        if u != v and (u, v) not in road_set:
            road_set.add((u, v))
            roads.append({
                'case_id': case_id, 'road_no': len(roads),
                'u': u, 'v': v, 'minutes': mins, 'cable': cable
            })

    if case_no == 48:
        # Long backbone line: 4 -> 5 -> ... -> 604 (600 edges, length 600 >= 500)
        for i in range(4, 604):
            add_edge(i, i + 1, rng.randint(1, 10), rng.randint(1, 50))
        add_edge(0, 4, 5, 20)
        
        # Target 0: Fewest roads route costs >= 1.5x cheapest route
        locations[target_0]['penalty'] = 6
        add_edge(0, target_0, 60, 90) # cost = 66
        locations[2]['penalty'] = 0
        locations[3]['penalty'] = 0
        add_edge(0, 2, 1, 10)
        add_edge(2, 3, 1, 10)
        add_edge(3, target_0, 1, 10) # cost = 1 + 0 + 1 + 0 + 1 + 6 = 9
        
        # Connect remaining nodes directly to node 2
        for i in range(1, V):
            if i not in (target_0, 2, 3) and not (4 <= i <= 604):
                add_edge(2, i, rng.randint(1, 30), rng.randint(1, 50))
    elif case_no < 46 and scenario == 5: # Landslide Corridor
        # Max degree <= 4, Avg degree <= 2.4, farthest from HQ >= floor(V/4)
        spine_len = max(math.floor(V / 4) + 5, 5)
        deg = {i: 0 for i in range(V)}
        for i in range(spine_len - 1):
            add_edge(i, i + 1, rng.randint(5, 25), rng.randint(10, 50))
            deg[i] += 1
            deg[i + 1] += 1
        
        # Attach remaining nodes to nodes with degree < 3 to ensure max degree <= 3 (strictly <= 4)
        avail = deque([i for i in range(spine_len) if deg[i] < 3])
        for i in range(spine_len, V):
            parent = avail[0]
            add_edge(parent, i, rng.randint(5, 25), rng.randint(10, 50))
            deg[parent] += 1
            deg[i] = 1
            if deg[parent] >= 3:
                avail.popleft()
            avail.append(i)
    else:
        # Spanning tree
        p = list(range(V))
        rng.shuffle(p)
        for i in range(1, V):
            u = p[i]
            v = p[rng.randint(0, i - 1)]
            add_edge(u, v, rng.randint(5, 30), rng.randint(10, 50))
        
        # Variety Rule 2 for Tier S
        if tier == 'S' and case_no in [0, 1, 2, 3, 4, 5]:
            locations[target_0]['penalty'] = 6
            add_edge(0, target_0, 60, 80)
            junc = [x for x in range(1, V) if x not in (target_0, target_1, target_2)][0]
            locations[junc]['penalty'] = 0
            add_edge(0, junc, 1, 10)
            add_edge(junc, target_0, 1, 10)

        # Target number of edges
        if case_no < 46 and scenario == 1: # Delta Flood: avg deg in [2.2, 3.2] -> E in [1.15 V, 1.55 V]
            target_E = int(math.ceil(V * rng.uniform(1.20, 1.50)))
        elif case_no < 46 and scenario == 2: # Mountain Earthquake: avg deg in [2.0, 2.6]
            target_E = int(math.ceil(V * rng.uniform(1.05, 1.25)))
        elif case_no < 46 and scenario == 4: # Urban Flash Flood: avg deg >= 3.5 -> E >= 1.80 V
            target_E = int(math.ceil(V * rng.uniform(1.85, 2.30)))
        else:
            target_E = int(math.ceil(V * rng.uniform(1.10, 1.50)))

        target_E = min(target_E, 3 * V)
        target_E = max(target_E, V - 1)

        attempts = 0
        while len(roads) < target_E and attempts < 20000:
            attempts += 1
            u = rng.randint(0, V - 1)
            v = rng.randint(0, V - 1)
            if u != v:
                add_edge(u, v, rng.randint(5, 45), rng.randint(10, 80))

    E = len(roads)
    # Closure Waves (2 to 5 waves)
    num_waves = rng.randint(3, 5) if (case_no < 46 and scenario in (1, 3, 5)) else rng.randint(2, 5)
    max_wave_size = max(1, E // 4)

    # Disjoint waves
    all_roads_perm = list(range(E))
    rng.shuffle(all_roads_perm)

    waves = []
    used_roads = set()
    r_ptr = 0

    if case_no < 46 and scenario == 5:
        # Union of all waves must leave at least one target unreachable from HQ
        target_0_incident = [r['road_no'] for r in roads if r['u'] == target_0 or r['v'] == target_0]
        used_roads = set()
        pool = [r for r in all_roads_perm if r not in target_0_incident]
        p_ptr = 0
        for w_idx in range(1, num_waves + 1):
            w_size = rng.randint(1, max_wave_size)
            w_roads = []
            if target_0_incident:
                r_inc = target_0_incident.pop()
                w_roads.append(r_inc)
                used_roads.add(r_inc)
            while len(w_roads) < w_size and p_ptr < len(pool):
                cand = pool[p_ptr]
                p_ptr += 1
                if cand not in used_roads:
                    used_roads.add(cand)
                    w_roads.append(cand)
            for r_no in w_roads:
                waves.append({'case_id': case_id, 'wave_no': w_idx, 'road_no': r_no})
    else:
        for w_idx in range(1, num_waves + 1):
            w_size = rng.randint(1, max_wave_size)
            for _ in range(w_size):
                while r_ptr < len(all_roads_perm):
                    cand = all_roads_perm[r_ptr]
                    r_ptr += 1
                    if cand not in used_roads:
                        used_roads.add(cand)
                        waves.append({'case_id': case_id, 'wave_no': w_idx, 'road_no': cand})
                        break

    data['locations'] = locations
    data['roads'] = roads
    data['waves'] = waves
    data['target_0'] = target_0
    data['target_1'] = target_1
    data['target_2'] = target_2

    # =========================================================================
    # 3. RADIO LOG, PATTERNS & REPORTS
    # =========================================================================
    if case_no == 49:
        log_len = 60000
        log_text = "A" * log_len
        pat_specs = ["AB", "AAAB", "AAAAAAAB", "AAAAAAAAAAAB", "A" * 20, "A" * 40]
    else:
        if tier == 'S':
            log_len = rng.randint(200, 450)
        elif tier == 'M':
            log_len = rng.randint(2000, 4000)
        else:
            log_len = rng.randint(20000, 30000)

        if case_no < 46 and scenario == 3: # Coastal Cyclone: uses at least 30 symbols
            syms_32 = list(ALPHABET[:34])
            chars = [rng.choice(syms_32) for _ in range(log_len)]
            for s_idx, s in enumerate(syms_32):
                chars[s_idx] = s
            log_text = "".join(chars)
        elif case_no < 46 and scenario == 6: # Outbreak Camp: one symbol >= 25%
            dom_sym = rng.choice(ALPHABET)
            chars = [dom_sym if rng.random() < 0.32 else rng.choice(ALPHABET) for _ in range(log_len)]
            log_text = "".join(chars)
        else:
            log_text = "".join(rng.choice(ALPHABET) for _ in range(log_len))

        pat_specs = []
        lengths = [2, 4, 8, 12, 20, 40]
        idx1 = rng.randint(0, log_len - 2)
        pat_specs.append(log_text[idx1:idx1 + 2])
        idx2 = rng.randint(0, log_len - 4)
        pat_specs.append(log_text[idx2:idx2 + 4])
        for l in lengths[2:-1]:
            idx = rng.randint(0, log_len - l)
            pat_specs.append(log_text[idx:idx + l])
        pat_specs.append("---___---___---___---___---___---___----")

    radio_log_rows = []
    chunk_size = 8000
    for p_idx in range(0, len(log_text), chunk_size):
        radio_log_rows.append({
            'case_id': case_id,
            'part': (p_idx // chunk_size) + 1,
            'text': log_text[p_idx:p_idx + chunk_size]
        })
    data['radio_log'] = radio_log_rows

    radio_patterns = []
    for p_no, p_str in enumerate(pat_specs):
        count = 0
        start = 0
        while True:
            pos = log_text.find(p_str, start)
            if pos == -1:
                break
            count += 1
            start = pos + 1
        radio_patterns.append({
            'case_id': case_id, 'pattern_no': p_no, 'pattern': p_str, 'count': count
        })
    data['radio_patterns'] = radio_patterns

    # Radio Reports
    if tier == 'S':
        rep_len = rng.randint(12, 25)
    elif tier == 'M':
        rep_len = rng.randint(40, 90)
    else:
        rep_len = rng.randint(210, 300)

    rep_a = "".join(rng.choice(ALPHABET) for _ in range(rep_len))
    chars_b = list(rep_a)
    mutations = max(2, rep_len // 5)
    for _ in range(mutations):
        m_type = rng.choice(['ins', 'del', 'rep'])
        pos = rng.randint(0, len(chars_b) - 1)
        if m_type == 'rep':
            chars_b[pos] = rng.choice(ALPHABET)
        elif m_type == 'del' and len(chars_b) > 5:
            chars_b.pop(pos)
        elif m_type == 'ins':
            chars_b.insert(pos, rng.choice(ALPHABET))
    rep_b = "".join(chars_b)

    true_dist = compute_edit_distance(rep_a, rep_b)
    edit_bound = true_dist + rng.randint(0, 5)
    data['radio_reports'] = [{'case_id': case_id, 'report_a': rep_a, 'report_b': rep_b}]
    data['edit_bound'] = edit_bound

    # =========================================================================
    # 4. WINDOWS & INCIDENTS
    # =========================================================================
    if tier == 'S':
        num_windows = rng.randint(8, 16)
        num_alarms = rng.randint(12, 35)
    elif tier == 'M':
        num_windows = rng.randint(60, 150)
        num_alarms = rng.randint(250, 600)
    else:
        num_windows = rng.randint(1050, 1400)
        num_alarms = rng.randint(2100, 3000)

    windows = []
    if case_no < 46 and scenario == 3: # Coastal Cyclone: overlap >= 2.0
        # Windows 1 & 2 touch at 200, Windows 3 & 4 touch at 350 (touching requirement)
        # Windows 2..N heavily overlap in [220, 380] guaranteeing average overlap >= 2.0
        windows.append({'case_id': case_id, 'window_id': 1, 'start': 100, 'finish': 200, 'value': rng.randint(10, 80)})
        windows.append({'case_id': case_id, 'window_id': 2, 'start': 200, 'finish': 400, 'value': rng.randint(10, 80)})
        windows.append({'case_id': case_id, 'window_id': 3, 'start': 250, 'finish': 350, 'value': rng.randint(10, 80)})
        windows.append({'case_id': case_id, 'window_id': 4, 'start': 350, 'finish': 500, 'value': rng.randint(10, 80)})
        for w_id in range(5, num_windows + 1):
            s = rng.randint(210, 240)
            dur = rng.randint(60, 150)
            f = min(1440, s + dur)
            val = rng.randint(1, 100)
            windows.append({'case_id': case_id, 'window_id': w_id, 'start': s, 'finish': f, 'value': val})
    else:
        for w_id in range(1, num_windows + 1):
            dur = rng.randint(15, 120)
            if w_id == 2:
                s = windows[0]['finish']
            elif w_id == 4:
                s = windows[2]['finish']
            else:
                s = rng.randint(0, 1440 - dur)
            f = min(1440, s + dur)
            val = rng.randint(1, 100)
            windows.append({'case_id': case_id, 'window_id': w_id, 'start': s, 'finish': f, 'value': val})
    data['windows'] = windows

    # Incidents
    incidents = []
    if tier in ('M', 'L', 'X'):
        last_tick = int(num_alarms / 1.5) - 1
        ticks = sorted([rng.randint(0, last_tick) for _ in range(num_alarms)])
        ticks[0] = 0
        ticks[-1] = last_tick
    else:
        cur_tick = 0
        ticks = []
        for _ in range(num_alarms):
            if rng.random() < 0.6:
                cur_tick += rng.randint(0, 2)
            ticks.append(cur_tick)

    prios = []
    for a_id in range(1, num_alarms + 1):
        if case_no < 46 and scenario == 2: # Mountain Earthquake: mean priority >= 6.0
            prio = rng.choice([7, 8, 9, 10, 10, rng.randint(6, 10)])
        else:
            prio = rng.randint(1, 10)
        prios.append(prio)

    if tier in ('M', 'L', 'X'):
        prios[0] = 1
        prios[1] = 2
        prios[2] = 4
        prios[3] = 6
        prios[4] = 8
        prios[5] = 10

    for a_id in range(1, num_alarms + 1):
        incidents.append({
            'case_id': case_id, 'alarm_id': a_id, 'tick': ticks[a_id - 1], 'priority': prios[a_id - 1]
        })
    data['incidents'] = incidents

    # =========================================================================
    # 5. SITES & PLANTED TOUR
    # =========================================================================
    if tier == 'S':
        num_sites = rng.randint(5, 8)
    elif tier == 'M':
        num_sites = rng.randint(10, 15)
    else:
        num_sites = rng.randint(200, 280)

    site_coords = set()
    sites = []
    for s_no in range(num_sites):
        while True:
            coord = (rng.randint(0, 999), rng.randint(0, 999))
            if coord not in site_coords:
                site_coords.add(coord)
                sites.append({'case_id': case_id, 'site_no': s_no, 'x': coord[0], 'y': coord[1]})
                break
    data['sites'] = sites

    coords_list = [(s['x'], s['y']) for s in sites]
    if tier in ('L', 'X'):
        # NN tour as planted tour
        visited = [False] * num_sites
        visited[0] = True
        perm = [0]
        cur = 0
        for _ in range(num_sites - 1):
            best_d = float('inf')
            best_nxt = -1
            for nxt in range(num_sites):
                if not visited[nxt]:
                    d = manhattan_dist(coords_list[cur], coords_list[nxt])
                    if d < best_d:
                        best_d = d
                        best_nxt = nxt
            visited[best_nxt] = True
            perm.append(best_nxt)
            cur = best_nxt
    else:
        other_sites = list(range(1, num_sites))
        rng.shuffle(other_sites)
        perm = [0] + other_sites

    t_len = 0
    for i in range(num_sites):
        u_node = perm[i]
        v_node = perm[(i + 1) % num_sites]
        t_len += manhattan_dist(coords_list[u_node], coords_list[v_node])

    tour_rows = [{'case_id': case_id, 'step': idx, 'site_no': s_node} for idx, s_node in enumerate(perm)]
    data['tour'] = tour_rows
    data['tour_length'] = t_len

    # =========================================================================
    # 6. PIPELINE DIMS & DRUM PRICES
    # =========================================================================
    if tier == 'S':
        num_stages = rng.randint(4, 8)
        drum_L = rng.randint(6, 12)
    elif tier == 'M':
        num_stages = rng.randint(18, 45)
        drum_L = rng.randint(45, 120)
    else:
        num_stages = rng.randint(105, 180)
        drum_L = rng.randint(520, 800)

    dims = [rng.randint(2, 100) for _ in range(num_stages + 1)]
    pipeline_rows = [{'case_id': case_id, 'idx': i, 'dim': d} for i, d in enumerate(dims)]
    data['pipeline_dims'] = pipeline_rows

    drum_rows = []
    base_rate = rng.randint(5, 15)
    for j in range(1, drum_L + 1):
        p = min(500, max(1, j * base_rate + (rng.randint(-5, 15) if j % 3 == 0 else 0)))
        drum_rows.append({'case_id': case_id, 'length': j, 'price': p})
    data['drum_prices'] = drum_rows

    # =========================================================================
    # 7. SENSOR EDGES & PLANTED COVER
    # =========================================================================
    if tier == 'S':
        num_sensor_nodes = rng.randint(6, 10)
    elif tier == 'M':
        num_sensor_nodes = rng.randint(22, 35)
    else:
        num_sensor_nodes = rng.randint(110, 180)

    sensor_k = rng.randint(2, num_sensor_nodes // 2)
    planted_cover = set(rng.sample(range(num_sensor_nodes), sensor_k))

    sensor_edges = []
    s_edge_set = set()
    cover_list = list(planted_cover)
    non_cover = [x for x in range(num_sensor_nodes) if x not in planted_cover]

    for u in non_cover:
        c = rng.choice(cover_list)
        edge = (min(u, c), max(u, c))
        s_edge_set.add(edge)
        sensor_edges.append({'case_id': case_id, 'u': edge[0], 'v': edge[1]})

    for i in range(len(cover_list) - 1):
        edge = (min(cover_list[i], cover_list[i + 1]), max(cover_list[i], cover_list[i + 1]))
        if edge not in s_edge_set:
            s_edge_set.add(edge)
            sensor_edges.append({'case_id': case_id, 'u': edge[0], 'v': edge[1]})

    for _ in range(num_sensor_nodes):
        c = rng.choice(cover_list)
        other = rng.randint(0, num_sensor_nodes - 1)
        if c != other:
            edge = (min(c, other), max(c, other))
            if edge not in s_edge_set:
                s_edge_set.add(edge)
                sensor_edges.append({'case_id': case_id, 'u': edge[0], 'v': edge[1]})

    data['sensor_nodes'] = num_sensor_nodes
    data['sensor_k'] = sensor_k
    data['sensor_edges'] = sensor_edges
    data['sensor_cover'] = [{'case_id': case_id, 'node': nd} for nd in sorted(planted_cover)]

    # =========================================================================
    # 8. SAFETY RULES & PLANTED ASSIGNMENT
    # =========================================================================
    if tier == 'S':
        num_safety_vars = rng.randint(6, 12)
        ratio = rng.uniform(2.5, 4.5)
    elif tier == 'M':
        num_safety_vars = rng.randint(22, 35)
        if 20 <= case_no <= 25:
            ratio = rng.uniform(2.6, 3.3) # < 3.5 (6 cases)
        elif 26 <= case_no <= 35:
            ratio = rng.uniform(3.7, 4.6) # in [3.5, 4.8] (10 cases)
        else:
            ratio = rng.uniform(4.9, 5.8) # > 4.8 (10 cases)
    else: # L or X
        num_safety_vars = rng.randint(25, 40)
        if 40 <= case_no <= 45:
            ratio = rng.uniform(4.9, 5.8)
        else:
            ratio = rng.uniform(3.5, 4.5)

    num_rules = int(num_safety_vars * ratio)
    planted_assignment = {var: rng.choice([0, 1]) for var in range(1, num_safety_vars + 1)}

    safety_rules = []
    for r_idx in range(1, num_rules + 1):
        vars_3 = rng.sample(range(1, num_safety_vars + 1), 3)
        sat_var = vars_3[0]
        lit_1 = sat_var if planted_assignment[sat_var] == 1 else -sat_var
        lit_2 = vars_3[1] if rng.choice([0, 1]) == 1 else -vars_3[1]
        lit_3 = vars_3[2] if rng.choice([0, 1]) == 1 else -vars_3[2]
        lits = [lit_1, lit_2, lit_3]
        rng.shuffle(lits)
        safety_rules.append({
            'case_id': case_id, 'rule_no': r_idx,
            'lit_1': lits[0], 'lit_2': lits[1], 'lit_3': lits[2]
        })

    data['safety_vars'] = num_safety_vars
    data['safety_rules'] = safety_rules
    data['safety_planted'] = [{'case_id': case_id, 'switch': sw, 'value': val} for sw, val in planted_assignment.items()]

    # =========================================================================
    # 9. RATIONS
    # =========================================================================
    if tier == 'S':
        num_rations = rng.randint(8, 16)
    elif tier == 'M':
        num_rations = rng.randint(25, 36)
    else:
        num_rations = rng.randint(52, 75)

    ration_vals = [rng.randint(10, 500) for _ in range(num_rations)]
    num_planted = rng.randint(2, max(2, min(6, num_rations - 1)))
    planted_indices = set(rng.sample(range(num_rations), num_planted))
    target_sum = sum(ration_vals[idx] for idx in planted_indices)

    rations_rows = []
    for i_idx, val in enumerate(ration_vals):
        rations_rows.append({
            'case_id': case_id, 'item': i_idx, 'value': val,
            'planted': 1 if i_idx in planted_indices else 0
        })

    data['rations'] = rations_rows
    data['rations_target'] = target_sum

    # =========================================================================
    # 10. CLAIMS (TIER S ONLY)
    # =========================================================================
    if tier == 'S':
        c_weights = [c['weight'] for c in crates]
        c_vals = [c['value'] for c in crates]
        cargo_opt = solve_knapsack(c_weights, c_vals, capacity)

        w_tuples = [(w['start'], w['finish'], w['value']) for w in windows]
        window_count_opt = solve_interval_count(w_tuples)
        window_value_opt = solve_interval_value(w_tuples)

        drum_p_list = [d['price'] for d in drum_rows]
        drum_opt = solve_rod_cutting(drum_p_list, drum_L)

        tour_opt = solve_exact_tsp(coords_list)

        s_edges_list = [(e['u'], e['v']) for e in sensor_edges]
        cover_min = solve_exact_vertex_cover(num_sensor_nodes, s_edges_list)

        data['claims'] = [{
            'case_id': case_id,
            'cargo_opt': cargo_opt,
            'window_count_opt': window_count_opt,
            'window_value_opt': window_value_opt,
            'drum_opt': drum_opt,
            'tour_opt': tour_opt,
            'cover_min': cover_min
        }]

    return data
