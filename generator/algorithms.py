"""
LIFELINE Data Generator
Design and Analysis of Algorithms - Project Phase 1
FAST-NUCES Islamabad
Degree: BS Artificial Intelligence (AI) | Section: AI-A
Team: Irtaza Shahid (24I-0104), Muhammad Harris (24I-0020)
"""

import sys
import os
import random
import itertools
from collections import deque
import openpyxl

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

def get_tier(case_no):
    if 0 <= case_no <= 19:
        return 'S'
    elif 20 <= case_no <= 39:
        return 'M'
    elif 40 <= case_no <= 45:
        return 'L'
    else:
        return 'X'

def get_scenario(case_no):
    return (case_no % 6) + 1

# Levenshtein distance
def compute_edit_distance(s1, s2):
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

# Exact 0/1 Knapsack
def solve_knapsack(weights, values, capacity):
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        w = weights[i]
        v = values[i]
        for c in range(capacity, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[capacity]

# Greedy Knapsack (value / kg descending)
def solve_greedy_knapsack(weights, values, capacity):
    items = []
    for i in range(len(weights)):
        items.append((values[i] / weights[i], weights[i], values[i], i))
    items.sort(key=lambda x: (-x[0], x[1])) # higher ratio first
    total_val = 0
    cur_cap = capacity
    for ratio, w, v, idx in items:
        if w <= cur_cap:
            cur_cap -= w
            total_val += v
    return total_val

# Exact Interval Scheduling (unweighted - max count)
def solve_interval_count(windows):
    # windows: list of (start, finish, value) or (start, finish, value, id)
    sorted_w = sorted(windows, key=lambda x: (x[1], x[0]))
    count = 0
    last_finish = -1
    for w in sorted_w:
        s, f = w[0], w[1]
        if s >= last_finish:
            count += 1
            last_finish = f
    return count

# Exact Weighted Interval Scheduling (max value)
def solve_interval_value(windows):
    sorted_w = sorted(windows, key=lambda x: x[1])
    n = len(sorted_w)
    dp = [0] * (n + 1)
    finishes = [w[1] for w in sorted_w]
    for i in range(1, n + 1):
        w = sorted_w[i - 1]
        s, f, val = w[0], w[1], w[2]
        low = 0
        high = i - 1
        p = 0
        while low <= high:
            mid = (low + high) // 2
            if finishes[mid] <= s:
                p = mid + 1
                low = mid + 1
            else:
                high = mid - 1
        dp[i] = max(dp[i - 1], dp[p] + val)
    return dp[n]

# Exact Rod Cutting DP
def solve_rod_cutting(prices, L):
    # prices: 1-indexed (prices[0] for len 1, etc.)
    dp = [0] * (L + 1)
    for i in range(1, L + 1):
        max_val = -1
        for j in range(1, i + 1):
            val = prices[j - 1] + dp[i - j]
            if val > max_val:
                max_val = val
        dp[i] = max_val
    return dp[L]

# Exact TSP (Manhattan metric, closed tour from site 0)
def solve_exact_tsp(sites):
    # sites: list of (x, y)
    n = len(sites)
    if n <= 1:
        return 0
    dist = [[abs(sites[i][0] - sites[j][0]) + abs(sites[i][1] - sites[j][1]) for j in range(n)] for i in range(n)]
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

# Exact Minimum Vertex Cover
def solve_exact_vertex_cover(n, edges):
    if not edges:
        return 0
    # bitmask search
    for k in range(1, n + 1):
        for combo in itertools.combinations(range(n), k):
            c_set = set(combo)
            covered = True
            for u, v in edges:
                if u not in c_set and v not in c_set:
                    covered = False
                    break
            if covered:
                return k
    return n

# Manhattan distance
def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Nearest neighbor tour from site 0
def compute_nn_tour_length(sites):
    n = len(sites)
    visited = [False] * n
    visited[0] = True
    curr = 0
    total = 0
    for _ in range(n - 1):
        best_d = float('inf')
        best_nxt = -1
        for nxt in range(n):
            if not visited[nxt]:
                d = manhattan_dist(sites[curr], sites[nxt])
                if d < best_d:
                    best_d = d
                    best_nxt = nxt
        visited[best_nxt] = True
        total += best_d
        curr = best_nxt
    total += manhattan_dist(sites[curr], sites[0])
    return total

