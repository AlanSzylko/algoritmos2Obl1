#include <cassert>
#include <string>
#include <iostream>
#include <limits>


#include "tads/AVL.cpp"



using namespace std;

int main()
{
    AVL<long long> monedas;
    AVL<string> pinturas;
    int cant;
    cin >> cant;
    
    for(int i = 0 ; i<cant ; i++){
        string propuesta;
        char coleccion;
        cin >> propuesta >> coleccion;
        if (propuesta=="ALTA"){
            if (coleccion=='P'){
                string pintura;
                cin >> pintura;
                pinturas.insertar(pintura);
            }
           else{
                long long moneda;
                cin >> moneda;
                monedas.insertar(moneda);
            }
        }
            // falta el caso que propuesta es buscar o rango 

    }
}