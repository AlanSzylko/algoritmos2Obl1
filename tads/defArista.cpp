#ifndef DEF_ARISTA
#define DEF_ARISTA

#include <iostream>

    struct Arista{
    int origen;
    int destino;
    int peso;
    Arista* sig;

    Arista(int unOrigen, int unDestino, int unPeso, Arista* unSig = NULL){
        origen = unOrigen;
        peso = unPeso;
        destino = unDestino;
        sig = unSig;
    }

    Arista* clonar(){
        return new Arista(origen, destino, peso);
    }
};

#endif