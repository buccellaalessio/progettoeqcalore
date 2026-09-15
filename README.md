# progettoeqcalore
Per svolgere il progetto ho scelto di proseguire in 5 passaggi, seguendo essenzialmente le richieste di ogni task. Per ogni parte svolta ho descritto le caratteristiche (IN, OUT) fino a descrivere essenzialmente quanto fatto nei codici. 

### PARTE 1 (generazione griglia e grafo di adiacenza) 
generazione della griglia del dominio tramite discretizzazione escludendo i bordi della griglia e considerandoli collegati solo se vicini. Avendo in INPUT un intero $N$ si vuole ottenere una riga che contenga informazioni sulle coordinate $x$ e $y$ e associazione ad un indice progressivo. Si vuole inoltre generare una riga (avendo sempre lo stesso input $N$) che contenga le liste di arco del grafo di due punti adiacenti (con indice $n_1$ e $n_2$) e di un numero $e$ che numeri gli archi. 
### PARTE 1: Generazione griglia e grafo di adiacenza
Generazione della griglia del dominio tramite discretizzazione escludendo i bordi della griglia e considerandoli collegati solo se vicini. 
* **IDEA DI BASE**: Per svolgere la task ho pesato innanzitutto di definire una struttura dati che rispetti le caratteristiche richieste. Come da richiesta devo implementare un commanndo che mi permetta di scegliere il numero N di nodi e con questo assegnare ad ogni nodo il suo indice n. Infine per ogni nodo (implementando quindi dei cicli for, come nei punti precedenti) dovrò creare una lista di adiacenza dei nodi vicini, inserendo poi esso nella lista dei vicini di questi (il grafo non è orientato). Infine implemento un modo per sovrascrivere i dati nei file. 
* **INPUT**: Un intero $N$ che determina la discretizzazione del quadrato.
* **OUTPUT**: Le coordinate dei punti associate agli indici progressivi e il grafo non orientato.
* **FUNZIONALITÀ RICHIESTE**: Lettura di $N$ scelto, associazione di un indice progressivo e generazione iterativa dei punti interni del dominio determinando le coordinate $i, j, x, y$ della griglia e geometriche. Esportazione dei dati in un file `coords.txt`, generazione del grafo di adiacenza e creazione di un file `connectivity.txt` con la struttura $e$, $u$, $v$.
* **STRUTTURE DATI**: `std::vector` per memorizzare i dati come vettori (si utilizza `using namespace std` per omettere `std::` nel codice) e di una `struct node`.
* **COMPLESSITÀ**: $O(N^2)$ – il tempo è lineare rispetto al numero totale di nodi, che sono $N \times N$.
* **DIPENDENZA DA ALTRI MODULI**: Genera il file `coords.txt` necessario per l'algoritmo di nested dissection della prossima parte. Inoltre, il file `connectivity.txt` contiene informazioni sui nodi ed è necessario per la parte 3, al fine di identificare gli elementi fuori diagonale non nulli della matrice $A$.
* **DESCRIZIONE IMPLEMENTATIVA**: 
  Per svolgere la task è stata creata una `struct node` contenente $n$ come ID, $i$ e $j$ (righe e colonne) come interi e le coordinate spaziali $x$ e $y$ come `double`. Viene acquisito $N$ in input con un controllo `if` per terminare l'esecuzione qualora $N$ non sia un intero positivo; in caso positivo viene calcolato il passo $h$. Si utilizza una funzione lambda `getIndex` che prende le coordinate della griglia e le trasforma nell'indice progressivo. 
  La generazione dei nodi avviene tramite due cicli `for`  (interno per le $i$ ed esterno per le $j$), calcolando ad ogni iterazione le coordinate moltiplicando per il passo $h$. 
  Per la costruzione del grafo di adiacenza ho utilizzato altri cicli `for`: se un punto è a destra o in alto rispetto a un nodo $u$, viene inserito nei nodi adiacenti $v$ (si inizia dunque a "contare" da sinistra ed in basso ed evito così doppi conteggi dei vicini). I nodi $v$ vengono aggiunti alla lista di adiacenza di $u$ (e viceversa) tramite `push_back`. 
  Infine, l'esportazione in `coords.txt` avviene scorrendo tutti i nodi tramite ciclo for, mentre per `connectivity.txt` si utilizza un ciclo for sui nodi $u$ e uno interno sui relativi vicini $v$.
### PARTE 2 (ordinamento dei nodi) 
ottenere una riordinazione dei nodi mediante l'algoritmo di nested dissection (avendo in input le coordinate del punto precedente) che ci restituisca una riga del tipo `n m`, dove il primo è l'indice della task1 mentre $m$ è l'indice intero appartenente a $[0, N^2 - 1]$ del nuovo riordinamento. 

### PARTE 3 (generazione matrice sparsa e termine noto) 
tramite C++ si vuole costruire la matrice $A$ del sistema della nostra equazione approssimata (sia con le coordinate iniziali che con quelle della precedente task). Si avrà quindi come output la matrice $A$ in formato `A.txt`. Inoltre si inglobano i valori di $u$ ai bordi come termine noto. Come input si usano le coordinate e l'ordinamento e l'espressione della funzione sorgente $f$, ottenendo il file dei vettori dei termini noti `rhs.txt`. 

### PARTE 4 (esportazione dati e risoluzione numerica del sistema) 
si vuole risolvere il sistema su Python, per farlo si crea un codice che legga i file `A.txt` e `rhs.txt` e li converta in formato CSC. Inoltre tramite Cholesky si risolve il sistema lineare. 

### PARTE 5 
utilizzando il sistema risolto si vogliono ottenere i tempi ed il numero di entrate, in funzione dell'intero $N$, e confrontare i risultati tra quelli delle coordinate e dell'ordinamento scelto. Infine si vuole ottenere il plot della soluzione e le immagini della struttura della matrice $A$.