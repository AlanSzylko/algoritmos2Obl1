#ifndef AVL_IMP
#define AVL_IMP

#include <iostream>

template <typename T>
class AVL {
private:
    struct NodoAVL{
        T dato;
        NodoAVL* izq;
        NodoAVL* der;
        int altura;

        //constructor
        NodoAVL(T valor)
        {
            dato = valor;
            izq = NULL;
            der = NULL;
            altura = 0;
        }
    };
    NodoAVL* raiz;
    NodoAVL* minimo(NodoAVL* r){
        while (r->izq != nullptr) {
            r = r->izq;
        }
        return r;
    }

    int obtenerAlt(NodoAVL* r) {
        if (r == nullptr) return -1;
        return r->altura;
    }

    void actualizarAlt(NodoAVL* r) {
        if (r == nullptr) return;

        int altDer = obtenerAlt(r->der);
        int altIzq = obtenerAlt(r->izq);

        if (altDer > altIzq) {
            r->altura = 1 + altDer;
        } else {
            r->altura = 1 + altIzq;
        }
    }
    
    int balance(NodoAVL* r) {
        if (r == nullptr) return 0;
        int b = obtenerAlt(r->der) - obtenerAlt(r->izq);
        return b;
    }

    NodoAVL* rotIzq(NodoAVL* r) {
        NodoAVL* b = r->der;
        NodoAVL* c = b->izq;

        b->izq = r;
        r->der = c;

        actualizarAlt(r);
        actualizarAlt(b);
        return b;
    }

    NodoAVL* rotDer( NodoAVL* r){
        NodoAVL* b = r->izq;
        NodoAVL* c = b->der;

        b->der = r;
        r->izq = c;

        actualizarAlt(r);
        actualizarAlt(b);
        return b;
    }

    NodoAVL* equilibrar(NodoAVL* r){
        if(r == nullptr) return r;
        actualizarAlt(r);
        int b = balance(r);
        if (b > 1) {
            if (balance(r->der) < 0) {
                r->der = rotDer(r->der);
            }
            return rotIzq(r);
        }

        if (b < -1) {
            if (balance(r->izq) > 0) {
                r->izq = rotIzq(r->izq);
            }
            return rotDer(r);
        }

        return r;        
    }




    NodoAVL* insertarRec(NodoAVL* r, T dato){
        if(!r)return new NodoAVL(dato);
        if(r->dato > dato) r->izq=insertarRec(r->izq, dato);
        else if(r->dato < dato) r->der = insertarRec(r->der, dato);  
        else {
            return r;
        }
        return equilibrar(r);

    }


    void destruir(NodoAVL* r){
        if(r==nullptr) return;
        destruir(r->der);
        destruir(r->izq);
        delete r;
        r=nullptr;

    }

    void rangoRec(NodoAVL* r, T inf, T sup){
        if(r==nullptr) return;
        if(r->dato > inf) {
            rangoRec(r->izq, inf, sup);
        }
        if (r->dato >= inf && r->dato <= sup) {
            std::cout << r->dato << '\n';
        }
        if(r->dato < sup) {
            rangoRec(r->der, inf, sup);
        }
    }

    bool buscarRec(NodoAVL* r, T dato){

        if(r==nullptr) return false;
        if(r->dato > dato) return buscarRec(r->izq, dato);
        else if(r->dato < dato) return buscarRec(r->der, dato);
        return true;
    }



public:
    AVL() {
        raiz = nullptr;
    }

    void insertar(T dato){
        raiz = insertarRec(raiz, dato);
    }


    ~AVL()
    {
        destruir(raiz);
    }

    bool esVacio(){
        return (raiz==nullptr);
    }
    
    int altura(){
        return obtenerAlt(raiz);
    }

    bool buscar(T dato){
        return buscarRec(raiz, dato);
    }

    void rango(T inf, T sup){
        rangoRec(raiz, inf, sup);
    }



};

   


#endif