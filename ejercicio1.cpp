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
        if (propuesta =="BUSCAR"){
            if(coleccion=='P'){
                string pintura;
                cin >> pintura;
                if(pinturas.buscar(pintura)){
                    cout << "si" << "\n";
                }
                else{
                    cout << "no" << "\n";
                }
            }
            else{
                long long moneda;
                cin >> moneda;
                if(monedas.buscar(moneda)){
                    cout << "si"<< "\n";
                }
                else{
                    cout << "no"<< "\n";
                }
            }
        }
        if(propuesta == "RANGO"){
            if(coleccion=='P'){
                string pinturaDesde;
                string pinturaHasta;
                cin >> pinturaDesde >> pinturaHasta;
                pinturas.rango(pinturaDesde,pinturaHasta);
            }
            else{
                long long monedaDesde;
                long long monedaHasta;
                cin >> monedaDesde >> monedaHasta;
                monedas.rango(monedaDesde,monedaHasta);
            }
        }
    }
}