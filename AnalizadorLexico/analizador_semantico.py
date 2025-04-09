import re
from typing import List, Dict, Tuple, Set, Optional

class Simbolo:
    def __init__(self, nombre: str, tipo: str, ambito: str, linea: int, modificadores: List[str] = None):
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.linea = linea
        self.modificadores = modificadores or []
    
    def __str__(self):
        mods = " ".join(self.modificadores)
        return f"{mods} {self.tipo} {self.nombre} (línea {self.linea})"

class Clase:
    def __init__(self, nombre: str, padre: str = None, modificadores: List[str] = None):
        self.nombre = nombre
        self.padre = padre
        self.modificadores = modificadores or []
        self.metodos: Dict[str, Metodo] = {}
        self.atributos: Dict[str, Simbolo] = {}
    
    def es_final(self) -> bool:
        return "final" in self.modificadores

class Metodo:
    def __init__(self, nombre: str, tipo_retorno: str, parametros: List[Tuple[str, str]], 
                 modificadores: List[str] = None, excepciones: List[str] = None):
        self.nombre = nombre
        self.tipo_retorno = tipo_retorno
        self.parametros = parametros  # Lista de tuplas (tipo, nombre)
        self.modificadores = modificadores or []
        self.excepciones = excepciones or []
        self.variables_locales: Dict[str, Simbolo] = {}
    
    def es_final(self) -> bool:
        return "final" in self.modificadores
    
    def es_privado(self) -> bool:
        return "private" in self.modificadores

class TablaSimbolos:
    def __init__(self):
        self.clases: Dict[str, Clase] = {}
        self.ambito_actual: List[str] = ["global"]
        self.errores: List[Tuple[int, str]] = []
    
    def obtener_ambito_actual(self) -> str:
        return ".".join(self.ambito_actual)
    
    def agregar_clase(self, nombre: str, padre: str = None, modificadores: List[str] = None, linea: int = 0) -> bool:
        if nombre in self.clases:
            self.errores.append((linea, f"Error: La clase '{nombre}' ya ha sido declarada"))
            return False
        
        self.clases[nombre] = Clase(nombre, padre, modificadores)
        return True
    
    def agregar_metodo(self, clase: str, nombre: str, tipo_retorno: str, 
                      parametros: List[Tuple[str, str]], modificadores: List[str] = None, 
                      excepciones: List[str] = None, linea: int = 0) -> bool:
        if clase not in self.clases:
            self.errores.append((linea, f"Error: La clase '{clase}' no ha sido declarada"))
            return False
        
        if nombre in self.clases[clase].metodos:
            # Verificar si es una sobrecarga válida (diferentes parámetros)
            metodo_existente = self.clases[clase].metodos[nombre]
            if len(metodo_existente.parametros) == len(parametros):
                tipos_iguales = True
                for i in range(len(parametros)):
                    if metodo_existente.parametros[i][0] != parametros[i][0]:
                        tipos_iguales = False
                        break
                
                if tipos_iguales:
                    self.errores.append((linea, f"Error: El método '{nombre}' ya ha sido declarado en la clase '{clase}'"))
                    return False
        
        # Verificar si está sobrescribiendo un método final
        if clase in self.clases and self.clases[clase].padre in self.clases:
            padre = self.clases[clase].padre
            if nombre in self.clases[padre].metodos and self.clases[padre].metodos[nombre].es_final():
                self.errores.append((linea, f"Error: No se puede sobrescribir el método final '{nombre}' de la clase '{padre}'"))
                return False
        
        self.clases[clase].metodos[nombre] = Metodo(nombre, tipo_retorno, parametros, modificadores, excepciones)
        return True
    
    def agregar_variable(self, nombre: str, tipo: str, ambito: str, linea: int, modificadores: List[str] = None) -> bool:
        # Verificar si la variable ya existe en el ámbito actual
        partes_ambito = ambito.split('.')
        
        # Si estamos en un método
        if len(partes_ambito) >= 3:  # global.Clase.metodo
            clase = partes_ambito[1]
            metodo = partes_ambito[2]
            
            if clase in self.clases and metodo in self.clases[clase].metodos:
                if nombre in self.clases[clase].metodos[metodo].variables_locales:
                    self.errores.append((linea, f"Error: La variable '{nombre}' ya ha sido declarada en este ámbito"))
                    return False
                
                self.clases[clase].metodos[metodo].variables_locales[nombre] = Simbolo(nombre, tipo, ambito, linea, modificadores)
                return True
        
        # Si estamos en una clase (atributo)
        elif len(partes_ambito) == 2:  # global.Clase
            clase = partes_ambito[1]
            
            if clase in self.clases:
                if nombre in self.clases[clase].atributos:
                    self.errores.append((linea, f"Error: El atributo '{nombre}' ya ha sido declarado en la clase '{clase}'"))
                    return False
                
                self.clases[clase].atributos[nombre] = Simbolo(nombre, tipo, ambito, linea, modificadores)
                return True
        
        self.errores.append((linea, f"Error: No se pudo agregar la variable '{nombre}' en el ámbito '{ambito}'"))
        return False
    
    def buscar_variable(self, nombre: str, ambito: str) -> Optional[Simbolo]:
        partes_ambito = ambito.split('.')
        
        # Buscar en ámbito de método
        if len(partes_ambito) >= 3:  # global.Clase.metodo
            clase = partes_ambito[1]
            metodo = partes_ambito[2]
            
            if clase in self.clases and metodo in self.clases[clase].metodos:
                if nombre in self.clases[clase].metodos[metodo].variables_locales:
                    return self.clases[clase].metodos[metodo].variables_locales[nombre]
            
            # Si no se encuentra en el método, buscar en los atributos de la clase
            if clase in self.clases and nombre in self.clases[clase].atributos:
                return self.clases[clase].atributos[nombre]
        
        # Buscar en ámbito de clase
        elif len(partes_ambito) == 2:  # global.Clase
            clase = partes_ambito[1]
            
            if clase in self.clases and nombre in self.clases[clase].atributos:
                return self.clases[clase].atributos[nombre]
        
        return None

