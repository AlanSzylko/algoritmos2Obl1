from pathlib import Path
import json
R=Path(__file__).resolve().parent
old=R.joinpath('summary_content.txt').read_text(encoding='utf-8').split('\n===\n')
def pages(file):return R.joinpath(file).read_text(encoding='utf-8').strip().split('\n===\n')
intro=pages('course_intro.txt')
topics={1:pages('course_t1.txt')+old[1:6],2:pages('course_t2.txt')+old[6:9],3:pages('course_t3.txt')+old[9:11],4:pages('course_t4.txt')+old[11:13],5:pages('course_t5.txt')+old[13:15],6:pages('course_t6.txt')+old[15:19],7:pages('course_t7.txt')+old[19:24]+pages('course_extra_t7.txt')}
titles={1:'Espacios vectoriales',2:'Transformaciones lineales',3:'Matriz asociada',4:'Cambio de base',5:'Semejanza y rango',6:'Valores y vectores propios (vvp)',7:'Diagonalización'}
book=[intro[0],'INDEX']+intro[1:]
chapter_ranges={}
for n,pp in topics.items():
    first=len(book)+1
    book.extend(pp)
    chapter_ranges[n]=(first,len(book))
book.append(old[24].replace('# Repaso final: qué usar en cada pregunta','# Consulta final: fórmulas y controles'))
consult=len(book)
index=['# Índice y recorrido de aprendizaje','## Herramientas previas','Ecuaciones, matrices, determinantes y aritmética compleja: páginas 3-4. Son herramientas de apoyo para leer los siete temas sin tener que reconstruir los procedimientos de cálculo.']
for n in range(1,8):
    a,b=chapter_ranges[n]
    index.extend([f'## {n}. {titles[n]} | páginas {a}-{b}',{
    1:'Axiomas, ejemplos de espacios finitos e infinitos, subespacios, generación, independencia y sus equivalencias, bases, dimensión, isomorfismo de coordenadas, suma e intersección, suma directa. Práctico 1: ejercicios 1.1-1.6.',
    2:'Linealidad, ejemplos del manuscrito, núcleo e imagen como subespacios, preimágenes, inyectividad, sobreyectividad, inversa y prueba del teorema rango-nulidad. Práctico 1: 1.7-1.10.',
    3:'Construcción por columnas, demostración de la propiedad fundamental, composición, identidad, inversa y ejemplo con bases no canónicas. Práctico 1: 1.11, 1.12 y 1.13(e).',
    4:'Dirección del pasaje, ejemplo original, fórmulas general y particular, cambios en espacios de dimensiones distintas. Práctico 1: 1.13(f,g) y 1.14.',
    5:'Relación de equivalencia, invariantes, rango de productos, operaciones elementales, igualdad de rango por filas y columnas y menores. Práctico 1: 1.15-1.16.',
    6:'Definiciones, sistemas propios, polinomio característico y sus coeficientes, semejanza y traspuesta, geometría y propiedades. Práctico 2: 2.1-2.6.',
    7:'Equivalencias de diagonalización, independencia de subespacios propios, multiplicidades, pruebas de la desigualdad y del criterio completo, parámetros y potencias. Práctico 2: 2.7-2.12.'}[n]])
index.extend(['## Consulta y correspondencia con los originales',f'Fórmulas y controles: página {consult}. Cobertura de los apuntes y ubicación de los ejercicios: páginas {consult+1}-{consult+3}. El panel de marcadores del PDF permite abrir directamente cada sección.'])
book[1]='\n\n'.join(index)
def locate(prefix):
    return next(i+1 for i,p in enumerate(book) if p.strip().splitlines()[0]==prefix)
def pr(n):
    a,b=chapter_ranges[n];return f'{a}-{b}'
