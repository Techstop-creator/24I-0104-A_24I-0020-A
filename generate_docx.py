"""
Word (.docx) Document Generator for LIFELINE Phase 1
Generates:
1. approach_note.docx
2. proposal.docx
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_approach_note_docx():
    doc = docx.Document()
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.6)
        s.right_margin = Inches(0.6)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LIFELINE: Iteration 1 Approach Note")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Group 66 | FAST-NUCES Islamabad | BS Data Science & AI | Roll Nos: 24i-0104, 24i-0020")
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(74, 85, 104)

    # Part 1
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("Part 1: From Story to Numbers")
    r_h1.bold = True
    r_h1.font.size = Pt(12)
    r_h1.font.color.rgb = RGBColor(43, 108, 176)

    intro = doc.add_paragraph()
    intro.paragraph_format.space_after = Pt(4)
    intro.add_run("Every numerical bound and graph distribution in our generator directly reflects the narrative physics of the 6 case studies:").font.size = Pt(9)

    points_p1 = [
        ("1. Delta Flood: ", "'A flat delta of small villages joined by raised roads. Roads go under water in waves. Food and water matter most.' ",
         "We set average degree 2E/V in [2.2, 3.2] modeling a planar raised-embankment mesh. Over 40% of locations have penalty >= 2 to represent submerged, waterlogged road surfaces. At least 3 waves simulate progressive flooding, and Food/Water crates (categories 0, 1) constitute >= 55% of relief cargo."),
        ("2. Mountain Earthquake: ", "'A valley town with a few roads and almost no alternatives. The injured need medicine and tools. Bursts of urgent calls follow each aftershock.' ",
         "Road topology is strictly constrained to sparse branching canyons (average degree 2.0 to 2.6). Medicine and tool crates (categories 2, 3) are biased to >= 45%, and seismic distress drives mean incident alarm priority >= 6.0."),
        ("3. Coastal Cyclone: ", "'A port city and fishing villages. Storm surge closes roads in waves. Rescue windows are short and overlap. The radio is full of noise.' ",
         "Emergency shelter locations (type S) are boosted to >= 25% of all nodes. Road closures occur in >= 3 surge waves. Rescue time windows are densely clustered so average window overlap is >= 2.0. Radio noise spans >= 30 of the 38 alphabet symbols."),
        ("4. Urban Flash Flood: ", "'A dense city with many alternative routes. Calls arrive faster than anyone can answer them. Rare equipment is available.' ",
         "Urban grid density forces average degree >= 3.5. Surging population distress generates high arrival rates (>= 1.5 alarms/tick on Tiers M and L). Specialized technical pumps and boats result in rare crates (cat 4) >= 10%."),
        ("5. Landslide Corridor: ", "'A single mountain highway along a gorge. A collapse cuts off whole communities.' ",
         "Linear highway spine limits max degree to <= 4 and average degree to <= 2.4, with the farthest location >= floor(V/4) roads from HQ. Multi-wave debris collapse severs critical bottlenecks, rendering at least one target completely unreachable from HQ."),
        ("6. Outbreak Camp: ", "'A relief camp with an outbreak. Medicine and water count and supplies spoil. Radio beacons repeat the same messages.' ",
         "Epidemic response requires Medicine and Water (cat 1, 2) >= 55%. Critical perishability forces >= 50% of crates to expire within 300 hours. Repetitive radio beacon transmissions cause one dominant symbol to occupy >= 25% of the log.")
    ]

    for title, quote, desc in points_p1:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.size = Pt(8.5)
        r2 = p.add_run(quote)
        r2.italic = True
        r2.font.size = Pt(8.5)
        r3 = p.add_run(desc)
        r3.font.size = Pt(8.5)

    # Part 2
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(6)
    r_h2 = h2.add_run("Part 2: Planted Objects and Claims (Correct by Construction)")
    r_h2.bold = True
    r_h2.font.size = Pt(12)
    r_h2.font.color.rgb = RGBColor(43, 108, 176)

    points_p2 = [
        ("Planted Closed TSP Tour: ", "The generator constructs a valid permutation starting at site 0. For Tiers L and X, the planted tour is derived directly from the Nearest Neighbor (NN) heuristic starting from site 0. Because the tour is identical to or optimized from the NN path, its closed Manhattan length is guaranteed to be <= the NN tour length. Validator V6 verifies step-by-step consecutive validity and recalculates Manhattan distance exactly."),
        ("Planted Sensor Cover: ", "To plant a cover of size k (2 <= k <= n/2) that touches every edge, the generator first samples k distinct nodes to form the planted cover set C. All subsequent graph edges (u, v) are constructed by enforcing that at least one endpoint is selected from C. This ensures every edge touches the cover by definition. Validator V6 checks that every edge has u in C or v in C."),
        ("Planted 3-SAT Assignment: ", "An assignment vector A in {0, 1}^N is randomly fixed first. Each of the M 3-CNF clauses is then generated by picking 3 distinct variables and assigning at least one literal to agree with A. Hence, A evaluates to True across all clauses by construction. Validator V6 evaluates all clauses under the planted assignment."),
        ("Planted Rations (Subset Sum): ", "A random subset S of ration items is marked with planted=1, and rations_target is set to sum(v for i in S). Validator V6 sums the planted items and asserts exact equality."),
        ("Tier S Claims: ", "All 6 optima are computed using rigorous exact combinatorial solvers (0/1 Knapsack DP, Earliest Finish Time Greedy, Weighted Interval Scheduling DP, Rod Cutting DP, Exact TSP Branch & Bound, and Exact Vertex Cover bitmask search).")
    ]

    for title, desc in points_p2:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.size = Pt(8.5)
        r2 = p.add_run(desc)
        r2.font.size = Pt(8.5)

    doc.add_page_break()

    # Part 3
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("Part 3: The Four Hostile Traps")
    r_h3.bold = True
    r_h3.font.size = Pt(12)
    r_h3.font.color.rgb = RGBColor(43, 108, 176)

    points_p3 = [
        ("Case 46 (Dock-Order Trap | Landslide Corridor): ", "1,600 crates are generated with fixed weight (10 kg), non-decreasing value (10 to 100), non-decreasing expiry, non-decreasing serials, and non-decreasing value-per-kg. This monotonicity in 5 fields triggers worst-case O(N^2) quadratic behavior in naive QuickSort algorithms that pick the first element as pivot. Validator check: V8 verifies monotonicity across all 5 fields."),
        ("Case 47 (Best-Looking-Crate Trap | Outbreak Camp): ", "12 crates are constructed where Crate 1 has weight 11 and value 55 (ratio 5.0), while Crates 2 and 3 each have weight 10 and value 48 (ratio 4.8). With truck capacity W = 20, the greedy density heuristic selects Crate 1 (leaving 9 kg, where no further items fit, yielding value 55). The optimal 0/1 knapsack selection picks Crates 2 and 3 (total value 96). Greedy achieves 55/96 = 57.29% <= 60% of optimum. Validator check: V8 executes both greedy and 0/1 DP knapsack, verifying greedy <= 60% of optimal."),
        ("Case 48 (Shortest-Looks-Cheapest Trap | Delta Flood): ", "A graph of 1,600 locations is built with a linear 600-edge chain (longest shortest path > 500 roads). Target 0 is connected via a direct 1-road path of minutes=60 into a penalty-6 node (cost 66), and an alternate 3-road path of minutes=1 into penalty-0 nodes (cost 9). The fewest-roads path (cost 66) is 7.33x more expensive than the cheapest path (cost 9), severely penalizing BFS-based routing. Validator check: V8 checks max hop distance >= 500 and asserts min fewest-roads cost >= 1.5x Dijkstra cost."),
        ("Case 49 (Near-Miss Trap | Mountain Earthquake): ", "A 60,000-character log is composed entirely of block 'A'. Four search patterns are crafted with length-1 prefixes of 'A' followed by 'B' (e.g. 'AB', 'AAAB', 'AAAAAAAB', 'AAAAAAAAAAAB'). At every position, naive string matchers perform (L - 1) successful comparisons before failing on the final symbol, causing O(N * M) worst-case thrashing. Validator check: V8 asserts log repetition >= 90% and verifies that >= 4 patterns match their prefix at >= 50% of starting positions.")
    ]

    for title, desc in points_p3:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.size = Pt(8.5)
        r2 = p.add_run(desc)
        r2.font.size = Pt(8.5)

    # Part 4
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(6)
    r_h4 = h4.add_run("Part 4: What Will Be Hard in Iteration 2")
    r_h4.bold = True
    r_h4.font.size = Pt(12)
    r_h4.font.color.rgb = RGBColor(43, 108, 176)

    intro4 = doc.add_paragraph()
    intro4.paragraph_format.space_after = Pt(4)
    intro4.add_run("For each case study, two relief decisions present severe algorithmic bottlenecks due to our data properties:").font.size = Pt(9)

    points_p4 = [
        ("1. Delta Flood: ", "(a) Route Planning: Roads close in disjoint waves, requiring time-dependent dynamic shortest path recomputation rather than static Dijkstra. (b) Relief Inventory: High volume of low-penalty food/water crates creates tight weight-to-capacity ratios where fractional relaxation bounds fail to prune branch-and-bound trees efficiently."),
        ("2. Mountain Earthquake: ", "(a) Emergency Queue: High mean priority (>= 6.0) causes severe priority-inversion and tie-breaking contention in the priority queue. (b) Nearest Sites: Mountain terrain topologies with long detours invalidate Euclidean heuristics, making spatial partitioning harder."),
        ("3. Coastal Cyclone: ", "(a) Rescue Scheduling: Dense temporal clustering with average overlap >= 2.0 creates dense interval conflict graphs requiring O(M log M) DP with exact binary search predecessors. (b) Radio Logs: High symbol entropy (>= 30 symbols) degrades compression ratios and inflates Huffman tree depth."),
        ("4. Urban Flash Flood: ", "(a) Emergency Queue: Arrival rates of >= 1.5 alarms/tick on Tiers M/L overwhelm standard event buffers, demanding strict heap operations. (b) Route Planning: Dense network (avg degree >= 3.5) causes rapid priority-queue growth and dense relaxation operations in Dijkstra."),
        ("5. Landslide Corridor: ", "(a) Route Planning: Wave closures disconnect critical targets, requiring fast reachability cut detection (BFS/Tarjan bridges). (b) Chains and Cuts: Extreme linear graph diameter forces high hop counts, making dynamic programming state spaces deeper."),
        ("6. Outbreak Camp: ", "(a) Relief Inventory: Half of crates expire by hour 300, turning standard 0/1 knapsack into a 2D time-dependent knapsack. (b) Radio Logs: Extreme symbol skew (>= 25% single symbol) causes unbalanced Huffman trees and requires specialized run-length or prefix encoding.")
    ]

    for title, desc in points_p4:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.size = Pt(8.5)
        r2 = p.add_run(desc)
        r2.font.size = Pt(8.5)

    doc.save("approach_note.docx")
    print("approach_note.docx successfully generated.")

if __name__ == '__main__':
    create_approach_note_docx()

