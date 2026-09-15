# 37. Práctica: preparar exactamente lo necesario
## Ejercicio 1. Predecí el resultado antes de mirar
Existe un commit inicial en el que `nota.txt` contiene A. Se cambia el contenido a B, se ejecuta `git add nota.txt`, se cambia a C y se ejecuta `git commit -m "Actualizar nota"`.

**Preguntas:** ¿qué contiene el commit nuevo?, ¿qué contiene el archivo de trabajo?, ¿queda algún cambio pendiente?, ¿qué muestran diff y diff --staged?

**Solución:** el nuevo commit contiene B; el directorio de trabajo contiene C. Hay un cambio sin preparar entre B y C. `git diff` lo muestra; `git diff --staged` queda vacío porque el índice coincide con el nuevo commit. Para confirmar C hay que volver a preparar y confirmar.

## Ejercicio 2. Archivo nuevo y archivo seguido
`programa.cpp` ya está seguido y fue modificado. `manual.txt` es nuevo y untracked. Se ejecuta `git commit -am "Actualizar"`.

**Solución:** se confirma la modificación de programa.cpp, pero no manual.txt. Para incluir ambos en un commit normal:
```text
git add programa.cpp manual.txt
git commit -m "Actualizar programa y agregar manual"
```
Si el commit -am ya se hizo, estos comandos incorporan manual.txt en otro commit; no repiten automáticamente la modificación ya registrada.

## Ejercicio 3. Separar dos cambios
Se modificaron `a.txt` y `b.txt` y se ejecutó `git add .`, pero se quiere confirmar solo a.txt. El repositorio tiene un commit previo.
```text
git reset HEAD b.txt
git diff --staged
git commit -m "Actualizar a"
```
**Solución:** el contenido de b.txt se conserva como modificación sin preparar. Usar checkout -- b.txt en su lugar descartaría cambios de trabajo y no expresa el mismo objetivo.

## Ejercicio 4. Ignorar un archivo ya versionado
Un archivo generado `salida.log` quedó en el historial y debe conservarse localmente sin futuras versiones. Se agrega `salida.log` a .gitignore; luego:
```text
git rm --cached salida.log
git add .gitignore
git commit -m "Dejar de versionar el archivo generado"
```
**Solución:** el archivo local permanece, deja de estar en la nueva instantánea y las reglas ayudan a no agregarlo otra vez. Las versiones históricas no desaparecen.

===
# 38. Práctica: ramas, fusión y colaboración
## Ejercicio 5. Deducir qué punteros se mueven
Historia inicial: `A--B`, con master activa. Se crea `tema`, se cambia a ella y se confirma C. Se vuelve a master y se confirma D.
```text
      C  (tema)
     /
A---B
     \
      D  (master, HEAD)
```
**Solución:** crear tema no cambió HEAD; confirmar C movió solo tema; confirmar D movió solo master. La historia divergió. Estando en master, `git merge tema` normalmente crea una fusión de tres vías, no un fast-forward. Si no se hubiera creado D, master podría avanzar hasta C.

## Ejercicio 6. Resolver una diferencia de texto
Master dice «Total con IVA» y tema dice «Importe final» en la misma línea. El resultado acordado es «Importe final con IVA».

**Solución:** ejecutar merge desde la rama destino, abrir el archivo conflictivo, dejar la frase acordada y borrar los marcadores. Revisar el archivo y ejecutar:
```text
git add resumen.txt
git commit -m "Unificar la descripción del importe"
git status
```
Ni la fecha más reciente ni el nombre de la rama deciden por sí solos el contenido correcto.

## Ejercicio 7. Trabajo remoto nuevo
Tu master local tiene L, y el servidor agregó R desde el ancestro común. `push` fue rechazado. Se desea integrar conservando ambas historias.
```text
git checkout master
git fetch origin
git log --oneline --graph --decorate --all
git merge origin/master
git push origin master
```
**Solución:** fetch trae R sin mezclar; merge integra en master, con resolución si hace falta; push publica el resultado. No se propone forzar la publicación porque el objetivo es conservar los dos trabajos.

## Ejercicio 8. Rebase local
Tema tiene C encima de B y master avanzó a D desde B. `git checkout tema` y `git rebase master` reconstruyen C como C' después de D. Tema avanza; master sigue en D hasta que se integre. C' y C no tienen el mismo identificador. Esta práctica se plantea para commits aún no compartidos.

===
# 39. Práctica: ejecutar un flujo completo
## Laboratorio local con la sintaxis de Pro Git
Usá una carpeta de práctica nueva. Las líneas de editar archivos son acciones para realizar en el editor; no son comandos. Elegí tu nombre y correo. No requiere remoto para llegar al tag local.

