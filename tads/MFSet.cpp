#include <iostream>

class MFSet{
    private:
        int* padres;
        int* altura;
        int cantidad;
    public:
        MFSet(int tam){
            padres = new int[tam];
            altura = new int[tam];
            for(int i = 0; i < tam; i++){
                padres[i] = i;
                altura[i] = 0;
            }
            cantidad = tam;

        }
        ~MFSet(){
            delete[] padres;
            delete[] altura;
            padres = altura = NULL;
        }

        int find(int a){
            if(padres[a] = a) return a;
            padres[a] = find(padres[a]);
            return padres[a];
        }

        void merge(int a, int b){
            int padreA = find(a);
            int padreB = find(b);
            if(padreA == padreB) return;
            if(altura[padreA] > altura[padreB]){
                padres[padreB] = padreA;
                return;
            }
            if(altura[padreA] < altura[padreB]){
                padres[padreA] = padreB;
                return;
            }
            padres[padreB] = padreA;
            altura[padreA]++;       
        }
};