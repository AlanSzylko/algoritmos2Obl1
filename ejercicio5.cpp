#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/Heap.cpp"
#include "tads/ListaAdy.cpp"
#include "tads/MFSet.cpp"


using namespace std;


bool funcionComparar(Arista* a, Arista* b){
    return a->peso < b->peso;
}

long long caminoKruskal(GrafoLista* grafo, int cantAristas){
    int cantV = grafo->cantVertices();
    Heap<Arista*> *minHeap = new Heap<Arista*>(cantAristas, funcionComparar);
    MFSet* mfset = new MFSet(cantV + 1);
    for(int i = 1; i <= cantV ; i++){
        Arista* arista = grafo->adyacentes(i);
        while(arista){
            if(arista->origen < arista->destino){
                minHeap->insertar(arista->clonar());
            }
            arista = arista->sig;

        }
    }
    
    long long retorno = 0;
    int cantAristasRet = 0;

    while(!minHeap->estaVacio() && cantAristasRet < cantV - 1 ){
        Arista* arista = minHeap->tope();
        minHeap->eliminarTope();
        int padreOrigen = mfset->find(arista->origen);
        int padreDestino = mfset->find(arista->destino);
        if(padreOrigen == padreDestino) continue;
        retorno += arista->peso;
        cantAristasRet++;
        mfset->merge(padreOrigen, padreDestino);
    }
    if (cantAristasRet < cantV - 1) return -1;
    return retorno;
}

int main()
{
    int cantRefugios;
    int cantSenderos;
    cin >> cantRefugios >> cantSenderos;
    GrafoLista* grafo = new GrafoLista(false, true, cantRefugios);
    int ret = 0;
    if(cantRefugios == 1){
        cout << "0";
        return 0;
    }
    for(int i = 0; i<cantSenderos; i++){
        int origen;
        int destino;
        int peso;
        cin >> origen >> destino >> peso;
        grafo->agregarArista(origen, destino, peso);
    }
    long long kruskal = caminoKruskal(grafo, cantSenderos);
    if(kruskal == -1){
        cout << "imposible";
        return 0;
    }
    cout << kruskal;
    return 0;
}