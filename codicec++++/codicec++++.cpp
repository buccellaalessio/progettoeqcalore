#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>

using namespace std;

struct Node {
    int id;
    int i, j;
    double x, y;
};

void nestedDissection(const vector<int>& subset, const vector<Node>& allNodes, bool cutVertical, vector<int>& newOrder) {
    if (subset.empty()) return;
    if (subset.size() == 1) {
        newOrder.push_back(subset[0]);
        return;
    }
    int min_val = 1e9;
    int max_val = -1;
    for (int id : subset) {
        int val = cutVertical ? allNodes[id].i : allNodes[id].j;
        if (val < min_val) min_val = val;
        if (val > max_val) max_val = val;
    }
    int mid_val = (min_val + max_val) / 2;
    vector<int> V1, V2, VS;
    for (int id : subset) {
        int val = cutVertical ? allNodes[id].i : allNodes[id].j;
        if (val < mid_val) {
            V1.push_back(id);
        }
        else if (val > mid_val) {
            V2.push_back(id);
        }
        else {
            VS.push_back(id);
        }
    }
    nestedDissection(V1, allNodes, !cutVertical, newOrder);
    nestedDissection(V2, allNodes, !cutVertical, newOrder);
    for (int id : VS) {
        newOrder.push_back(id);
    }
}

int main() {
    int N;
    cout << "Inserisci il valore di N: ";
    if (!(cin >> N) || N <= 0) {
        cerr << "Errore: N deve essere un numero intero positivo." << endl;
        return 1;
    }

    double h = 1.0 / (N + 1);
    int numNodes = N * N;

    vector<Node> nodes(numNodes);
    vector<vector<int>> adjList(numNodes);

    auto getIndex = [N](int i, int j) {
        return (j - 1) * N + (i - 1);
        };

    for (int j = 1; j <= N; ++j) {
        for (int i = 1; i <= N; ++i) {
            int id = getIndex(i, j);
            nodes[id] = { id, i, j, i * h, j * h };
        }
    }

    for (int j = 1; j <= N; ++j) {
        for (int i = 1; i <= N; ++i) {
            int u = getIndex(i, j);
            if (i < N) {
                int v = getIndex(i + 1, j);
                adjList[u].push_back(v);
                adjList[v].push_back(u);
            }
            if (j < N) {
                int v = getIndex(i, j + 1);
                adjList[u].push_back(v);
                adjList[v].push_back(u);
            }
        }
    }

    ofstream coordsFile("coords.txt");
    coordsFile << fixed << setprecision(6);
    for (const auto& node : nodes) {
        coordsFile << node.id << " " << node.i << " " << node.j << " "
            << node.x << " " << node.y << "\n";
    }
    coordsFile.close();

    ofstream connFile("connectivity.txt");
    int e = 0;
    for (int u = 0; u < numNodes; ++u) {
        for (int v : adjList[u]) {
            if (u < v) {
                connFile << e++ << " " << u << " " << v << "\n";
            }
        }
    }
    connFile.close();

    vector<int> initialSubset(numNodes);
    for (int k = 0; k < numNodes; ++k) {
        initialSubset[k] = k;
    }

    vector<int> orderedIndices;
    nestedDissection(initialSubset, nodes, true, orderedIndices);

    ofstream ordFile("ordering.txt");
    for (int m = 0; m < orderedIndices.size(); ++m) {
        ordFile << m << " " << orderedIndices[m] << "\n";
    }
    ordFile.close();

    cout << "Generazione completata con successo:" << endl;
    cout << "- coords.txt" << endl;
    cout << "- connectivity.txt" << endl;
    cout << "- ordering.txt" << endl;

    return 0;
}