def analizar_semanticamente(codigo: str) -> Tuple[TablaSimbolos, List[Tuple[int, str]]]:
    tabla = TablaSimbolos()
    errores = []
    
    # Dividir el código en líneas para el análisis
    lineas = codigo.split('\n')
    
    # Patrones para identificar elementos del código
    patron_clase = r'(public|private|protected|final|abstract)?\s+class\s+(\w+)(?:\s+extends\s+(\w+))?'
    patron_metodo = r'(public|private|protected|static|final|abstract)?\s+(\w+)\s+(\w+)\s*$$(.*?)$$'
    patron_variable = r'(public|private|protected|static|final)?\s+(\w+)\s+(\w+)\s*(?:=\s*(.+?))?;'
    patron_asignacion = r'(\w+)\s*=\s*(.+?);'
    patron_operacion = r'(.+?)\s*([+\-*/])\s*(.+?)'
    
    # Análisis de clases
    clase_actual = None
    metodo_actual = None
    
    for i, linea in enumerate(lineas, 1):
        linea = linea.strip()
        if not linea:
            continue
        
        # Buscar declaraciones de clase
        match_clase = re.search(patron_clase, linea)
        if match_clase:
            modificadores = []
            if match_clase.group(1):
                modificadores = match_clase.group(1).split()
            
            nombre_clase = match_clase.group(2)
            clase_padre = match_clase.group(3)
            
            tabla.agregar_clase(nombre_clase, clase_padre, modificadores, i)
            clase_actual = nombre_clase
            tabla.ambito_actual = ["global", nombre_clase]
            continue
        
        # Buscar declaraciones de método
        match_metodo = re.search(patron_metodo, linea)
        if match_metodo and clase_actual:
            modificadores = []
            if match_metodo.group(1):
                modificadores = match_metodo.group(1).split()
            
            tipo_retorno = match_metodo.group(2)
            nombre_metodo = match_metodo.group(3)
            
            # Procesar parámetros
            parametros_str = match_metodo.group(4).strip()
            parametros = []
            
            if parametros_str:
                for param in parametros_str.split(','):
                    param = param.strip()
                    if param:
                        partes = param.split()
                        if len(partes) >= 2:
                            tipo_param = partes[0]
                            nombre_param = partes[1]
                            parametros.append((tipo_param, nombre_param))
            
            tabla.agregar_metodo(clase_actual, nombre_metodo, tipo_retorno, parametros, modificadores, [], i)
            metodo_actual = nombre_metodo
            tabla.ambito_actual = ["global", clase_actual, metodo_actual]
            
            # Agregar parámetros como variables locales
            for tipo_param, nombre_param in parametros:
                tabla.agregar_variable(nombre_param, tipo_param, tabla.obtener_ambito_actual(), i)
            
            continue
        
        # Buscar declaraciones de variables
        match_variable = re.search(patron_variable, linea)
        if match_variable:
            modificadores = []
            if match_variable.group(1):
                modificadores = match_variable.group(1).split()
            
            tipo_var = match_variable.group(2)
            nombre_var = match_variable.group(3)
            valor_var = match_variable.group(4) if match_variable.group(4) else None
            
            # Verificar compatibilidad de tipos en la asignación
            if valor_var:
                # Verificar asignación de string a int
                if tipo_var == "int" and ('"' in valor_var or "'" in valor_var):
                    errores.append((i, f"Error: No se puede asignar un String a una variable de tipo int"))
                
                # Verificar asignación de boolean a int
                elif tipo_var == "int" and valor_var in ["true", "false"]:
                    errores.append((i, f"Error: No se puede asignar un boolean a una variable de tipo int"))
                
                # Verificar asignación de int a boolean
                elif tipo_var == "boolean" and re.match(r'^[0-9]+$', valor_var) and valor_var not in ["0", "1"]:
                    errores.append((i, f"Error: No se puede asignar un int a una variable de tipo boolean"))
            
            tabla.agregar_variable(nombre_var, tipo_var, tabla.obtener_ambito_actual(), i, modificadores)
            continue
        
        # Buscar asignaciones
        match_asignacion = re.search(patron_asignacion, linea)
        if match_asignacion:
            nombre_var = match_asignacion.group(1)
            valor = match_asignacion.group(2)
            
            # Buscar la variable en la tabla de símbolos
            variable = tabla.buscar_variable(nombre_var, tabla.obtener_ambito_actual())
            
            if not variable:
                errores.append((i, f"Error: La variable '{nombre_var}' no ha sido declarada"))
            else:
                # Verificar compatibilidad de tipos en la asignación
                if variable.tipo == "int":
                    if '"' in valor or "'" in valor:
                        errores.append((i, f"Error: No se puede asignar un String a una variable de tipo int"))
                    elif valor in ["true", "false"]:
                        errores.append((i, f"Error: No se puede asignar un boolean a una variable de tipo int"))
                
                elif variable.tipo == "boolean":
                    if re.match(r'^[0-9]+$', valor) and valor not in ["0", "1"]:
                        errores.append((i, f"Error: No se puede asignar un int a una variable de tipo boolean"))
                
                # Verificar acceso a miembros privados
                if "private" in variable.modificadores:
                    partes_ambito = tabla.obtener_ambito_actual().split('.')
                    partes_var = variable.ambito.split('.')
                    
                    if len(partes_ambito) >= 2 and len(partes_var) >= 2:
                        if partes_ambito[1] != partes_var[1]:  # Diferentes clases
                            errores.append((i, f"Error: No se puede acceder al miembro privado '{nombre_var}' desde fuera de la clase '{partes_var[1]}'"))
            
            continue
        
        # Buscar operaciones aritméticas/lógicas
        match_operacion = re.search(patron_operacion, linea)
        if match_operacion:
            operando1 = match_operacion.group(1).strip()
            operador = match_operacion.group(2)
            operando2 = match_operacion.group(3).strip()
            
            # Verificar operaciones con tipos incompatibles
            if operador in ['+', '-', '*', '/']:
                # Verificar si alguno de los operandos es un booleano
                if operando1 in ["true", "false"] or operando2 in ["true", "false"]:
                    errores.append((i, f"Error: No se pueden realizar operaciones aritméticas con valores booleanos"))
                
                # Verificar si se está intentando operar un string con algo que no sea +
                elif ('"' in operando1 or "'" in operando1 or '"' in operando2 or "'" in operando2) and operador != '+':
                    errores.append((i, f"Error: Solo se puede usar el operador + con strings (concatenación)"))
            
            continue
    
    # Verificar llamadas a constructores
    for i, linea in enumerate(lineas, 1):
        if "new" in linea:
            match_constructor = re.search(r'new\s+(\w+)', linea)
            if match_constructor:
                nombre_clase = match_constructor.group(1)
                
                if nombre_clase not in tabla.clases:
                    errores.append((i, f"Error: La clase '{nombre_clase}' no ha sido declarada"))
    
    # Verificar herencia de clases finales
    for nombre, clase in tabla.clases.items():
        if clase.padre and clase.padre in tabla.clases:
            if tabla.clases[clase.padre].es_final():
                errores.append((0, f"Error: No se puede heredar de la clase final '{clase.padre}'"))
    
    # Combinar errores de la tabla de símbolos con los detectados durante el análisis
    todos_errores = tabla.errores + errores
    
    return tabla, todos_errores

