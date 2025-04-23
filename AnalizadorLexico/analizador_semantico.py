import re
from typing import List, Dict, Tuple, Optional

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
                 modificadores: List[str] = None):
        self.nombre = nombre
        self.tipo_retorno = tipo_retorno
        self.parametros = parametros
        self.modificadores = modificadores or []
        self.variables_locales: Dict[str, Simbolo] = {}
    
    def es_final(self) -> bool:
        return "final" in self.modificadores

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
        nueva = Clase(nombre, padre, modificadores)
        if padre and padre in self.clases:
            padre_cls = self.clases[padre]
            nueva.atributos = padre_cls.atributos.copy()
            nueva.metodos = padre_cls.metodos.copy()
        self.clases[nombre] = nueva
        return True
    
    def agregar_metodo(self, clase: str, nombre: str, tipo_retorno: str, 
                      parametros: List[Tuple[str, str]], modificadores: List[str], linea: int = 0) -> bool:
        if clase not in self.clases:
            self.errores.append((linea, f"Error: La clase '{clase}' no ha sido declarada"))
            return False
        cls_obj = self.clases[clase]
        # Sobre carga/override
        if nombre in cls_obj.metodos:
            existente = cls_obj.metodos[nombre]
            if len(existente.parametros) == len(parametros) and all(existente.parametros[i][0] == parametros[i][0] for i in range(len(parametros))):
                self.errores.append((linea, f"Error: El método '{nombre}' ya ha sido declarado en la clase '{clase}'"))
                return False
        padre = cls_obj.padre
        if padre in self.clases and nombre in self.clases[padre].metodos and self.clases[padre].metodos[nombre].es_final():
            self.errores.append((linea, f"Error: No se puede sobrescribir el método final '{nombre}' de la clase '{padre}'"))
            return False
        cls_obj.metodos[nombre] = Metodo(nombre, tipo_retorno, parametros, modificadores)
        return True
    
    def agregar_variable(self, nombre: str, tipo: str, ambito: str, linea: int, modificadores: List[str] = None) -> bool:
        partes = ambito.split('.')
        # Método
        if len(partes) == 3:
            cls, met = partes[1], partes[2]
            if cls in self.clases and met in self.clases[cls].metodos:
                vars_loc = self.clases[cls].metodos[met].variables_locales
                if nombre in vars_loc:
                    self.errores.append((linea, f"Error: La variable '{nombre}' ya ha sido declarada en este ámbito"))
                    return False
                vars_loc[nombre] = Simbolo(nombre, tipo, ambito, linea, modificadores)
                return True
        # Atributo
        if len(partes) == 2:
            cls = partes[1]
            if cls in self.clases:
                attrs = self.clases[cls].atributos
                if nombre in attrs:
                    self.errores.append((linea, f"Error: El atributo '{nombre}' ya ha sido declarado en la clase '{cls}'"))
                    return False
                attrs[nombre] = Simbolo(nombre, tipo, ambito, linea, modificadores)
                return True
        self.errores.append((linea, f"Error: No se pudo agregar la variable '{nombre}' en el ámbito '{ambito}'"))
        return False
    
    def buscar_variable(self, nombre: str, ambito: str) -> Optional[Simbolo]:
        partes = ambito.split('.')
        if len(partes) == 3:
            cls, met = partes[1], partes[2]
            metodo = self.clases[cls].metodos.get(met)
            if metodo and nombre in metodo.variables_locales:
                return metodo.variables_locales[nombre]
            if nombre in self.clases[cls].atributos:
                return self.clases[cls].atributos[nombre]
        if len(partes) == 2:
            cls = partes[1]
            if nombre in self.clases[cls].atributos:
                return self.clases[cls].atributos[nombre]
        return None

# Inferencia de tipos sencilla

def inferir_tipo(expr: str, tabla: TablaSimbolos, ambito: str) -> Optional[str]:
    expr = expr.strip()
    if re.fullmatch(r'\d+', expr): return 'int'
    if expr in ('true', 'false'): return 'boolean'
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")): return 'String'
    if expr.endswith('[]'):
        base = expr[:-2]
        return base + '[]'
    sym = tabla.buscar_variable(expr, ambito)
    if sym: return sym.tipo
    m = re.match(r'new\s+(\w+)\s*\(\s*\)', expr)
    if m and m.group(1) in tabla.clases: return m.group(1)
    return None

