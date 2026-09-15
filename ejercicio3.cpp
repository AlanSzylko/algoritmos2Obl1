#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/Heap.cpp"

using namespace std;

bool Comparar(int a, int b){
    return a<b;
}

    int fusionar(Heap<int>* h, int cant){
        int retorno=0;
        for (int i = 0; i < cant-1; i++)
        {
            int a=h->tope();
            h->eliminarTope();
            int b= h->tope();
            h->eliminarTope();
            int fusion= a+b;
            retorno += fusion;
            h->insertar(fusion);
        }
        return retorno;
        
    }


int main()
{
    int cant;
    cin >> cant;
    Heap<int>* heap = new Heap<int>(cant + 1, Comparar);

    for(int i = 1 ; i<cant + 1 ; i++){
        int agrego;
        cin >> agrego;
        heap->insertar(agrego);
    }

    int r = fusionar(heap, cant);
    cout << r << "\n" << endl;   
     return 0;

}