def obtener_tabla_simbolos_texto(tabla: TablaSimbolos) -> str:
    """Genera una representación textual de la tabla de símbolos para mostrar en la interfaz."""
    resultado = []
    
    for nombre_clase, clase in tabla.clases.items():
        mods = " ".join(clase.modificadores)
        resultado.append(f"CLASE: {mods} {nombre_clase}" + (f" extends {clase.padre}" if clase.padre else ""))
        
        # Atributos
        if clase.atributos:
            resultado.append("  ATRIBUTOS:")
            for nombre, atributo in clase.atributos.items():
                resultado.append(f"    {str(atributo)}")
        
        # Métodos
        if clase.metodos:
            resultado.append("  MÉTODOS:")
            for nombre, metodo in clase.metodos.items():
                mods = " ".join(metodo.modificadores)
                params = ", ".join([f"{tipo} {nombre}" for tipo, nombre in metodo.parametros])
                resultado.append(f"    {mods} {metodo.tipo_retorno} {nombre}({params})")
                
                # Variables locales
                if metodo.variables_locales:
                    resultado.append("      VARIABLES LOCALES:")
                    for var_nombre, var in metodo.variables_locales.items():
                        resultado.append(f"        {str(var)}")
        
        resultado.append("")  # Línea en blanco entre clases
    
    return "\n".join(resultado)

