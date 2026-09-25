#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/Heap.cpp"
#include "tads/ListaAdy.cpp"

using namespace std;
struct NodoVertice {
    int prioridad;
    int numero;
};

bool comparar(NodoVertice a, NodoVertice b) {
    if (a.prioridad != b.prioridad) {
        return a.prioridad < b.prioridad;
    }
    return a.numero < b.numero;
}

int main()
{
    int aristas=0;
    int vertices=0;
    cin >> vertices >> aristas;
    int* res = new int[vertices];
    int* prioridad = new int[vertices + 1]();
    int* dependientes = new int[vertices + 1]();
    Heap<NodoVertice>* siguientes = new Heap<NodoVertice>(vertices, comparar);
    GrafoLista grafo(true, false, vertices);
    
    for(int i=0;i<vertices;i++){
        int p;
        cin >> p;
        prioridad[i+1]=p; 
    }

    for(int i=0;i<aristas;i++){
        int origen;
        int destino;
        cin >> origen >> destino;
        grafo.agregarArista(origen,destino); 
        dependientes[destino]++;
    }

    for(int i=1;i<vertices+1;i++){
        if(dependientes[i]==0){
            NodoVertice n;
            n.prioridad = prioridad[i];
            n.numero = i;
            siguientes->insertar(n);
        }
    }

    int guardados = 0;
    while(!siguientes->estaVacio()){
        NodoVertice actual = siguientes->tope();
        siguientes->eliminarTope();



        auto ady = grafo.adyacentes(actual.numero);
        while(ady != nullptr){
            dependientes[ady->destino]--;
            if (dependientes[ady->destino] == 0){
                NodoVertice n;
                n.prioridad = prioridad[ady->destino];
                n.numero = ady->destino;
                siguientes->insertar(n);
            }
            ady = ady->sig;

        }
        res[guardados] = actual.numero;
        guardados++;
        
    }
    if(guardados==vertices){
        for(int i=0; i<vertices; i++){
            cout << res[i] << "\n";
        }
    }
    else{
        cout<< "imposible"<< "\n";
    }
    return 0;
}