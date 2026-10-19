#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/Heap.cpp"

using namespace std;

bool Comparar(long long a, long long b){
    return a<b;
}

        long long fusionar(Heap<long long>* h, int cant){
            long long retorno=0;
            for (int i = 0; i < cant-1; i++)
            {
                long long a=h->tope();
                h->eliminarTope();
                long long b= h->tope();
                h->eliminarTope();
                long long fusion= a+b;
                retorno += fusion;
                h->insertar(fusion);
            }
            return retorno;
        }


int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);

    int cant;
    cin >> cant;
    Heap<long long>* heap = new Heap<long long>(cant + 1, Comparar);

    for(int i = 1 ; i<cant + 1 ; i++){
        long long agrego;
        cin >> agrego;
        heap->insertar(agrego);
    }

        long long r =fusionar(heap, cant);
        cout <<r <<"\n";

}
