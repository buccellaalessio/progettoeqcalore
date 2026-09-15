# progettoeqcalore
Per svolgere il progetto ho scelto di proseguire in 5 passaggi, seguendo essenzialmente le richieste di ogni task. Per ogni parte svolta ho descritto le caratteristiche (IN, OUT) fino a descrivere essenzialmente quanto fatto nei codici. 

### PARTE 1 (generazione griglia e grafo di adiacenza) 
generazione della griglia del dominio tramite discretizzazione escludendo i bordi della griglia e considerandoli collegati solo se vicini. Avendo in INPUT un intero $N$ si vuole ottenere una riga che contenga informazioni sulle coordinate $x$ e $y$ e associazione ad un indice progressivo. Si vuole inoltre generare una riga (avendo sempre lo stesso input $N$) che contenga le liste di arco del grafo di due punti adiacenti (con indice $n_1$ e $n_2$) e di un numero $e$ che numeri gli archi. 

### PARTE 2 (ordinamento dei nodi) 
ottenere una riordinazione dei nodi mediante l'algoritmo di nested dissection (avendo in input le coordinate del punto precedente) che ci restituisca una riga del tipo `n m`, dove il primo è l'indice della task1 mentre $m$ è l'indice intero appartenente a $[0, N^2 - 1]$ del nuovo riordinamento. 

### PARTE 3 (generazione matrice sparsa e termine noto) 
tramite C++ si vuole costruire la matrice $A$ del sistema della nostra equazione approssimata (sia con le coordinate iniziali che con quelle della precedente task). Si avrà quindi come output la matrice $A$ in formato `A.txt`. Inoltre si inglobano i valori di $u$ ai bordi come termine noto. Come input si usano le coordinate e l'ordinamento e l'espressione della funzione sorgente $f$, ottenendo il file dei vettori dei termini noti `rhs.txt`. 

### PARTE 4 (esportazione dati e risoluzione numerica del sistema) 
si vuole risolvere il sistema su Python, per farlo si crea un codice che legga i file `A.txt` e `rhs.txt` e li converta in formato CSC. Inoltre tramite Cholesky si risolve il sistema lineare. 

### PARTE 5 
utilizzando il sistema risolto si vogliono ottenere i tempi ed il numero di entrate, in funzione dell'intero $N$, e confrontare i risultati tra quelli delle coordinate e dell'ordinamento scelto. Infine si vuole ottenere il plot della soluzione e le immagini della struttura della matrice $A$.