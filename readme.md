### PyJava: Compilador de Java con Traducción a Python

## Índice

- [Introducción](#introducción)
- [¿Qué es un Compilador?](#qué-es-un-compilador)
- [Características de PyJava](#características-de-pyjava)
- [Componentes del Compilador](#componentes-del-compilador)

- [Analizador Léxico](#analizador-léxico)
- [Analizador Sintáctico](#analizador-sintáctico)
- [Analizador Semántico](#analizador-semántico)
- [Traductor Java a Python](#traductor-java-a-python)



- [Tecnologías y Librerías](#tecnologías-y-librerías)
- [Instalación](#instalación)
- [Uso](#uso)

- [Interfaz Principal](#interfaz-principal)
- [Análisis Léxico](#análisis-léxico)
- [Análisis Sintáctico](#análisis-sintáctico)
- [Análisis Semántico](#análisis-semántico)
- [Traducción a Python](#traducción-a-python)



- [Estructura del Proyecto](#estructura-del-proyecto)
- [Autores](#autores)
- [Licencia](#licencia)
- [Contribuciones](#contribuciones)


## Introducción

PyJava es un compilador educativo que permite analizar código Java y traducirlo a Python. Desarrollado como herramienta didáctica, PyJava implementa las fases fundamentales de un compilador: análisis léxico, sintáctico y semántico.

Este proyecto está diseñado para ayudar a estudiantes y profesionales a comprender el funcionamiento interno de los compiladores, visualizando cada etapa del proceso de compilación a través de una interfaz gráfica intuitiva desarrollada con Flet.

## ¿Qué es un Compilador?

Un compilador es un programa informático que traduce código escrito en un lenguaje de programación (el lenguaje fuente) a otro lenguaje (el lenguaje objetivo). El proceso de compilación consta de varias fases:

1. **Análisis Léxico**: Convierte el código fuente en tokens (unidades léxicas).
2. **Análisis Sintáctico**: Organiza los tokens en una estructura jerárquica (árbol sintáctico).
3. **Análisis Semántico**: Verifica la coherencia semántica del código.
4. **Generación de Código Intermedio**: Crea una representación intermedia del programa.
5. **Optimización**: Mejora el código intermedio.
6. **Generación de Código Objetivo**: Produce el código en el lenguaje destino.


PyJava implementa las tres primeras fases y añade una funcionalidad de traducción directa de Java a Python.

## Características de PyJava

- **Interfaz gráfica intuitiva** desarrollada con Flet (basado en Flutter)
- **Análisis léxico** con identificación de tokens y detección de errores
- **Análisis sintáctico** con generación visual de árboles sintácticos
- **Análisis semántico** con tabla de símbolos y verificación de tipos
- **Traducción de Java a Python** con soporte para estructuras básicas
- **Carga de archivos** Java externos
- **Visualización de errores** en cada fase del análisis
- **Diseño modular** que facilita la comprensión del proceso de compilación


## Componentes del Compilador

### Analizador Léxico

El analizador léxico (implementado en `analizador_lexico.py`) es la primera fase del compilador. Su función es:

1. **Tokenización**: Divide el código fuente en unidades léxicas (tokens) como identificadores, palabras clave, operadores, etc.
2. **Clasificación**: Asigna una categoría a cada token (por ejemplo: "identificador", "palabra reservada", "operador").
3. **Detección de errores**: Identifica caracteres no permitidos o tokens mal formados.


El analizador léxico de PyJava utiliza expresiones regulares para identificar patrones en el código fuente y clasificarlos según las reglas del lenguaje Java. Los resultados se muestran en una tabla que incluye:

- Línea donde aparece el token
- Valor del token
- Categoría del token


Ejemplo de categorías de tokens:

- Palabras reservadas (`public`, `class`, `if`, etc.)
- Identificadores (nombres de variables, clases, métodos)
- Operadores (`+`, `-`, `*`, `/`, `=`, etc.)
- Literales (números, cadenas, booleanos)
- Delimitadores (`{`, `}`, `;`, etc.)


### Analizador Sintáctico

El analizador sintáctico (implementado en `analizador_sintactico.py`) toma los tokens generados por el analizador léxico y verifica si su estructura cumple con las reglas gramaticales del lenguaje Java. Sus funciones principales son:

1. **Construcción del árbol sintáctico**: Organiza los tokens en una estructura jerárquica que representa la estructura gramatical del programa.
2. **Detección de errores sintácticos**: Identifica construcciones que no cumplen con la gramática del lenguaje.
3. **Visualización del árbol**: Genera una representación gráfica del árbol sintáctico.


PyJava utiliza la biblioteca Lark para implementar un analizador LALR (Look-Ahead LR) que procesa la gramática de Java. El árbol sintáctico se visualiza utilizando Graphviz, permitiendo a los usuarios comprender la estructura jerárquica del código.

El árbol sintáctico muestra:

- Declaraciones de clases
- Métodos
- Bloques de código
- Expresiones
- Sentencias de control (if, for, while)
- Operaciones aritméticas y lógicas


### Analizador Semántico

El analizador semántico (implementado en `analizador_semantico.py`) verifica la coherencia semántica del código después de que su estructura sintáctica ha sido validada. Sus principales funciones son:

1. **Construcción de la tabla de símbolos**: Registra identificadores (variables, métodos, clases) junto con sus atributos (tipo, ámbito, etc.).
2. **Verificación de tipos**: Comprueba que las operaciones se realicen entre tipos compatibles.
3. **Verificación de ámbitos**: Asegura que las variables se utilicen dentro de su ámbito válido.
4. **Detección de errores semánticos**: Identifica problemas como variables no declaradas, tipos incompatibles, etc.


La tabla de símbolos generada muestra:

- Nombre del identificador
- Tipo de dato
- Ámbito
- Línea de declaración
- Valor inicial (si existe)


El AST (Abstract Syntax Tree) anotado muestra el árbol sintáctico con información semántica adicional, como los tipos de las expresiones y las referencias a la tabla de símbolos.

## Tecnologías y Librerías

PyJava utiliza las siguientes tecnologías y librerías:

- **Python**: Lenguaje de programación principal
- **Flet**: Framework para crear interfaces gráficas multiplataforma basado en Flutter
- **Lark**: Biblioteca para la construcción de parsers y análisis sintáctico
- **Graphviz**: Herramienta para la visualización de grafos y árboles
- **Base64**: Para la codificación de imágenes en la interfaz
- **OS**: Para operaciones del sistema de archivos
- **Time**: Para funciones relacionadas con el tiempo y timestamps


## Instalación

### Requisitos Previos

- Python 3.8 o superior
- Flet
- Graphviz (para la visualización de árboles sintácticos)


### Pasos de Instalación

1. **Clonar el repositorio**:

```shellscript
git clone https://github.com/usuario/pyjava.git
cd pyjava
```


2. **Crear un entorno virtual** (opcional pero recomendado):

```shellscript
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```


3. **Instalar dependencias**:

```shellscript
pip install -r requirements.txt
```


4. **Instalar Graphviz**:

1. **Windows**: Descargar e instalar desde [graphviz.org](https://graphviz.org/download/) y añadir a PATH
2. **macOS**: `brew install graphviz`
3. **Linux**: `sudo apt-get install graphviz`



5. **Verificar la instalación de Graphviz**:

```shellscript
dot -V
```



### Solución de Problemas Comunes

- **Error: "dot" no se reconoce como un comando interno o externo**: Asegúrate de que Graphviz esté correctamente instalado y añadido al PATH del sistema.
- **Error al generar el árbol sintáctico**: Verifica que el código Java sea sintácticamente correcto.
- **La interfaz no muestra imágenes**: Asegúrate de tener permisos de escritura en el directorio de la aplicación.


## Uso

### Ejecución del Programa

Para iniciar PyJava, ejecuta:

```shellscript
python main.py
```

### Interfaz Principal

La interfaz principal de PyJava consta de:

1. **Título**: "PyJava - Compilador de Java"
2. **Área de código**: Editor donde puedes escribir o pegar código Java
3. **Botón de carga**: Permite cargar archivos Java (.java)
4. **Botones de navegación**: Acceso a los diferentes analizadores

1. Analizador Léxico
2. Analizador Sintáctico
3. Analizador Semántico





### Análisis Léxico

Para realizar un análisis léxico:

1. Escribe o carga código Java en el editor
2. Navega a la sección "Analizador Léxico"
3. Haz clic en "Resultados" para ver los tokens identificados
4. Haz clic en "Errores" para ver posibles errores léxicos


La vista muestra:

- Tabla de tokens con línea, valor y categoría
- Lista de errores léxicos (si existen)


### Análisis Sintáctico

Para realizar un análisis sintáctico:

1. Escribe o carga código Java en el editor
2. Navega a la sección "Analizador Sintáctico"
3. Haz clic en "Árbol" para generar y visualizar el árbol sintáctico
4. Haz clic en "Errores" para ver posibles errores sintácticos


La vista muestra:

- Representación visual del árbol sintáctico
- Lista de errores sintácticos (si existen)


### Análisis Semántico

Para realizar un análisis semántico:

1. Escribe o carga código Java en el editor
2. Navega a la sección "Analizador Semántico"
3. Haz clic en "Analizar" para realizar el análisis semántico


La vista muestra:

- Lista de errores semánticos (si existen)
- Tabla de símbolos con información sobre variables y métodos
- AST anotado con información semántica



## Estructura del Proyecto

```plaintext
pyjava/
├── main.py                    # Punto de entrada y UI principal
├── analizador_lexico.py       # Implementación del analizador léxico
├── analizador_sintactico.py   # Implementación del analizador sintáctico
├── analizador_semantico.py    # Implementación del analizador semántico
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación
└── ejemplos/                  # Ejemplos de código Java
    ├── ejemplo1.java
    ├── ejemplo2.java
    └── ...
```

## Autores

- **Rodrigo Torres** - Desarrollo e implementación
- **Jesús Araujo** - Desarrollo e implementación


## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contribuciones y Desarrollo Futuro

### Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request


---

## Agradecimientos

Agradecemos a todos los que han contribuido a este proyecto educativo, así como a los desarrolladores de las bibliotecas y herramientas utilizadas.

Para más información, consultas o reportes de errores, por favor contactanos o abre un issue en el repositorio del proyecto.