def obtener_ast_anotado(tabla: TablaSimbolos) -> str:
    """Genera una representación textual del AST anotado con tipos."""
    resultado = []
    
    for nombre_clase, clase in tabla.clases.items():
        resultado.append(f"Clase: {nombre_clase} [Tipo: class]")
        
        # Atributos
        if clase.atributos:
            resultado.append("  Atributos:")
            for nombre, atributo in clase.atributos.items():
                resultado.append(f"    {nombre} [Tipo: {atributo.tipo}]")
        
        # Métodos
        if clase.metodos:
            resultado.append("  Métodos:")
            for nombre, metodo in clase.metodos.items():
                resultado.append(f"    {nombre} [Retorno: {metodo.tipo_retorno}]")
                
                # Parámetros
                if metodo.parametros:
                    resultado.append("      Parámetros:")
                    for tipo, nombre in metodo.parametros:
                        resultado.append(f"        {nombre} [Tipo: {tipo}]")
                
                # Variables locales
                if metodo.variables_locales:
                    resultado.append("      Variables:")
                    for var_nombre, var in metodo.variables_locales.items():
                        resultado.append(f"        {var_nombre} [Tipo: {var.tipo}]")
        
        resultado.append("")  # Línea en blanco entre clases
    
    return "\n".join(resultado)