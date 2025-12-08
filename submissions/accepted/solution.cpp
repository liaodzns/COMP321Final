#include <iostream>
#include <vector>
#include <deque>
#include <sstream>
#include <string>
using namespace std;

/*
 * Tesla Plant – Connected Components
 *
 * We build an undirected graph where nodes are building IDs.
 * Then we count how many connected components contain at least
 * one building from Billy's inspection list. If this number is k,
 * the minimum number of drives between sectors is max(0, k - 1).
 */

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int B, numToInspect;  // number of buildings and number to inspect
    if (!(cin >> B >> numToInspect)) {
        return 0; // no input
    }

    // Read the building IDs to inspect
    vector<int> toInspect;
    for (int i = 0; i < numToInspect; ++i) {
        int id;
        cin >> id;
        toInspect.push_back(id);
    }

    const int MAX_ID = 1000; // IDs are 0 < id < 1000
    vector<vector<int>> adj(MAX_ID + 1);

    // Read building descriptions and build undirected graph
    for (int i = 0; i < B; ++i) {
        string line;
        getline(cin, line);
        if (line.empty()) {
            --i; // ensure we still read B non-empty lines
            continue;
        }

        stringstream ss(line);
        int id, deg;
        ss >> id >> deg;

        for (int j = 0; j < deg; ++j) {
            int nb;
            ss >> nb;
            if (id >= 0 && id <= MAX_ID && nb >= 0 && nb <= MAX_ID) {
                adj[id].push_back(nb);
                adj[nb].push_back(id); // undirected
            }
        }
    }

    vector<bool> visited(MAX_ID + 1, false);
    int sectors = 0;

    // For each building on Billy's list, if its component hasn't
    // been visited yet, BFS from it and count a new sector.
    for (int start : toInspect) {
        if (start < 0 || start > MAX_ID) continue;
        if (visited[start]) continue;

        sectors++;
        deque<int> dq;
        visited[start] = true;
        dq.push_back(start);

        while (!dq.empty()) {
            int u = dq.front();
            dq.pop_front();

            for (int v : adj[u]) {
                if (!visited[v]) {
                    visited[v] = true;
                    dq.push_back(v);
                }
            }
        }
    }

    int drives = (sectors > 0 ? sectors - 1 : 0);
    cout << drives << "\n";

    return 0;
}
