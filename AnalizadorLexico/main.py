import flet as ft
import os
from analizador_lexico import analizar_lexicamente, obtener_errores
from analizador_sintactico import generar_arbol_sintactico

def main(page: ft.Page):
    page.title = "Fases de un compilador"
    page.theme_mode = "dark"
    page.bgcolor = "#121212" 
    page.padding = 20
    
    #Declarar la variable codigo_input en un ámbito más amplio
    codigo_input = None
    
    #Definir la función on_file_picked antes de crear el FilePicker
    def on_file_picked(e):
        if e.files and len(e.files) > 0:
            selected_file = e.files[0]
            try:
                # Leer el contenido del archivo
                with open(selected_file.path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    #Actualizar el campo de texto con el contenido del archivo
                    codigo_input.value = content
                    page.update()
            except Exception as ex:
                print(f"Error al leer el archivo: {ex}")
    
    #Crear el FilePicker para seleccionar archivos Java
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    def route_change(route):
        nonlocal codigo_input
        
        page.views.clear()
        
        # Main menu view
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Column(
                            [
                                ft.Text("Fases de un compilador", 
                                        size=32, 
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=40),
                                ft.ElevatedButton(
                                    "Analizador Léxico",
                                    width=300,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=lambda _: page.go("/lexico")
                                ),
                                ft.ElevatedButton(
                                    "Analizador Sintáctico",
                                    width=300,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=lambda _: page.go("/sintactico")
                                ),
                                ft.ElevatedButton(
                                    "Analizador Semántico",
                                    width=300,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8)
                                    ),
                                    on_click=lambda _: page.go("/semantico")
                                ),
                                ft.Container(height=40),
                                ft.Text(
                                    "Rodrigo Torres y Jesús Araujo",
                                    size=16,
                                    color=ft.colors.GREY_400,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ]
                )
            )

        #vista lexoico
        if page.route == "/lexico":
            codigo_input = ft.TextField(
                multiline=True,
                min_lines=8,
                max_lines=8,
                hint_text="Introduzca su código aquí...",
                hint_style=ft.TextStyle(color=ft.colors.GREY_400),
                border_radius=8,
                bgcolor="#282828",
                border_color="transparent",
                text_size=14,
                color=ft.colors.WHITE,
                value="""public class Prueba {
            public static void main(String[] args) {
                int x = 10;
                if (x >= 5) {
                    x += 2;
                }
            }
        }"""
            )

            # Tabla de resultados con scroll
            resultados_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=250  
            )

            # Tabla de errores con scroll (donde se mostrará la línea y el error)
            errores_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=250  
            )

            def analizar_codigo(e):
                codigo = codigo_input.value
                tokens = analizar_lexicamente(codigo)

                resultados_table.controls.clear()

                # Encabezado de la tabla de tokens
                resultados_table.controls.append(
                    ft.Row([
                        ft.Text("Línea", weight=ft.FontWeight.BOLD, width=50),
                        ft.Text("Token", weight=ft.FontWeight.BOLD, width=120),
                        ft.Text("Categoría", weight=ft.FontWeight.BOLD, width=150)
                    ])
                )

                for palabra, linea, categoria in tokens:
                    resultados_table.controls.append(
                        ft.Row([
                            ft.Text(str(linea), width=50),
                            ft.Text(palabra, width=120),
                            ft.Text(categoria, width=150)
                        ])
                    )

                page.update()

            def mostrar_errores(e):
                codigo = codigo_input.value
                errores = obtener_errores(codigo)

                errores_table.controls.clear()

                # Encabezado de la tabla de errores
                errores_table.controls.append(
                    ft.Row([
                        ft.Text("Línea", weight=ft.FontWeight.BOLD, width=50),
                        ft.Text("Error", weight=ft.FontWeight.BOLD, width=300)
                    ])
                )

                if errores:
                    for linea, mensaje in errores:
                        linea_str = str(linea) if linea != 0 else "Global"
                        errores_table.controls.append(
                            ft.Row([
                                ft.Text(linea_str, width=50),
                                ft.Text(mensaje, width=300)
                            ])
                        )
                else:
                    errores_table.controls.append(
                        ft.Row([
                            ft.Text(""),
                            ft.Text("No se encontraron errores.", width=300)
                        ])
                    )
                page.update()

            def limpiar_resultados(e):
                resultados_table.controls.clear()
                errores_table.controls.clear()
                page.update()

            def abrir_selector_archivos(e):
                file_picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=["java"]
                )

            page.views.append(
                ft.View(
                    "/lexico",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                            title=ft.Text("Analizador Léxico"),
                            center_title=True,
                            bgcolor="#121212",
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Text("Código fuente", size=14, weight=ft.FontWeight.W_500),
                                                ft.ElevatedButton(
                                                    "Buscar archivo Java",
                                                    icon=ft.icons.UPLOAD_FILE,
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=20),
                                                        bgcolor={"": "#1DB954"}
                                                    ),
                                                    on_click=abrir_selector_archivos
                                                )
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            codigo_input
                                        ]),
                                        padding=ft.padding.only(bottom=10)
                                    ),
                                    # Contenedor con tablas de resultados y errores alineados horizontalmente
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Container(
                                                    content=ft.Column([
                                                        ft.Text("Resultados", size=14, weight=ft.FontWeight.W_500),
                                                        resultados_table
                                                    ]),
                                                    expand=True,
                                                    padding=ft.padding.all(10)
                                                ),
                                                ft.Container(
                                                    content=ft.Column([
                                                        ft.Text("Errores", size=14, weight=ft.FontWeight.W_500),
                                                        errores_table
                                                    ]),
                                                    expand=True,
                                                    padding=ft.padding.all(10)
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        height=300  
                                    ),
                                    # Botones de acciones
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Resultados",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=20),
                                                    bgcolor={"": "#1DB954"}
                                                ),
                                                on_click=analizar_codigo
                                            ),
                                            ft.ElevatedButton(
                                                "Errores",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=20),
                                                    bgcolor={"": "#1DB954"}
                                                ),
                                                on_click=mostrar_errores
                                            ),
                                            ft.ElevatedButton(
                                                "Limpiar",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=20),
                                                    bgcolor={"": "#FF3B30"}
                                                ),
                                                on_click=limpiar_resultados
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10
                                    )
                                ],
                                spacing=10
                            ),
                            padding=20,
                            border_radius=10
                        )
                    ]
                )
            )

        # Vista Sintáctico
        elif page.route == "/sintactico":
            # Creamos un input específico para el código en la vista sintáctica
            codigo_input_sintactico = ft.TextField(
                multiline=True,
                min_lines=8,
                max_lines=8,
                hint_text="Ingrese el código Java para el árbol sintáctico...",
                hint_style=ft.TextStyle(color=ft.colors.GREY_400),
                border_radius=8,
                bgcolor="#282828",
                border_color="transparent",
                text_size=14,
                color=ft.colors.WHITE,
                value="""public class Prueba {
        public static void main(String[] args) {
            int x = 10;
            if (x >= 5) {
                x += 2;
            }
        }
    }"""
            )

            # Imagen donde se mostrará el árbol generado
            tree_image = ft.Image(src="arbol_sintactico.png", width=400, height=300)

            def generar_arbol(e):
                codigo = codigo_input_sintactico.value
                # Se genera el árbol sintáctico a partir del código ingresado
                generar_arbol_sintactico(codigo)
                # Actualizamos la imagen para reflejar la nueva versión del árbol
                tree_image.src = "arbol_sintactico.png"  # Se asume que el archivo se guarda con este nombre
                page.update()

            page.views.append(
                ft.View(
                    "/semantico",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                            title=ft.Text("Analizador Sintáctico"),
                            center_title=True,
                            bgcolor="#121212",
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Generador de Árbol Sintáctico", 
                                        size=20, 
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    codigo_input_sintactico,
                                    ft.ElevatedButton("Generar Árbol", on_click=generar_arbol),
                                    tree_image
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20
                            ),
                            expand=True,
                            alignment=ft.alignment.center
                        )
                    ]
                )
            )

        #vista semantico
        elif page.route == "/semantico":
            page.views.append(
                ft.View(
                    "/semantico",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.ARROW_BACK, 
                                                on_click=lambda _: page.go("/")),
                            title=ft.Text("Analizador Semántico"),
                            center_title=True,
                            bgcolor="#121212",
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Analizador Semántico - En construcción", 
                                            size=20, 
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER),
                                    ft.Image(
                                        src="AnalizadorLexico\perro.jpg",
                                        width=200,  # Ajusta el ancho según sea necesario
                                        height=200, # Ajusta el alto según sea necesario
                                        fit=ft.ImageFit.CONTAIN, # Ajusta el fit según sea necesario
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            expand=True,
                            alignment=ft.alignment.center
                        )
                    ]
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)