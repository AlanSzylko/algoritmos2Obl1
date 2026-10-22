# Bitácora — Obligatorio 1

**Integrantes:** Alan Szylkowski (290025), Tiago Fuhrman (290103)


## 2026-02-09 —  Los dos
- Creamos el repo a partir del template del obl y verificamos el flujo inicial de Git/GitHub, los commits.

## 2026-07-09 — Alan
Empecé el ejercicio 1 y creé en tads -> AVL.h. Definí el nodo genérico y la clase AVL con su raíz.
Hice las funciones altura, balance, rotaciones(izq y der) y equilibrio. Usé altura 0 para una hoja y -1 para un árbol vacío.
Consulté a Codex para entender el funcionamiento y como escribir en codigo templates, struct, class, public y private.

## 2026-10-09 - Tiago
Creé el TAD TablaHash en el archivo TablaHash.cpp. Implementé las declaraciones privadas de la clase y comencé con las públicas, falta bastante.

## 2026-10-09 — Alan
Termine el tad AVL con las funciones rango, búsquedas y recorridos. 
Usé GitHub Copilot como apoyo para comprender la diferencia entre funciones públicas y privadas.
Arranque ej 1, falta terminarlo

## 2026-15-09 - Tiago
Terminé el ejercicio1. Implementé la lógica para chequear la busqueda y el rango. Investigué sobre la utilización del doble ">>" en el cin para asociar a dos variables contiguas. Corrí tests con ayuda de Claude y confirmé que el output esperado y real coincidan.

## 2026-15-09 — Alan
Implemente funciones main y  fusionar, quedo terminado el ejercicio 3

## 2026-22-09 - Tiago
Terminé el TAD TablaHash y el ejercicio 2. Corregí un template inicial que me habia hecho Copilot cuando cree el TAD, borre las funciones que creó (tenía el completado automático) y las hice yo de 0. Creamos una función de dispersión de hash dependiente de la cantidad de letras y su posición en el array, para realizarlo de la forma más dispersa posible. Corrí tests con Claude para confirmar que el output esperado y el obtenido es el mismo.


## 2026-09-25 — Alan
Trabajé el ejercicio 4
  Reutilicé el Heap del ejercicio 3 (con un struct de prioridad y número de
  módulo, y un comparador que desempata por número) y el GrafoLista que armó Tiago. El orden se guarda en un arreglo y se imprime recién al final, porque si hay ciclo no se puede imprimir nada.
  Cree un contador de dependencias por vertice (se suma 1 al destino de cada
  arista). Los módulos con contador 0 entran a un heap. Cada vez que saco uno, lo guardo en el orden y resto 1 a sus vecinos, los que llegan a 0 entran al heap. Al final, si guardé menos de V módulos hay un ciclo y imprimo "imposible".
- Use claude para entender bien la letra y el algoritmo, con un diagrama  me
  ayudó a encontrar los errores de sintaxis, algunos cin <<,  en vez de ->, un = en lugar de == cuando no me compilaban las pruebas.
  Revisé todo y lo probé con los ejemplos.

## 2026-10-11 - Tiago
Realicé la implementación de la clase MFSet en un archivo cpp por separado, dentro de la carpeta de Tads, con las dos optimizaciones vistas. Implementé el algoritmo de Kruskal como vimos en la clase, dentro del ejercicio 5. Por otro lado, separe la definición de arista en un cpp solo ya que me estaba complicando para acceder en distintos archivos. Realicé el ejercicio 5. 

Investigué con Claude el uso de #ifndef, #define, y #endif, ya que me estaba tirando errores de doble definición cuando trataba de complicar. Después de compilar sin errores y hacer un par de ejemplos a mano, corrí pruebas con claude para asegurarme que el resultado esperado y obtenido es el mismo.

## 2026-10-19 — Alan
Ultimos arreglos pre entrega:
Revisé con Tiago los bugs que encontramos contra la letra teniamos overflow en ejercicio3, hash mal distribuido en ejercicio2, y falta de sync_with_stdio en los 5 ejercicios.
Corregí ejercicio3 pasando el heap, el comparador y la suma de fusionar a long long, porque el acumulado superaba el rango de int. En ejercicio2 reemplacé la función de hash por una sobre el array de 26 conteos, porque la
anterior distribuia casi todas las palabras en pocos buckets. Agregué
ios::sync_with_stdio(false) y cin.tie(0) a los 5 main.
Usé Claude para que me explique por qué fallaba cada cosa, mas que nada los long long.

## 2026-10-22 - Tiago
Realicé toda la justificación de órdenes de cada ejercicio.