1. Crear la carpeta, entrar e inicializar Git.
```text
git init
git config user.name "Estudiante"
git config user.email "estudiante@example.com"
```
2. Crear `README.txt` con «Proyecto inicial», prepararlo y confirmar.
```text
git add README.txt
git commit -m "Crear proyecto inicial"
git branch
```
3. Identificar el nombre de la rama principal. Si no es master, usar su nombre en los pasos siguientes. Crear la rama mejora, agregar una línea al README y confirmar.
```text
git checkout -b mejora
git add README.txt
git commit -m "Documentar una mejora"
```
4. Volver a la rama principal e integrar. Si no hubo nuevos commits allí, se espera fast-forward.
```text
git checkout master
git merge mejora
git log --oneline --graph --decorate --all
git branch -d mejora
git tag -a v1.0 -m "Versión de práctica"
git show v1.0
```
**Resultado esperado:** dos commits, el segundo accesible desde la rama principal, la rama mejora eliminada y el tag apuntando al segundo commit. Eliminar mejora no elimina ese trabajo ya integrado.

**Extensión con remoto existente y autorizado:** registrar su URL con `git remote add origin URL`, publicar con `git push -u origin master` y enviar la etiqueta con `git push origin v1.0`. La URL es un marcador que debe sustituirse; el servidor tiene que existir y permitir escritura.

**Comprobación de aprendizaje:** explicá después de cada comando qué cambió: archivo, índice, historial, referencia local o referencia remota. Si no podés decirlo, volvé a las tres áreas de Git.

===
# 40. Práctica conceptual de ingeniería
## Caso 1. Reservas con requisitos inciertos
Una organización quiere una aplicación de reservas, pero los usuarios no tienen claras sus pantallas ni reglas de modificación.

**Respuesta modelo:** usar prototipos para descubrir y validar necesidades y desarrollo incremental para construir funciones prioritarias. Entregar operativamente por partes si esas partes pueden usarse de forma útil. No elegir cascada rígida solo porque facilita documentación: los requisitos inciertos aumentan el retrabajo.

## Caso 2. Controlador crítico
Se debe controlar un dispositivo cuya actuación incorrecta podría producir un accidente.

**Respuesta modelo:** enfatizar confiabilidad, seguridad, requisitos completos y análisis de interacciones. Un proceso planificado y verificación rigurosa resulta justificable. Los prototipos pueden ayudar a explorar riesgos, pero uno desechable no debe convertirse sin más en el controlador de producción. No existe una elección automática basada únicamente en la palabra «crítico».

## Caso 3. Sistema administrativo estándar
Existen productos que cubren casi todas las necesidades de una empresa.

**Respuesta modelo:** evaluar reutilización/COTS: identificar componentes, revisar requisitos negociables, diseñar integración y validar. Ventajas: menos desarrollo; riesgos: ajuste imperfecto y dependencia de la evolución del proveedor.

## Caso 4. Cumple el documento, pero nadie lo puede usar
El sistema implementa cada requisito escrito, pero el flujo hace que los usuarios no puedan completar su trabajo.

**Respuesta modelo:** puede haber conformidad con la especificación y fallar la validación de necesidades o la aceptabilidad. Hay que revisar requisitos y trabajo real; no basta afirmar que pasó las pruebas técnicas.

## Caso 5. Cambio solicitado por el cliente
El cliente pide una nueva función y el programador modifica directamente una versión vieja.

**Respuesta modelo:** la solicitud necesita registro y análisis de impacto; deben identificarse la configuración y versión correctas. SCM evita perder trazabilidad y entregar combinaciones equivocadas. Git conserva versiones, pero el equipo debe establecer el proceso de decisión y entrega.

## Caso 6. Presión para ocultar un fallo
Una persona recibe presión para dar por validado un sistema aunque conoce una falla relevante.

**Respuesta modelo:** identificar riesgos y afectados, mantener integridad de la evidencia y comunicar el problema por los canales adecuados. Considerar interés público, producto, juicio y responsabilidades con cliente y empleador; no reducir la ética a obedecer una orden ni inventar resultados de pruebas.

