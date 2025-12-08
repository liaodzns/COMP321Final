import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

/**
 * Tesla Plant – Connected Components
 *
 * Build an undirected graph of buildings, then count the number
 * of connected components that contain at least one building
 * from Billy's inspection list. Answer = max(0, k - 1).
 */
public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        // First line: number of buildings and number to inspect
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) {
            return;
        }
        StringTokenizer st = new StringTokenizer(line.trim());
        int B = Integer.parseInt(st.nextToken());
        int numToInspect = Integer.parseInt(st.nextToken());

        // Second line: sequence of building IDs to inspect
        line = br.readLine();
        List<Integer> toInspect = new ArrayList<>();
        if (line != null && !line.trim().isEmpty()) {
            st = new StringTokenizer(line);
            for (int i = 0; i < numToInspect; i++) {
                toInspect.add(Integer.parseInt(st.nextToken()));
            }
        }

        final int MAX_ID = 1000; // IDs are 0 < id < 1000
        @SuppressWarnings("unchecked")
        List<Integer>[] adj = new ArrayList[MAX_ID + 1];
        for (int i = 0; i <= MAX_ID; i++) {
            adj[i] = new ArrayList<>();
        }

        // Next B lines: building id, degree, then neighbors
        for (int i = 0; i < B; i++) {
            line = br.readLine();
            while (line != null && line.trim().isEmpty()) {
                line = br.readLine(); // skip blank lines if any
            }
            if (line == null) break;

            st = new StringTokenizer(line);
            int id = Integer.parseInt(st.nextToken());
            int deg = Integer.parseInt(st.nextToken());

            for (int j = 0; j < deg; j++) {
                int nb = Integer.parseInt(st.nextToken());
                if (id >= 0 && id <= MAX_ID && nb >= 0 && nb <= MAX_ID) {
                    adj[id].add(nb);
                    adj[nb].add(id); // undirected edge
                }
            }
        }

        boolean[] visited = new boolean[MAX_ID + 1];
        int sectors = 0;

        // BFS/DFS from each unvisited building in the inspection list
        for (int start : toInspect) {
            if (start < 0 || start > MAX_ID) {
                continue;
            }
            if (visited[start]) {
                continue;
            }

            sectors++;
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            visited[start] = true;
            queue.add(start);

            while (!queue.isEmpty()) {
                int u = queue.poll();
                for (int v : adj[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        queue.add(v);
                    }
                }
            }
        }

        int drives = (sectors > 0) ? sectors - 1 : 0;
        System.out.println(drives);
    }
}