# Análisis semántico robusto

def analizar_semanticamente(codigo: str) -> Tuple[TablaSimbolos, List[Tuple[int, str]]]:
    tabla = TablaSimbolos()
    errores: List[Tuple[int, str]] = []
    lineas = codigo.split('\n')
    # Modificadores permitidos
    mods_pattern = r'(?:public|private|protected|static|final|abstract)'
    # Patrón de método: varios modificadores opcionales, tipo (incluyendo []), nombre, params
    patron_metodo = rf'^(?P<mods>(?:{mods_pattern}\s+)*)' + \
                   r'(?P<tipo>\w+(?:\[\])?)\s+' + \
                   r'(?P<name>\w+)\s*\((?P<params>.*?)\)'
    p_met = re.compile(patron_metodo)
    p_clase = re.compile(r'^(?P<mods>(?:public|private|protected|final|abstract)\s+)*class\s+(?P<name>\w+)(?:\s+extends\s+(?P<padre>\w+))?')
    p_var = re.compile(r'^(?P<mods>(?:public|private|protected|static|final)\s+)*(?P<tipo>\w+(?:\[\])?)\s+(?P<name>\w+)(?:=\s*(?P<val>.+?))?;')
    p_asig = re.compile(r'^(?P<name>\w+)\s*=\s*(?P<val>.+);')
    p_ret = re.compile(r'^return\s+(?P<expr>.+);')
    p_call = re.compile(r'^(?P<obj>\w+)\.(?P<m>\w+)\((?P<args>.*?)\);')
    brace_count = 0
    rastreo_return: Dict[Tuple[str, str], bool] = {}
    clase_act = None
    metodo_act = None

    for i, linea in enumerate(lineas, 1):
        s = linea.strip()
        if not s: 
            brace_count += 0
        # Clase
        m_cl = p_clase.match(s)
        if m_cl:
            mods = m_cl.group('mods').split() if m_cl.group('mods') else []
            name = m_cl.group('name')
            padre = m_cl.group('padre')
            tabla.agregar_clase(name, padre, mods, i)
            clase_act = name
            tabla.ambito_actual = ["global", name]
        # Método
        m_met = p_met.match(s)
        if m_met and clase_act:
            mods = m_met.group('mods').split() if m_met.group('mods') else []
            tipo = m_met.group('tipo')
            name = m_met.group('name')
            params = []
            rawp = m_met.group('params')
            for p in [x.strip() for x in rawp.split(',') if x.strip()]:
                t, n = p.split()[:2]
                params.append((t, n))
            tabla.agregar_metodo(clase_act, name, tipo, params, mods, i)
            metodo_act = name
            tabla.ambito_actual = ["global", clase_act, name]
            rastreo_return[(clase_act, name)] = False
            for t,n in params:
                tabla.agregar_variable(n, t, tabla.obtener_ambito_actual(), i)
        # Variable
        m_var = p_var.match(s)
        if m_var:
            mods = m_var.group('mods').split() if m_var.group('mods') else []
            t = m_var.group('tipo')
            n = m_var.group('name')
            val = m_var.group('val')
            if val:
                tval = inferir_tipo(val, tabla, tabla.obtener_ambito_actual())
                if tval and tval != t:
                    errores.append((i, f"Error: No se puede asignar {tval} a {t}"))
            tabla.agregar_variable(n, t, tabla.obtener_ambito_actual(), i, mods)
        # Asignación
        m_as = p_asig.match(s)
        if m_as:
            sym = tabla.buscar_variable(m_as.group('name'), tabla.obtener_ambito_actual())
            if not sym:
                errores.append((i, f"Error: La variable '{m_as.group('name')}' no declarada"))
            else:
                tval = inferir_tipo(m_as.group('val'), tabla, tabla.obtener_ambito_actual())
                if tval and tval != sym.tipo:
                    errores.append((i, f"Error: No se puede asignar {tval} a {sym.tipo}"))
        # Return
        m_r = p_ret.match(s)
        if m_r and metodo_act:
            rastreo_return[(clase_act, metodo_act)] = True
            tret = inferir_tipo(m_r.group('expr'), tabla, tabla.obtener_ambito_actual())
            esperado = tabla.clases[clase_act].metodos[metodo_act].tipo_retorno
            if esperado != 'void' and tret != esperado:
                errores.append((i, f"Error: return {tret} no coincide con {esperado}"))
        # Llamada
        m_c = p_call.match(s)
        if m_c:
            sym = tabla.buscar_variable(m_c.group('obj'), tabla.obtener_ambito_actual())
            cls_name = sym.tipo if sym else m_c.group('obj') if m_c.group('obj') in tabla.clases else None
            if not cls_name:
                errores.append((i, f"Error: Tipo {m_c.group('obj')} desconocido"))
            elif m_c.group('m') not in tabla.clases[cls_name].metodos:
                errores.append((i, f"Error: {m_c.group('m')} no en {cls_name}"))
        # Conteo llaves y cierre de ámbitos
        brace_count += s.count('{') - s.count('}')
        if metodo_act and brace_count < 2:
            ok = rastreo_return.get((clase_act, metodo_act), False)
            ret_type = tabla.clases[clase_act].metodos[metodo_act].tipo_retorno
            if ret_type != 'void' and not ok:
                errores.append((i, f"Error: {metodo_act} no retorna {ret_type}"))
            metodo_act = None
            tabla.ambito_actual = ["global", clase_act]
        if clase_act and brace_count < 1:
            clase_act = None
            tabla.ambito_actual = ["global"]
    # Validaciones finales
    for idx,l in enumerate(lineas,1):
        if 'new ' in l:
            m = re.search(r'new\s+(\w+)', l)
            if m and m.group(1) not in tabla.clases:
                errores.append((idx, f"Error: clase {m.group(1)} no declarada"))
    for c in tabla.clases.values():
        if c.padre and c.padre in tabla.clases and tabla.clases[c.padre].es_final():
            errores.append((0, f"Error: hereda final {c.padre}"))
    todos = tabla.errores + errores
    return tabla, todos