===
# 41. Repaso de última vuelta
## Veinte asociaciones que conviene dominar
- Software: programas + documentación + configuración.
- Ingeniería de software: producción completa bajo restricciones.
- 1968: conferencia vinculada a la crisis del software.
- Actividades fundamentales: especificación, desarrollo, validación, evolución.
- Especificación: servicios y restricciones; validación: conformidad y necesidades.
- Apoyo del formulario: proyectos, configuración, calidad.
- Cascada: requisitos estables y fases; incremental: versiones y adaptación.
- Prototipo: aprender; entrega incremental: usar partes reales.
- Espiral: riesgos; RUP: concepción, elaboración, construcción, transición.
- SCM: controlar artefactos y cambios; Git: control de versiones.
- Git: distribuido; commits y ramas pueden ser offline.
- init crea repositorio; clone copia uno existente.
- add prepara; commit confirma; push publica.
- commit normal guarda índice; commit -a no incorpora untracked por sí solo.
- status informa; diff compara; log recorre historia; show detalla.
- .gitignore no retira seguimiento existente ni borra el pasado.
- branch crea; checkout cambia; checkout -b hace ambas cosas.
- merge integra EN la rama activa; fast-forward no necesita un commit de fusión.
- fetch obtiene; pull obtiene e integra; origin/master es conocimiento local del remoto.
- rebase reaplica y cambia identificadores; tag no avanza automáticamente.

## Cómo responder un múltiple opción
Leé primero la consigna completa. Identificá si pide la correcta, la incorrecta o la mejor alternativa. Ubicá el concepto antes de leer las letras. Descartá opciones que confundan áreas, actividades o alcances. Si una alternativa usa «siempre» o «únicamente», comprobá si hay un contraejemplo del capítulo.

## Autoevaluación
Podés considerar un tema aprendido si explicás la respuesta sin verla, das un ejemplo nuevo y justificás por qué una alternativa parecida sería incorrecta. En Git, además, tenés que predecir el estado después de una secuencia de comandos.

**Antes del escrito:** revisá especialmente las preguntas 3, 4 y 5 de procesos y las de identidad, CLI, distribución y SCM de tus capturas. Son los puntos donde aparecen errores que se pueden corregir comprendiendo una distinción breve.

===
# 42. Fuentes y cobertura
## Libros aportados
**Ian Sommerville. Ingeniería de software, 9.ª edición, traducción española, 2011.** Capítulo 1: pp. 3-26; capítulo 2: pp. 27-55. En el archivo aportado corresponden a páginas PDF 21-44 y 45-73. El complemento de SCM procede de pp. 682-684, páginas PDF 700-702.

**Scott Chacon y Ben Straub. Pro Git, segunda edición, traducción española.** El archivo identifica la versión 2.1.22-4-g2264d13, de 2021-08-14. Capítulo 1: pp. 9-23; capítulo 2: pp. 24-58; capítulo 3: pp. 59-99. En el PDF corresponden a páginas 14-28, 29-63 y 64-104.

Sitio de referencia indicado en tu programa: https://git-scm.com/book/en/v2. Esta guía se basó en los archivos aportados; no reemplaza sus ejemplos extensos ni reproduce los capítulos completos.

## Control de cobertura del resumen
- Sommerville 1.1: software profesional, productos, atributos, disciplinas, diversidad, fundamentos y Web.
- Sommerville 1.2: responsabilidad profesional y ocho principios éticos.
- Sommerville 1.3: bomba de insulina, pacientes y estación meteorológica.
- Sommerville 2.1: cascada, incremental, reutilización y menciones de desarrollo formal.
- Sommerville 2.2: requisitos, diseño, implementación, validación y evolución.
- Sommerville 2.3: anticipación/tolerancia al cambio, prototipos, entrega incremental y espiral.
- Sommerville 2.4: perspectivas, fases, flujos y prácticas de RUP.
- Pro Git 1: control de versiones, historia, fundamentos, CLI, instalación, configuración y ayuda.
- Pro Git 2: repositorios, seguimiento, diferencias, commits, archivos, log, deshacer, remotos, tags y alias.
- Pro Git 3: ramas, HEAD, merge, conflictos, gestión y flujos, seguimiento remoto y rebase.

## Ilustraciones y preguntas
Se incluyeron 16 recortes de figuras originales con su número, página y explicación. Las figuras de Sommerville mantienen su atribución al libro; la espiral conserva la mención a IEEE que figura allí. Pro Git declara licencia CC BY-NC-SA 3.0; sus recortes se atribuyen a sus autores y a la segunda edición.

Las 24 respuestas se vinculan a tus cuatro capturas. Las 100 preguntas adicionales y los casos de práctica son material de estudio elaborado para esta guía. Las ambigüedades observadas se señalan expresamente: SCM, alcance de «todos» en CLI y formulaciones simplificadas de algunos comandos.

**Límite del alcance:** no se incluyeron como temario adicional los capítulos de Scrum/XP, requisitos avanzados, servidores Git o herramientas avanzadas. Solo se agregaron aclaraciones breves necesarias para comprender las preguntas y ejecutar los flujos básicos.
