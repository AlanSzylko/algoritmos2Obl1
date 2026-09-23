#include <iostream>
#include <cassert>

class GrafoLista{
    private:
    struct Arista{
        int origen;
        int destino;
        int peso;
        Arista* sig;
        Arista(int unOrigen, int unDestino, int unPeso, Arista* unSig = nullptr){
            this->destino = unDestino;
            this->origen = unOrigen;
            this->peso = unPeso;
            this->sig = unSig;
        }
    };
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
        return vertices[vertice]; //aca se puede acceder a la memoria real. Chequear forma de pasarlo por copia (clonar la lista).
    }

    //Arista* clonar(Arista* a)

    int cantVertices(){
        return cantidadVertices;
    }

   /* void BFS(int inicio, GrafoLista* grafo){
        Queue<int>* cola = new Queue<int>();
        int cantV = grafo->cantVertices();
        bool* visitados = new bool[cantV + 1];
        cola->encolar(inicio);
        visitados[inicio] = true;
        while(!cola->estaVacia()){
            int v = cola->descencolar();
            cout << "Procesando:" << v << endl;
            Arista* ady = grafo->adyacentes(vertice);
            while(ady){
                if(!visitados[ady->destino]){
                    cola->encolar(ady->destino);
                    
                }
            }
        }

    }
    */
};