#ifndef LISTA_ADY
#define LISTA_ADY

#include <iostream>
#include <cassert>
#include "defArista.cpp"

class GrafoLista{
    private:
    bool dirigido;
    bool ponderado;
    int cantidadVertices;
    Arista** vertices;
    
    public:
    GrafoLista(bool esDirigido, bool esPonderado, int cantV){
        dirigido = esDirigido;
        ponderado = esPonderado;
        cantidadVertices = cantV;
        vertices = new Arista*[cantV + 1];
        for(int i = 0; i<cantV+1; i++){
            vertices[i] = nullptr;
        }
    };

    void agregarArista(int origen, int destino, int peso = 1){
        assert(ponderado || peso == 1);
        Arista* nuevaArista = new Arista(origen, destino, peso);
        nuevaArista->sig = vertices[origen];
        vertices[origen] = nuevaArista;
        if(!dirigido){
            vertices[destino] = new Arista(destino, origen, peso, vertices[destino]);
        }
    }

    Arista* adyacentes(int vertice){
        return vertices[vertice]; 
    }

    int cantVertices(){
        return cantidadVertices;
    }
};

#endif