# Salida textual (sin cambios significativos)
def obtener_tabla_simbolos_texto(tabla: TablaSimbolos) -> str:
    out = []
    for cls in tabla.clases.values():
        mods = ' '.join(cls.modificadores)
        line = f"CLASE: {mods} {cls.nombre}" + (f" extends {cls.padre}" if cls.padre else '')
        out.append(line)
        if cls.atributos:
            out.append('  ATRIBUTOS:')
            for atr in cls.atributos.values(): out.append(f"    {atr}")
        if cls.metodos:
            out.append('  MÉTODOS:')
            for m in cls.metodos.values():
                pm = ' '.join(m.modificadores)
                ps = ', '.join(f"{t} {n}" for t,n in m.parametros)
                out.append(f"    {pm} {m.tipo_retorno} {m.nombre}({ps})")
                if m.variables_locales:
                    out.append('      VARIAS LOCALES:')
                    for v in m.variables_locales.values(): out.append(f"        {v}")
        out.append('')
    return '\n'.join(out)

def obtener_ast_anotado(tabla: TablaSimbolos) -> str:
    lines = []
    for cls in tabla.clases.values():
        lines.append(f"Clase: {cls.nombre} [Tipo: class]")
        if cls.atributos:
            lines.append('  Atributos:')
            for atr in cls.atributos.values(): lines.append(f"    {atr.nombre} [Tipo: {atr.tipo}]")
        if cls.metodos:
            lines.append('  Métodos:')
            for m in cls.metodos.values():
                lines.append(f"    {m.nombre} [Retorno: {m.tipo_retorno}]")
                if m.parametros:
                    lines.append('      Parámetros:')
                    for t,n in m.parametros: lines.append(f"        {n} [Tipo: {t}]")
                if m.variables_locales:
                    lines.append('      Variables:')
                    for v in m.variables_locales.values(): lines.append(f"        {v.nombre} [Tipo: {v.tipo}]")
        lines.append('')
    return '\n'.join(lines)
