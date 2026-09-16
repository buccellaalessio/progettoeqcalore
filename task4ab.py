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
        
        L = None
        
        try:
           
            print(f"    Calcolo Cholesky...")
            start_cholesky = time.perf_counter()
        
        
            L_prof = my_cholesky(-A)
            if tril(L_prof, -1).nnz == 0:
                L = L_prof.transpose()
            else:
                L = L_prof
                
            time_cholesky = time.perf_counter() - start_cholesky
            
           
            print(f"    Risoluzione sistema...")
            start_solve = time.perf_counter()
            y = spsolve_triangular(L, -rhs, lower=True)
            x = spsolve_triangular(L.T, y, lower=False)
            time_solve = time.perf_counter() - start_solve
            
           
            nnz_L = L.nnz
            
            risultati_profiling.append({
                "N": N,
                "Ordinamento": ord_type,
                "Tempo Cholesky (s)": round(time_cholesky, 5),
                "Tempo Soluzione (s)": round(time_solve, 5),
                "Tempo Totale (s)": round(time_cholesky + time_solve, 5),
                "NNZ (Fill-in)": nnz_L
            })
           
            
        except MemoryError:
            print(f"[!] MEMORY ERROR per N={N} (Ordinamento {ord_type}).")
            
        del A_data, rhs, rows, cols, vals, A, L
print("\n=================== RISULTATI ===================")
for ris in risultati_profiling:
    print(f"N: {ris['N']:<4} | "
          f"Ord: {ris['Ordinamento']:<3} | "
          f"Cholesky: {ris['Tempo Cholesky (s)']:<10} | "
          f"Soluzione: {ris['Tempo Soluzione (s)']:<10} | "
          f"Totale: {ris['Tempo Totale (s)']:<10} | "
          f"NNZ: {ris['NNZ (Fill-in)']}")
print("=================================================\n")


N_plot = 32
plt.figure(figsize=(10, 5)) 

for i, ord_type in enumerate(ordinamenti):
    file_A = f"{percorso_cpp}\\A{N_plot}.{ord_type}.txt"
    try:
        A_data = np.loadtxt(file_A)
        rows = A_data[:, 0].astype(int)
        cols = A_data[:, 1].astype(int)
        vals = A_data[:, 2]
        
        n_size = int(max(rows.max(), cols.max())) + 1
        A = csc_matrix((vals, (rows, cols)), shape=(n_size, n_size))
        
        plt.subplot(1, 2, i + 1)
        plt.spy(A, markersize=0.5, color='blue') 
        plt.title(f"Struttura Matrice A\nOrdinamento {ord_type} (N={N_plot})")
        
    except FileNotFoundError:
        print(f"[!] Impossibile trovare i file per il plot SPY (N={N_plot}, Ord={ord_type}).")

plt.tight_layout()
plt.show()



N_sol = 32
ord_sol = "1"  

file_A_sol = f"{percorso_cpp}\\A{N_sol}.{ord_sol}.txt"
file_rhs_sol = f"{percorso_cpp}\\rhs{N_sol}.{ord_sol}.txt"
file_ord_sol = f"{percorso_cpp}\\ordering{N_sol}.txt"

try:
    A_data = np.loadtxt(file_A_sol)
    rhs = np.loadtxt(file_rhs_sol)
    
    rows = A_data[:, 0].astype(int)
    cols = A_data[:, 1].astype(int)
    vals = A_data[:, 2]
    
    n_size = int(max(rows.max(), cols.max())) + 1
    A_sol = csc_matrix((vals, (rows, cols)), shape=(n_size, n_size))
    
    L_prof_sol = my_cholesky(-A_sol)
    if tril(L_prof_sol, -1).nnz == 0:
        L_sol = L_prof_sol.transpose()
    else:
        L_sol = L_prof_sol
        
    y = spsolve_triangular(L_sol, -rhs, lower=True)
    x = spsolve_triangular(L_sol.T, y, lower=False)
    
    
    if ord_sol == "1":
        ord_data = np.loadtxt(file_ord_sol)
        m_nuovi = ord_data[:, 0].astype(int)
        n_originali = ord_data[:, 1].astype(int)
        
        U_natural = np.zeros_like(x)
        U_natural[n_originali] = x[m_nuovi]
        U = U_natural.reshape((N_sol, N_sol))
    else:
        U = x.reshape((N_sol, N_sol))
    
    plt.figure(figsize=(7, 6))
    plt.imshow(U, extent=[0, 1, 0, 1], origin='lower', cmap='inferno', interpolation='bicubic')
    plt.colorbar(label='Temperatura $u(x,y)$')
    plt.title(f"Distribuzione della Temperatura (N={N_sol})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    
except FileNotFoundError:
    print(f"[!] Errore: Assicurati che i file A, rhs e ordering per N={N_sol} siano sul desktop.")
