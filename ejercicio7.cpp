#include <cassert>
#include <string>
#include <iostream>
#include <limits>

using namespace std;

int* intercalar(int* arr1, int l1, int* arr2, int l2, int& cont) {
  int* ret = new int[l1 + l2];
  int i = 0, j = 0, k = 0;
  while (i < l1 && j < l2) {
    if (arr1[i] < arr2[j]) {
      ret[k] = arr1[i];
      k++;
      i++;
    } else {
      ret[k] = arr2[j];
      int r = i;
      while(r < l1){
        if(arr1[r] > arr2[j]*2) cont++;
        r++;
      };
      k++;
      j++;
    }
  }
  while (i < l1) {
    ret[k++] = arr1[i++];
  }
  while (j < l2) {
    ret[k++] = arr2[j++];
  }
  return ret;
}

int* mergeSort(int* corredores, int inicio, int fin, int& cont){
  if(inicio == fin){
    int* ret = new int[1];
    ret[0] = corredores[inicio];
    return ret;
  }
  int mitad = (inicio + fin) / 2;

  int* ord1 = mergeSort(corredores, inicio, mitad, cont);
  int* ord2 = mergeSort(corredores, mitad + 1, fin, cont);

  int* ret =  intercalar(ord1, mitad-inicio+1 ,ord2, fin-mitad, cont);
  
  return ret;
}

int main(){
  int n;
  cin >> n;
  int* corr = new int[n];
  for(int i = 0; i < n; i++){
    cin >> corr[i];
  };
  int cont = 0;
  int* corrOrdenados = mergeSort(corr, 0, n - 1, cont);
  cout << cont;
  return 0;
};

