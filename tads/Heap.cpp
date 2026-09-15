#include <cassert>
template<typename T>
class Heap{
    private:
    T* arr;
    int capacidad;
    int ultimoOcupado;

    bool (*Comparar)(T, T);

    int padre(int pos){
        return pos / 2;
    }

    int izq(int pos){
        return pos * 2; 
    }

    int der(int pos){
        return (pos * 2) + 1; 
    }

    void swap(int posA, int posB){
        T aux = arr[posA];
        arr[posA] = arr[posB];
        arr[posB] = aux;
    }

    void flotar(int pos)
    {
        if(pos == 1) return;
        int posPadre = padre(pos);
        if(Comparar(arr[pos],arr[posPadre])){
            swap(pos,posPadre);
            flotar(posPadre);
        }
    }
    void hundir(int pos){
        int posIzq = izq(pos);
        int posDer = der(pos);
        if(posIzq > ultimoOcupado) return;
        int posMax = posIzq;
        if(posDer <= ultimoOcupado && Comparar(arr[posDer],arr[posIzq])){
            posMax = posDer;
        }
        if(Comparar(arr[posMax],arr[pos])){
            swap(posMax,pos);
            hundir(posMax);
        }
    }
    public:



    Heap(int capacidad, bool (*Comparar)(T, T)) {
        this->arr = new T[capacidad + 1]();
        this->capacidad = capacidad;
        this->Comparar = Comparar;
        this->ultimoOcupado = 0;

    }

    T tope(){
        assert(!estaVacio());
        return arr[1];

    }
    void eliminarTope(){
        assert(!estaVacio());
        arr[1] = arr[ultimoOcupado];
        ultimoOcupado--;
        hundir(1);
    }

    void insertar(T elem){
        assert(!estaLleno());
        arr[++ultimoOcupado] = elem;
        flotar(ultimoOcupado);
    }

    bool estaLleno(){
        return (capacidad == ultimoOcupado);
    }

    bool estaVacio(){
        return (ultimoOcupado == 0);
    }
};




