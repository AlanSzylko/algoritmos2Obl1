#include <cassert>
#include <string>
#include <iostream>
#include <limits>
#include "tads/Heap.cpp"

using namespace std;

bool comparar(int a, int b){
    return a<b;
}

int main()
{
    Heap<int>* heap = new Heap<int>(0, comparar);


    return 0;
}