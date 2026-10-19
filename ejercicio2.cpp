#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/TablaHash.cpp"

using namespace std;

int funcionHash(int* k, int l){
    long long ret = 0;
    const long long BASE = 131;
    for(int i = 0; i < 26; i++){
        ret = (ret * BASE + k[i]) % l;
    }
    return (int)ret;
}

bool sonIguales(int* a, int* b){
    for(int i = 0; i<26;i ++){
        if(a[i] != b[i]) return false;
    };
    return true;
}

int* convertirAInt(string p){
    int* pal = new int[26]();
    for (int i =0; i<p.length();i++){
        char l = p[i];
        pal[l - 97]++;
    }
    return pal;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n;
    cin >> n;
    int cantCajones = 0;
    TablaHash tabla(n*10/7, funcionHash, sonIguales);
    for(int i = 0; i < n; i++){
        string p;
        cin >> p;
        int* q = convertirAInt(p);
        if(tabla.insertar(q, 1)){
            cantCajones++;
        }
        else{
            delete[] q;
        }
    }
    int q;
    cin >> q;
    for(int i = 0; i< q; i++){
        string r;
        cin >> r;
        int* s = convertirAInt(r);
        int cant = tabla.buscar(s);
        cout << cant << "\n";
        delete[] s;

    }
    cout << cantCajones << " " << tabla.darCantMax();

    return 0;
    
};