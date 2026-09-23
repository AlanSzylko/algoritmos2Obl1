#include <iostream>
#include <functional>
using namespace std;

class TablaHash {
private:
    struct Nodo {
        int* clave;
        int valor;
        Nodo* siguiente;
        Nodo(int* c, int v){
            clave = c;
            valor = v;
            siguiente = NULL;
        }
    };
    Nodo** tabla;
    int largo;
    int cantMax = 1;
    int (*funcionDeHash)(int*, int);
    bool (*sonIguales)(int*,int*);

public:

    TablaHash(int nuevoLargo, int (*funcionDeHashParam)(int*, int), bool (*sonIgualesParam)(int*,int*)){
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
                delete[] temp->clave;
                delete temp;
            }
            delete tabla[i];
            tabla[i] = NULL;
        } 
        delete[] tabla;
        tabla = NULL;
    }
    bool insertar(int* clave, int valor) {
        int pos = funcionDeHash(clave, largo);
        bool v = false;
        Nodo* inicio = tabla[pos];
        while(inicio && inicio->siguiente != NULL){
            if(sonIguales(clave, inicio->clave)){
                inicio->valor++;
                if(inicio->valor > cantMax) cantMax = inicio->valor;
                return false;
            }
            inicio = inicio->siguiente;
        }
        if(inicio == NULL){
            Nodo* nuevo = new Nodo(clave, valor);
            tabla[pos] = nuevo;
            v = true;
        }
        else{
            if(sonIguales(clave, inicio->clave)){
                inicio->valor++;
                if(inicio->valor > cantMax) cantMax = inicio->valor;
                return false;
            }
            else{
                Nodo* nuevo = new Nodo(clave, valor);
                nuevo->siguiente = tabla[pos];
                tabla[pos] = nuevo;
                v = true;
            }
        }
        return v;
    }

    int buscar(int* clave){
        int pos = funcionDeHash(clave, largo);
        Nodo* inicio = tabla[pos];
        while(inicio){
            if(sonIguales(clave, inicio->clave)){
                return inicio->valor;
            }
            inicio = inicio->siguiente;
        }
        return 0;
    }

    int darCantMax(){
        return cantMax;
    }

};

