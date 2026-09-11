#include <iostream>
#include <functional>
using namespace std;

template<typename K, typename V>
class TablaHash {
private:
    struct Nodo {
        K clave;
        V valor;
        Nodo* siguiente;
        Nodo(K c, V v){
            clave = c;
            valor = v;
            siguiente = NULL;
        }
    };
    Nodo** tabla;
    int largo;
    int (*funcionDeHash)(K);
    bool (*sonIguales)(K,K);

public:
    TablaHash(int nuevoLargo, int (*funcionDeHashParam)(K), bool (*sonIgualesParam)(K,K)){
        largo = nuevoLargo;
        funcionDeHash = funcionDeHashParam;
        sonIguales = sonIgualesParam;
        tabla = new Nodo*[largo]();
    }
    ~TablaHash() {
        for (int i = 0; i< largo; i++){
            while(tabla[i]){
                Nodo* temp = tabla[i];
                tabla[i] = tabla[i]->siguiente;
                delete temp;
            }
            delete tabla[i];
            tabla[i] = NULL;
        } 
        delete[] tabla;
        tabla = NULL;
    }
    void insertar(K clave, V valor) {
        Nodo* nuevo = new Nodo(clave, valor);
    }

    V buscar(K clave) {
        // Search implementation
    }

    void eliminar(K clave) {
        // Delete implementation
    }
};

