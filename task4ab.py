import numpy as np
from scipy.sparse import csc_matrix, tril
from scipy.sparse.linalg import spsolve_triangular
from sksparse.cholmod import cholesky

# Percorso dei file generati dal C++
percorso_cpp = r"C:\Users\bccls\Desktop"

def my_cholesky(A):
    factor = cholesky(A, order="natural")
    if isinstance(factor, tuple):
        if hasattr(factor[0], 'L'):
            return factor[0].L() 
        return factor[0]         
    return factor.L()

valori_N = [32, 64, 128, 256, 512, 1024]
ordinamenti = ["0", "1"]

print("Avvio caricamento, fattorizzazione e risoluzione...")

for N in valori_N:
    for ord_type in ordinamenti:
        
        # Controllo di sicurezza per evitare il crash di memoria con l'ordinamento naturale grande
        if N >= 256 and ord_type == "0":
            print(f"[-] Salto N={N} con ordinamento naturale (0) per salvaguardare la RAM.")
            continue
            
        file_A = f"{percorso_cpp}\\A{N}.{ord_type}.txt"
        file_rhs = f"{percorso_cpp}\\rhs{N}.{ord_type}.txt"
        
        try:
            A_data = np.loadtxt(file_A)
            rhs = np.loadtxt(file_rhs)
        except FileNotFoundError:
            continue
            
        rows = A_data[:, 0].astype(int)
        cols = A_data[:, 1].astype(int)
        vals = A_data[:, 2]
        
        n_size = int(max(rows.max(), cols.max())) + 1
        A = csc_matrix((vals, (rows, cols)), shape=(n_size, n_size))
        
        try:
            print(f"--> Elaborazione per N={N} (Ord: {ord_type})...")
            
            # 1. Fattorizzazione di Cholesky su -A
            L_prof = my_cholesky(-A)
            if tril(L_prof, -1).nnz == 0:
                L = L_prof.transpose()
            else:
                L = L_prof
                
            # 2. Risoluzione del sistema lineare triangolare
            y = spsolve_triangular(L, -rhs, lower=True)
            x = spsolve_triangular(L.T, y, lower=False)
            
            print(f"    Sistema risolto con successo! (Elementi non nulli in L: {L.nnz})")
            
        except MemoryError:
            print(f"[!] MEMORY ERROR per N={N} (Ordinamento {ord_type}).")
            
        del A_data, rhs, rows, cols, vals, A, L