coverage1=f'''# Correspondencia con los originales: temas 1-2

## Tema 1: «01-Espacios vectoriales (repaso) 2026_v1.pdf»

**Pp. 1-6:** concepto de vector, operaciones, axiomas y estructura (V,K,+,·). Desarrollo en «Espacios vectoriales: definición completa», página {locate('# 1. Espacios vectoriales: definición completa')}.

**Pp. 7-15:** plano x-3y+2z=0; matrices; polinomios; funciones continuas; escalares complejos; polinomios con raíz 3; criterio de subespacio. Desarrollo en «Matrices, polinomios y funciones como vectores» y «Subespacios y subespacio generado», páginas {locate('# 1. Matrices, polinomios y funciones como vectores')}-{locate('# 1. Subespacios y subespacio generado')}. La multiplicación compleja de p. 11 se trabaja en la página 4.

**Pp. 16-22:** combinación lineal, generación, ejemplos, independencia, equivalencias y ampliación de una lista L.I. Desarrollo en «Subespacios y subespacio generado» e «Independencia: equivalencias y crecimiento», páginas {locate('# 1. Subespacios y subespacio generado')}-{locate('# 1. Independencia: equivalencias y crecimiento')}.

**Pp. 23-29:** dimensión finita e infinita, bases, monomios y base trasladada, coordenadas, ejemplo numérico, isomorfismo y extensión de bases. Desarrollo en «Bases, dimensión y extensión» y «Bases de polinomios y coordenadas», páginas {locate('# 1. Bases, dimensión y extensión')}-{locate('# 1. Bases de polinomios y coordenadas')}. El ejemplo infinito se encuentra también en la página {locate('# 1. Matrices, polinomios y funciones como vectores')}.

**Pp. 30-38:** suma, intersección, ejemplo de los planos coordenados, procedimientos, prueba completa del teorema de dimensiones y suma directa. Desarrollo en páginas {locate('# 1. Suma e intersección: prueba del teorema')}-{locate('# 1. Suma directa y aplicaciones complejas')}.

## Tema 2: «2-repaso transformaciones lineales.pdf»

**Pp. 1-2:** definición, superposición, proyección, rotación, traslación, derivación y T(0)=0. Desarrollo en «Linealidad: definición, alcance y ejemplos», página {locate('# 2. Linealidad: definición, alcance y ejemplos')}.

**Pp. 3-5:** definiciones y pruebas de núcleo e imagen como subespacios, imágenes de los ejemplos, T_A y sistemas homogéneos/no homogéneos, matriz [[2,-1],[-4,2]]. Desarrollo en «Núcleo e imagen: definiciones y pruebas», página {locate('# 2. Núcleo e imagen: definiciones y pruebas')}.

**P. 6:** inyectividad y núcleo trivial, sobreyectividad, biyectividad, inversa y caso matricial. Desarrollo en «Invertibilidad y teorema de la dimensión» y las aplicaciones de 1.10; la prueba de la matriz inversa también aparece en el tema 3.

**Pp. 7-9:** imágenes de generadores, prueba del teorema rango-nulidad y ejemplos de rango. Desarrollo en «Invertibilidad y teorema de la dimensión», página {locate('# 2. Invertibilidad y teorema de la dimensión')}, y ejercicio 1.10(a).'''
coverage2=f'''# Correspondencia con los originales: temas 3-7

## Tema 3: «3-matriz asociada.pdf»

**Pp. 1-2:** construcción y notación de la matriz. **Pp. 3-5:** propiedad fundamental y demostración por coordenadas. **P. 6:** equivalencia entre transformación y multiplicación por una matriz. Se desarrollan en la página {locate('# 3. De una transformación a su matriz')}.

**Pp. 7-9:** composición, identidad, inversa y sus matrices, con demostraciones. Se desarrollan en la página {locate('# 3. Composición, identidad e inversa: pruebas')}. El capítulo completo, con ejemplos y práctico, ocupa las páginas {pr(3)}.

## Tema 4: «4-cambio de base.pdf»

**Pp. 1-2:** identidad, dirección del pasaje, inversa y ejemplo de bases ((1,0),(0,1)) y ((1,1),(1,2)). **P. 3:** A'=Q⁻¹AP. **P. 4:** A'=P⁻¹AP y semejanza. Desarrollo en página {locate('# 4. Cambio de base: derivación y ejemplo original')}, con aplicaciones en el resto del capítulo, páginas {pr(4)}.

## Tema 5: «5-semejanza y rango.pdf»

**P. 1:** semejanza como equivalencia e invariantes. **Pp. 2-3:** imagen por columnas, definición de rango, cotas, núcleo y productos. Desarrollo en página {locate('# 5. Semejanza y rango: fundamentos')} y ejercicio 1.15.

**Pp. 3-6:** ejemplo 3×4, operaciones elementales como matrices invertibles, forma escalonada y rango por filas. Desarrollo y justificaciones en página {locate('# 5. Escalerización y rango por filas')}; ejercicios de menores en 1.16. Al usar una matriz escalerizada, se distingue su imagen de la imagen de la matriz original.

## Tema 6: «vvp.pdf»

**Pp. 1-3:** definiciones, interpretación, subespacio propio y equivalencias con el sistema homogéneo y el determinante. Desarrollo en página {locate('# 6. Valores propios: del operador al sistema')}.

**Pp. 4-5:** polinomio, grado, coeficientes, invariancia por semejanza y traspuesta, polinomio del operador. Desarrollo en página {locate('# 6. Polinomio característico: todos los coeficientes clave')}. Capítulo con aplicaciones: páginas {pr(6)}.

## Tema 7: «7-Diagonalizacion.pdf»

**Pp. 1-3:** base propia, diagonalización matricial y contraejemplos. **Pp. 4-5:** independencia para valores distintos, corolario y ejemplo polinómico. **Pp. 6-7:** multiplicidades y desigualdades. **P. 8:** condición necesaria y suficiente y caso complejo. Desarrollo completo con pruebas en páginas {chapter_ranges[7][0]}-{chapter_ranges[7][0]+3}; aplicaciones y prácticos en el resto del capítulo.'''
coverage3='''# Prácticos completos y alcance del apunte

## Práctico Tema 1: ubicación de los ejercicios

**1.1-1.6:** capítulo 1. Se incluyen las matrices generadoras, el parámetro a, las tres bases de subespacios, las dos bases para coordenadas, los tres casos de suma/intersección y los tres de suma directa. Los incisos complejos 1.5(c) y 1.6(c) están en «Suma directa y aplicaciones complejas».

**1.7-1.10:** capítulo 2. La simetría y la multiplicación por una matriz compleja se resuelven en «Práctico 1: simetría y matrices complejas». Evaluación, multiplicación de polinomios y el caso no lineal se resuelven en las aplicaciones. Se desarrollan íntegramente los operadores 1.8 y 1.9 y las dos demostraciones de 1.10.

**1.11-1.12:** capítulo 3; **1.13:** capítulos 3 y 4, junto con su conexión con diagonalización en el 7; **1.14:** capítulo 4, continuando el operador de matrices de 1.9; **1.15-1.16:** capítulo 5, con todas las propiedades e identificación de menores invertibles.

## Práctico Tema 2: ubicación de los ejercicios

**2.1-2.6:** capítulo 6. Se incluyen los dos controles de vector propio, las tres interpretaciones geométricas, los cinco verdadero/falso, las tres matrices sobre R y C, las propiedades de potencias/inversa/desplazamientos/polinomios y los tres incisos sobre sumas de filas. El original salta de (e) a (g) en 2.5; se incluye también ese último inciso.

**2.7:** capítulo 7, casos reales (a,b) y caso complejo (c). **2.8:** capítulo 7, las cuatro matrices; la tercera se desarrolla junto a multiplicidades repetidas y las restantes en las páginas finales del capítulo. **2.9-2.12:** capítulo 7, con prueba para simétricas 2×2, discusión en a, caso de único valor propio y discusión en α con cálculo de A¹³.

## Qué se tomó de cada material

Se desarrollan los contenidos teóricos de los siete apuntes, incluidos los resultados que en las diapositivas se enuncian brevemente, los ejemplos y las demostraciones presentes en ellas. Las repeticiones de una misma definición se reúnen en un único desarrollo. Los ejercicios conservan la numeración de los originales y sus enunciados se expresan en forma abreviada antes de resolverlos.

Los apoyos sobre Gauss, determinantes, complejos, comparación de tamaños de bases y las pruebas adicionales completan pasos necesarios para comprender los temas. No se agregan otras unidades del curso, como Jordan, producto interno o mínimos cuadrados, que no estaban entre los archivos indicados para este documento.

Dominar este apunte significa comprender y poder aplicar lo aquí desarrollado. Para comprobarlo, rehacé los ejercicios sin consultar las soluciones y explicá en voz alta las hipótesis y el razonamiento de cada demostración; reconocer una fórmula al leerla no equivale a saber usarla en un problema nuevo.'''
book.extend([coverage1,coverage2,coverage3])
R.joinpath('course_content.txt').write_text('\n===\n'.join(book),encoding='utf-8')
manifest={'pages':len(book),'chapters':chapter_ranges,'sections':[{'page':i+1,'title':p.strip().splitlines()[0].removeprefix('# ').removeprefix('TITLE '),'chars':len(p)} for i,p in enumerate(book)]}
R.joinpath('course_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Expected pages:',len(book),'Longest page:',max(len(p) for p in book))
