import sys
from collections import deque

"""
Tesla Plant – Connected Components

We read the graph, then count how many connected components
contain at least one building on Billy's inspection list.

If that number is k, he needs k - 1 drives between sectors.
"""

def main() -> None:
    lines = sys.stdin.read().strip().splitlines()
    if not lines:
        return

    it = iter(lines)

    # First line: number of buildings and number to inspect
    first_line = next(it).strip().split()
    B = int(first_line[0])
    num_to_inspect = int(first_line[1])

    # Second line: building IDs to inspect
    inspect_line = next(it).strip()
    if inspect_line:
        to_inspect = list(map(int, inspect_line.split()))
    else:
        to_inspect = []

    MAX_ID = 1000  # IDs satisfy 0 < id < 1000
    adj = [[] for _ in range(MAX_ID + 1)]

    # Next B lines: "id degree neighbor1 neighbor2 ..."
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

        for nb in neighbors:
            if 0 <= node <= MAX_ID and 0 <= nb <= MAX_ID:
                adj[node].append(nb)
                adj[nb].append(node)  # undirected

    visited = [False] * (MAX_ID + 1)
    sectors = 0

    # BFS from every unvisited building in the inspection list
    for start in to_inspect:
        if start < 0 or start > MAX_ID:
            continue
        if visited[start]:
            continue

        sectors += 1
        q = deque([start])
        visited[start] = True

        while q:
            u = q.popleft()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)

    drives = sectors - 1 if sectors > 0 else 0
    print(drives)


if __name__ == "__main__":
    main()
