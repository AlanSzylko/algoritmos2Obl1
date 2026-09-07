#ifndef AVL_H
#define AVL_H

template<typename T>
struct NodoAVL{
    T dato;
    NodoAVL<T>* izq;
    NodoAVL<T>* der;
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

template <typename T>
class AVL {
private:
    NodoAVL<T>* raiz;

    int obtenerAlt(NodoAVL<T>* r) {
        if (r == nullptr) return -1;
        return r->altura;
    }

    void actualizarAlt(NodoAVL<T>* r) {
        if (r == nullptr) return;

        int altDer = obtenerAlt(r->der);
        int altIzq = obtenerAlt(r->izq);

        if (altDer > altIzq) {
            r->altura = 1 + altDer;
        } else {
            r->altura = 1 + altIzq;
        }
    }
    
    int balance(NodoAVL<T>* r) {
        if (r == nullptr) return 0;
        int b = obtenerAlt(r->der) - obtenerAlt(r->izq);
        return b;
    }

    NodoAVL<T>* rotIzq(NodoAVL<T>* r) {
        NodoAVL<T>* b = r->der;
        NodoAVL<T>* c = b->izq;

        b->izq = r;
        r->der = c;

        actualizarAlt(r);
        actualizarAlt(b);
        return b;
    }

    NodoAVL<T>* rotDer( NodoAVL< T>* r){
        NodoAVL<T>* b = r->izq;
        NodoAVL<T>* c = b->der;

        b->der = r;
        r->izq = c;

        actualizarAlt(r);
        actualizarAlt(b);
        return b;
    }

    NodoAVL<T>* equilibrar(NodoAVL<T>* r){
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


public:
    AVL() {
        raiz = nullptr;
    }
};

#endif