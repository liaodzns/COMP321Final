#!/usr/bin/env python3
"""
This solution demonstrates a common Kattis mistake:
    - using an O(V^3) all-pairs connectivity algorithm (Floyd–Warshall)
      when a simple O(V + E) DFS/BFS over the graph would suffice.

For up to 1000 buildings, the algorithm will require 10^9 iterations,
which will almost certainly Time Out in python
"""

import sys

def main() -> None:
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return

    it = iter(data)

    # Number of buildings
    B = int(next(it).strip())

    # List of building IDs to inspect 
    inspect_line = next(it).strip()
    to_inspect = list(map(int, inspect_line.split())) if inspect_line else []

    # Building an adjacency matrix for ALL IDs 0..1000.
    # This is already heavier than needed (1e6 entries),
    # but still under typical memory limits.
    MAX_ID = 1000
    reachable = [[False] * (MAX_ID + 1) for _ in range(MAX_ID + 1)]

    # Track which building IDs actually appear in the description so we can limit the Floyd–Warshall loops somewhat.
    seen_ids = set()

    # loop through all the building descriptions
    for _ in range(B):
        try:
            line = next(it)
        except StopIteration:
            break

        line = line.strip()
        if not line:
            continue

        parts = list(map(int, line.split()))
        if len(parts) < 2:
            continue

        node = parts[0]
        deg = parts[1]
        neighbors = parts[2:2 + deg]

        seen_ids.add(node)
        reachable[node][node] = True  # a building can reach itself

        for nb in neighbors:
            seen_ids.add(nb)
            reachable[nb][nb] = True
            # connecting both ways since the tunnels go both directions
            reachable[node][nb] = True
            reachable[nb][node] = True

    if not seen_ids:
        # if there's no buildings at all, we don't need to drive anywhere
        print(0)
        return

    max_id = max(seen_ids)

    # This is the slow part - using Floyd-Warshall to find all connections
    # It's doing way too many loops (like max_id^3 times)
    # This is gonna time out but I wanted to see if it would work
    #
    for k in range(1, max_id + 1):
        for i in range(1, max_id + 1):
            if reachable[i][k]:          # small optimization, still too slow
                row_i = reachable[i]
                row_k = reachable[k]
                for j in range(1, max_id + 1):
                    if row_k[j]:
                        row_i[j] = True

    # Reachable[i][j] tells us if building i and j are connected, even if they need to go through other buildings to get there

    # Now group the buildings from Billy's list into components.
    comp_id = {}
    sectors = 0

    for b in to_inspect:
        if b not in comp_id:
            sectors += 1
            cid = sectors
            # Check which other buildings in Billy's list we can reach from this one
            # and put them in the same component.
            for other in to_inspect:
                if reachable[b][other]:
                    comp_id[other] = cid

    print(sectors)

if __name__ == "__main__":
    main()
