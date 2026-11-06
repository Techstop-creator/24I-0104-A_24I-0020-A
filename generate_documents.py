"""
PDF Generation Script for LIFELINE Phase 1
Produces:
1. approach_note.pdf (Exactly 2 pages)
2. proposal.pdf (Strictly 2 pages: Page 1 = Module Table, Page 2 = Work Division Table)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_approach_note():
    pdf_path = "approach_note.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        alignment=1, # Centered
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=3
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontSize=7.0,
        leading=8.8,
        textColor=colors.HexColor('#1A202C'),
        leftIndent=10,
        spaceAfter=2
    )

    story = []

    # Title Banner
    story.append(Paragraph("LIFELINE: Iteration 1 Approach Note", title_style))
    story.append(Paragraph("Group 66 | FAST-NUCES Islamabad | BS Data Science & AI | Roll Nos: 24i-0104, 24i-0020", subtitle_style))

    # Part 1
    story.append(Paragraph("Part 1: From Story to Numbers", h1_style))
    story.append(Paragraph(
        "Every numerical bound and graph distribution in our generator directly reflects the narrative physics of the 6 case studies:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Delta Flood:</b> <i>'A flat delta of small villages joined by raised roads. Roads go under water in waves. Food and water matter most.'</i> "
        "We set average degree 2E/V in [2.2, 3.2] modeling a planar raised-embankment mesh. Over 40% of locations have penalty >= 2 to represent submerged, waterlogged road surfaces. At least 3 waves simulate progressive flooding, and Food/Water crates (categories 0, 1) constitute >= 55% of relief cargo.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Mountain Earthquake:</b> <i>'A valley town with a few roads and almost no alternatives. The injured need medicine and tools. Bursts of urgent calls follow each aftershock.'</i> "
        "Road topology is strictly constrained to sparse branching canyons (average degree 2.0 to 2.6). Medicine and tool crates (categories 2, 3) are biased to >= 45%, and seismic distress drives mean incident alarm priority >= 6.0.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>3. Coastal Cyclone:</b> <i>'A port city and fishing villages. Storm surge closes roads in waves. Rescue windows are short and overlap. The radio is full of noise.'</i> "
        "Emergency shelter locations (type S) are boosted to >= 25% of all nodes. Road closures occur in >= 3 surge waves. Rescue time windows are densely clustered so average window overlap is >= 2.0. Radio noise spans >= 30 of the 38 alphabet symbols.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>4. Urban Flash Flood:</b> <i>'A dense city with many alternative routes. Calls arrive faster than anyone can answer them. Rare equipment is available.'</i> "
        "Urban grid density forces average degree >= 3.5. Surging population distress generates high arrival rates (>= 1.5 alarms/tick on Tiers M and L). Specialized technical pumps and boats result in rare crates (cat 4) >= 10%.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>5. Landslide Corridor:</b> <i>'A single mountain highway along a gorge. A collapse cuts off whole communities.'</i> "
        "Linear highway spine limits max degree to <= 4 and average degree to <= 2.4, with the farthest location >= floor(V/4) roads from HQ. Multi-wave debris collapse severs critical bottlenecks, rendering at least one target completely unreachable from HQ.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>6. Outbreak Camp:</b> <i>'A relief camp with an outbreak. Medicine and water count and supplies spoil. Radio beacons repeat the same messages.'</i> "
        "Epidemic response requires Medicine and Water (cat 1, 2) >= 55%. Critical perishability forces >= 50% of crates to expire within 300 hours. Repetitive radio beacon transmissions cause one dominant symbol to occupy >= 25% of the log.",
        bullet_style
    ))

    # Part 2
    story.append(Paragraph("Part 2: Planted Objects and Claims (Correct by Construction)", h1_style))
    story.append(Paragraph(
        "<b>Planted Closed TSP Tour:</b> The generator constructs a valid permutation starting at site 0. For Tiers L and X, the planted tour is derived directly from the Nearest Neighbor (NN) heuristic starting from site 0. Because the tour is identical to or optimized from the NN path, its closed Manhattan length is guaranteed to be <= the NN tour length. Validator V6 verifies step-by-step consecutive validity and recalculates Manhattan distance exactly.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Planted Sensor Cover:</b> To plant a cover of size k (2 <= k <= n/2) that touches every edge, the generator first samples k distinct nodes to form the planted cover set C. All subsequent graph edges (u, v) are constructed by enforcing that at least one endpoint is selected from C. This ensures every edge touches the cover by definition. Validator V6 checks that every edge has u in C or v in C.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Planted 3-SAT Assignment:</b> An assignment vector A in {0, 1}^N is randomly fixed first. Each of the M 3-CNF clauses is then generated by picking 3 distinct variables and assigning at least one literal to agree with A. Hence, A evaluates to True across all clauses by construction. Validator V6 evaluates all clauses under the planted assignment.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Planted Rations (Subset Sum):</b> A random subset S of ration items is marked with planted=1, and rations_target is set to sum(v for i in S). Validator V6 sums the planted items and asserts exact equality.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Tier S Claims:</b> All 6 optima are computed using rigorous exact combinatorial solvers (0/1 Knapsack DP, Earliest Finish Time Greedy, Weighted Interval Scheduling DP, Rod Cutting DP, Exact TSP Branch & Bound, and Exact Vertex Cover bitmask search).",
        bullet_style
    ))

    story.append(PageBreak()) # FORCE EXACT PAGE 2

    # Part 3
    story.append(Paragraph("Part 3: The Four Hostile Traps", h1_style))
    story.append(Paragraph(
        "<b>Case 46 (Dock-Order Trap | Landslide Corridor):</b> 1,600 crates are generated with fixed weight (10 kg), non-decreasing value (10 to 100), non-decreasing expiry, non-decreasing serials, and non-decreasing value-per-kg. This monotonicity in 5 fields triggers worst-case O(N^2) quadratic behavior in naive QuickSort algorithms that pick the first element as pivot. <i>Validator check:</i> V8 verifies monotonicity across all 5 fields.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Case 47 (Best-Looking-Crate Trap | Outbreak Camp):</b> 12 crates are constructed where Crate 1 has weight 11 and value 55 (ratio 5.0), while Crates 2 and 3 each have weight 10 and value 48 (ratio 4.8). With truck capacity W = 20, the greedy density heuristic selects Crate 1 (leaving 9 kg, where no further items fit, yielding value 55). The optimal 0/1 knapsack selection picks Crates 2 and 3 (total value 96). Greedy achieves 55/96 = 57.29% <= 60% of optimum. <i>Validator check:</i> V8 executes both greedy and 0/1 DP knapsack, verifying greedy <= 60% of optimal.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Case 48 (Shortest-Looks-Cheapest Trap | Delta Flood):</b> A graph of 1,600 locations is built with a linear 600-edge chain (longest shortest path > 500 roads). Target 0 is connected via a direct 1-road path of minutes=60 into a penalty-6 node (cost 66), and an alternate 3-road path of minutes=1 into penalty-0 nodes (cost 9). The fewest-roads path (cost 66) is 7.33x more expensive than the cheapest path (cost 9), severely penalizing BFS-based routing. <i>Validator check:</i> V8 checks max hop distance >= 500 and asserts min fewest-roads cost >= 1.5x Dijkstra cost.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>Case 49 (Near-Miss Trap | Mountain Earthquake):</b> A 60,000-character log is composed entirely of block 'A'. Four search patterns are crafted with length-1 prefixes of 'A' followed by 'B' (e.g. 'AB', 'AAAB', 'AAAAAAAB', 'AAAAAAAAAAAB'). At every position, naive string matchers perform (L - 1) successful comparisons before failing on the final symbol, causing O(N * M) worst-case thrashing. <i>Validator check:</i> V8 asserts log repetition >= 90% and verifies that >= 4 patterns match their prefix at >= 50% of starting positions.",
        bullet_style
    ))

    # Part 4
    story.append(Paragraph("Part 4: What Will Be Hard in Iteration 2", h1_style))
    story.append(Paragraph(
        "For each case study, two relief decisions present severe algorithmic bottlenecks due to our data properties:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Delta Flood:</b> (a) <i>Route Planning:</i> Roads close in disjoint waves, requiring time-dependent dynamic shortest path recomputation rather than static Dijkstra. (b) <i>Relief Inventory:</i> High volume of low-penalty food/water crates creates tight weight-to-capacity ratios where fractional relaxation bounds fail to prune branch-and-bound trees efficiently.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>2. Mountain Earthquake:</b> (a) <i>Emergency Queue:</i> High mean priority (>= 6.0) causes severe priority-inversion and tie-breaking contention in the priority queue. (b) <i>Nearest Sites:</i> Mountain terrain topologies with long detours invalidate Euclidean heuristics, making spatial partitioning harder.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>3. Coastal Cyclone:</b> (a) <i>Rescue Scheduling:</i> Dense temporal clustering with average overlap >= 2.0 creates dense interval conflict graphs requiring O(M log M) DP with exact binary search predecessors. (b) <i>Radio Logs:</i> High symbol entropy (>= 30 symbols) degrades compression ratios and inflates Huffman tree depth.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>4. Urban Flash Flood:</b> (a) <i>Emergency Queue:</i> Arrival rates of >= 1.5 alarms/tick on Tiers M/L overwhelm standard event buffers, demanding strict heap operations. (b) <i>Route Planning:</i> Dense network (avg degree >= 3.5) causes rapid priority-queue growth and dense relaxation operations in Dijkstra.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>5. Landslide Corridor:</b> (a) <i>Route Planning:</i> Wave closures disconnect critical targets, requiring fast reachability cut detection (BFS/Tarjan bridges). (b) <i>Chains and Cuts:</i> Extreme linear graph diameter forces high hop counts, making dynamic programming state spaces deeper.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>6. Outbreak Camp:</b> (a) <i>Relief Inventory:</i> Half of crates expire by hour 300, turning standard 0/1 knapsack into a 2D time-dependent knapsack. (b) <i>Radio Logs:</i> Extreme symbol skew (>= 25% single symbol) causes unbalanced Huffman trees and requires specialized run-length or prefix encoding.",
        bullet_style
    ))

    doc.build(story)
    print("approach_note.pdf successfully generated (2 pages).")

def build_proposal():
    pdf_path = "proposal.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=24,
        bottomMargin=24
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'PropTitle',
        parent=styles['Heading1'],
        fontSize=12.5,
        leading=15,
        textColor=colors.HexColor('#1A365D'),
        alignment=1,
        spaceAfter=2
    )
    sub_style = ParagraphStyle(
        'PropSub',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=5
    )
    th_style = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontSize=7.0,
        leading=8.5,
        textColor=colors.white,
        fontName='Helvetica-Bold',
        alignment=1
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=6.2,
        leading=7.8,
        textColor=colors.HexColor('#1A202C'),
        fontName='Helvetica-Bold'
    )
    cell_text = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=5.8,
        leading=7.2,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("LIFELINE: Algorithm Selection Report (Proposal)", title_style))
    story.append(Paragraph("Group 66 | Section A | BS Data Science & AI | Roll Nos: 24i-0104, 24i-0020", sub_style))

    # Page 1 contains ONE TABLE with 9 rows (Modules A to I) and NOTHING ELSE
    table_data = [
        [
            Paragraph("Module", th_style),
            Paragraph("Problem (Variables)", th_style),
            Paragraph("Candidates & Complexities", th_style),
            Paragraph("Selection", th_style),
            Paragraph("Justification & Failure Case", th_style)
        ],
        [
            Paragraph("<b>A. Relief Inventory</b>", cell_bold),
            Paragraph("Max sum(v_i) s.t. sum(w_i) &lt;= W, indivisible crates.<br/>Vars: N crates, capacity W.", cell_text),
            Paragraph("1. 0/1 Knapsack DP: O(N*W)<br/>2. Branch &amp; Bound: O(2^N)<br/>3. Greedy density: O(N log N)", cell_text),
            Paragraph("<b>Primary:</b> 0/1 DP<br/><b>Baseline:</b> Greedy value/kg", cell_text),
            Paragraph("DP guarantees global optimum. Greedy fails severely on adversarial sets (Case 47 achieves &lt;= 60% of optimum).", cell_text)
        ],
        [
            Paragraph("<b>B. Route Planning</b>", cell_bold),
            Paragraph("Find cheapest path u-&gt;v with edge mins + target penalty, plus reachable set.<br/>Vars: V locs, E roads.", cell_text),
            Paragraph("1. Dijkstra + Min-Heap: O((V+E) log V)<br/>2. Bellman-Ford: O(V*E)<br/>3. Breadth-First Search: O(V+E)", cell_text),
            Paragraph("<b>Primary:</b> Dijkstra (Heap)<br/><b>Baseline:</b> BFS (fewest roads)", cell_text),
            Paragraph("Non-negative costs make Dijkstra optimal. BFS only minimizes hops and incurs severe cost inflation (Case 48 costs &gt;= 1.5x).", cell_text)
        ],
        [
            Paragraph("<b>C. Rescue Scheduling</b>", cell_bold),
            Paragraph("Select max compatible windows (count or value), touching allowed.<br/>Vars: M windows in [0, 1440].", cell_text),
            Paragraph("1. Weighted DP + BinSearch: O(M log M)<br/>2. Greedy Earliest Finish: O(M log M)<br/>3. Brute Force: O(2^M)", cell_text),
            Paragraph("<b>Primary:</b> Weighted DP<br/><b>Baseline:</b> Greedy Earliest Finish", cell_text),
            Paragraph("Weighted DP finds optimal values under heavy overlap. Greedy only optimizes unweighted count and fails on value maximization.", cell_text)
        ],
        [
            Paragraph("<b>D. Emergency Queue</b>", cell_bold),
            Paragraph("Release 1 alarm per tick in urgency order (priority 10 down to 1).<br/>Vars: A alarms, T ticks.", cell_text),
            Paragraph("1. Binary Min-Heap: O(A log A)<br/>2. Fibonacci Heap: O(A + A log A)<br/>3. Unsorted List: O(A^2)", cell_text),
            Paragraph("<b>Primary:</b> Binary Max-Heap<br/><b>Baseline:</b> Unsorted Array Scan", cell_text),
            Paragraph("Heap guarantees O(log A) push/pop, sustaining bursts up to 1.8 alarms/tick (Urban Flood). Unsorted scans cause starvation.", cell_text)
        ],
        [
            Paragraph("<b>E. Radio Logs</b>", cell_bold),
            Paragraph("Pattern search (overlaps); min edit script; prefix-free code.<br/>Vars: N log len, P pat len, L reports.", cell_text),
            Paragraph("1. KMP: O(N+P) vs Naive O(N*P)<br/>2. Wagner-Fischer: O(L1*L2)<br/>3. Huffman Coding: O(S log S)", cell_text),
            Paragraph("<b>Primary:</b> KMP + Wagner-Fischer + Huffman<br/><b>Baseline:</b> Naive search", cell_text),
            Paragraph("KMP eliminates backtracking on near-miss logs (Case 49 triggers O(N*P) in naive search). Huffman minimizes transmission bits.", cell_text)
        ],
        [
            Paragraph("<b>F. Network Planning</b>", cell_bold),
            Paragraph("Connect all reachable nodes with minimum total cable cost.<br/>Vars: V locs, E roads.", cell_text),
            Paragraph("1. Kruskal + DSU: O(E log V)<br/>2. Prim + Heap: O(E + V log V)<br/>3. BFS Spanning Tree: O(V+E)", cell_text),
            Paragraph("<b>Primary:</b> Kruskal with DSU<br/><b>Baseline:</b> BFS Spanning Tree", cell_text),
            Paragraph("Sparse-to-medium networks (E &lt;= 3V) favor Kruskal with path compression. BFS tree ignores cable weights and yields suboptimal cost.", cell_text)
        ],
        [
            Paragraph("<b>G. Chains &amp; Cuts</b>", cell_bold),
            Paragraph("Optimal matrix chain parenthesization; max revenue drum cut.<br/>Vars: n stages, drum length L.", cell_text),
            Paragraph("1. Matrix Chain DP: O(n^3)<br/>2. Drum Cutting DP: O(L^2)<br/>3. Greedy price/meter cut: O(L log L)", cell_text),
            Paragraph("<b>Primary:</b> 1D &amp; 2D DP<br/><b>Baseline:</b> Greedy Density Cutting", cell_text),
            Paragraph("Non-monotonic drum prices cause greedy cutting to fail. Matrix chain DP finds exact global minimum scalar multiplications.", cell_text)
        ],
        [
            Paragraph("<b>H. Hard Planning</b>", cell_bold),
            Paragraph("Solve 3-SAT, Subset Sum, closed TSP, and Vertex Cover.<br/>Vars: N vars/items, V nodes, k cover.", cell_text),
            Paragraph("1. DPLL Backtracking: O(2^N)<br/>2. Subset Sum DP: O(N*Sum)<br/>3. TSP Held-Karp / Branch &amp; Bound<br/>4. Vertex Cover FPT: O(2^k * V)", cell_text),
            Paragraph("<b>Primary:</b> DPLL + Exact DP / B&amp;B<br/><b>Baseline:</b> Random Walk / 2-Approx", cell_text),
            Paragraph("Exact DP/B&amp;B verifies planted solutions and handles phase-transition clause densities (ratio 3.5 to 4.8). Approximations fail exact targets.", cell_text)
        ],
        [
            Paragraph("<b>I. Nearest &amp; Checksums</b>", cell_bold),
            Paragraph("Pair of sites at min squared dist; product of serial numbers.<br/>Vars: n sites, D digits.", cell_text),
            Paragraph("1. Closest Pair D&amp;C: O(n log n)<br/>2. Karatsuba Mult: O(D^1.585)<br/>3. All-pairs O(n^2), Grade-School O(D^2)", cell_text),
            Paragraph("<b>Primary:</b> Divide &amp; Conquer + Karatsuba<br/><b>Baseline:</b> O(n^2) Brute Force", cell_text),
            Paragraph("Divide-and-conquer scales efficiently to Tier L (n=500 sites). Karatsuba speeds up multi-precision arithmetic on serial products.", cell_text)
        ]
    ]

    col_widths = [75, 110, 130, 95, 140]
    t1 = Table(table_data, colWidths=col_widths, repeatRows=1)
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#CBD5E0')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#1A365D')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t1)

    # ================= PAGE 2 =================
    story.append(PageBreak())

    p2_title = ParagraphStyle(
        'P2Title',
        parent=styles['Heading1'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1A365D'),
        alignment=1,
        spaceAfter=3
    )
    p2_sub = ParagraphStyle(
        'P2Sub',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=15
    )

    story.append(Paragraph("LIFELINE: Iteration 1 Work Division & Iteration 2 Plan", p2_title))
    story.append(Paragraph("Group 66 | Section A | Equal 50/50 Team Collaboration (2 Members)", p2_sub))

    # Page 2 contains ONE TABLE with 1 row per member
    work_table_data = [
        [
            Paragraph("Member", th_style),
            Paragraph("Iteration 1 Contribution &amp; Iteration 2 Proposed Decision Modules", th_style)
        ],
        [
            Paragraph(
                "<b>Member 1</b><br/><br/>"
                "<b>Name:</b> Member 1<br/>"
                "<b>Roll No:</b> 24i-0104<br/>"
                "<b>Section:</b> A<br/>"
                "<b>Role:</b> Core Systems, Graph Algorithms &amp; Traps Architect",
                cell_bold
            ),
            Paragraph(
                "<b>Iteration 1 Contributions:</b><br/>"
                "• <b>Generator Core:</b> Architected `main.py`, CLI arguments, workbook serializer for all 20 sheets, and natural sorting logic.<br/>"
                "• <b>Data Modules Built:</b> Crates generator (weight, value, expiry, serials), Locations (penalties, depot/shelter assignments), Roads network generator, and Wave Closures.<br/>"
                "• <b>Hostile Traps:</b> Implemented Case 46 (Dock-Order monotone crate list) and Case 48 (Shortest-Looks-Cheapest 600-node chain with 7.33x BFS cost penalty).<br/>"
                "• <b>Validator Engineering:</b> Implemented checks V1 (Sheet schema and consecutive case IDs), V2 (Numerical ranges and capacity thresholds), V3 (Foreign key and reference validation), V4 (Network connectivity via BFS and wave disjointness), and V7 (Delta Flood, Mountain, and Coastal scenario signatures).<br/>"
                "• <b>Documentation:</b> Authored Approach Note Part 1 (Story to numbers) and Part 3 (Traps specification and adversarial mechanics).<br/><br/>"
                "<b>Proposed Iteration 2 Decision Modules:</b><br/>"
                "• <b>Module A (Relief Inventory):</b> 0/1 Knapsack Dynamic Programming with space-optimized state array.<br/>"
                "• <b>Module B (Route Planning):</b> Dijkstra's Algorithm with binary min-heap supporting dynamic road closures and target penalties.<br/>"
                "• <b>Module D (Emergency Queue):</b> Event-driven Priority Queue engine managing incident streams under high alarm rates.<br/>"
                "• <b>Module F (Network Planning):</b> Kruskal's Minimum Spanning Tree with Disjoint Set Union (path compression and union-by-rank).",
                ParagraphStyle('CellTextLarge', parent=cell_text, fontSize=7.2, leading=9.6)
            )
        ],
        [
            Paragraph(
                "<b>Member 2</b><br/><br/>"
                "<b>Name:</b> Member 2<br/>"
                "<b>Roll No:</b> 24i-0020<br/>"
                "<b>Section:</b> A<br/>"
                "<b>Role:</b> Planted Objects, String Analysis &amp; Hard Problems Lead",
                cell_bold
            ),
            Paragraph(
                "<b>Iteration 1 Contributions:</b><br/>"
                "• <b>Data Modules Built:</b> Radio Log &amp; Chunking, Patterns (2 to 40 chars), Reports &amp; Levenshtein mutation, Rescue Windows (touching pairs), Incidents &amp; Poisson ticks, Sites &amp; Planted TSP Tour, Pipeline Dimensions, Drum Prices, Sensor Cover, Safety Rules (3-SAT), and Rations (Subset Sum).<br/>"
                "• <b>Exact Tier S Solvers:</b> Implemented exact algorithms for `claims` sheet: 0/1 Knapsack DP, Earliest Finish Time Greedy, Weighted Interval DP, Rod Cutting DP, Exact TSP DP, and Minimum Vertex Cover bitmask search.<br/>"
                "• <b>Hostile Traps:</b> Implemented Case 47 (Best-Looking-Crate greedy trap &lt;= 60%) and Case 49 (Near-Miss 60,000-char string matching worst-case).<br/>"
                "• <b>Validator Engineering:</b> Implemented checks V5 (Pattern counts, edit distance bounds, and Tier S claims recomputations), V6 (Planted tour closed Manhattan length, sensor cover, 3-SAT satisfying assignment, and rations sum), and V8 (Trap rules 46-49 verification). Built `create_broken_tests.py` (10 corrupted cases) and `run_suite.py`.<br/>"
                "• <b>Documentation:</b> Authored Approach Note Part 2 (Planted objects proof) and Part 4 (What will be hard), and Proposal Page 1 Table.<br/><br/>"
                "<b>Proposed Iteration 2 Decision Modules:</b><br/>"
                "• <b>Module C (Rescue Scheduling):</b> Weighted Interval Scheduling DP with binary search for predecessor compatible windows.<br/>"
                "• <b>Module E (Radio Logs):</b> Knuth-Morris-Pratt (KMP) string matching, Wagner-Fischer edit scripts, and Huffman compression.<br/>"
                "• <b>Module G (Chains &amp; Cuts):</b> Matrix Chain Multiplication DP parenthesization and Unbounded Rod Cutting DP.<br/>"
                "• <b>Module H (Hard Planning):</b> DPLL SAT solver with unit propagation, Subset Sum meet-in-the-middle, and Vertex Cover FPT.<br/>"
                "• <b>Module I (Nearest &amp; Checksums):</b> Divide-and-Conquer Closest Pair of Points and Karatsuba Fast Multiplication.",
                ParagraphStyle('CellTextLarge2', parent=cell_text, fontSize=7.2, leading=9.6)
            )
        ]
    ]

    t2 = Table(work_table_data, colWidths=[130, 420])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#1A365D')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')])
    ]))
    story.append(t2)

    doc.build(story)
    print("proposal.pdf successfully generated (strictly 2 pages).")

if __name__ == '__main__':
    build_approach_note()
    build_proposal()
