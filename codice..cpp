#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
\\
using namespace std;


struct Node {
    int id;       
    int i, j;     
    double x, y;  
};

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

    cout << "Generazione completata con successo usando liste di adiacenza!" << endl;
    cout << "- coords.txt" << endl;
    cout << "- connectivity.txt" << endl;

    return 0;
}