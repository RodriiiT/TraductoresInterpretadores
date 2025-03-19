import flet as ft
import os
from analizador_lexico import analizar_lexicamente, obtener_errores

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
        elif page.route == "/lexico":
            # Crear los controles para la vista del analizador léxico
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
}"""  # Código de ejemplo
            )
            
            resultados_output = ft.TextField(
                multiline=True,
                min_lines=6,
                max_lines=6,
                read_only=True,
                bgcolor="#282828",
                border_color="transparent",
                border_radius=8,
                text_size=14
            )
            
            errores_output = ft.TextField(
                multiline=True,
                min_lines=6,
                max_lines=6,
                read_only=True,
                bgcolor="#282828",
                border_color="transparent",
                border_radius=8,
                text_size=14
            )
            
            # Función para analizar el código y mostrar resultados
            def analizar_codigo(e):
                codigo = codigo_input.value
                tokens = analizar_lexicamente(codigo)
                
                # Formatear los resultados
                resultados_texto = ""
                for palabra, linea, categoria in tokens:
                    resultados_texto += f"{palabra} -> {linea}, {categoria}\n"
                
                resultados_output.value = resultados_texto
                page.update()
            
            # Función para mostrar errores
            def mostrar_errores(e):
                codigo = codigo_input.value
                errores = obtener_errores(codigo)
                
                # Formatear los errores
                errores_texto = ""
                if errores:
                    for error in errores:
                        errores_texto += f"{error}\n"
                else:
                    errores_texto = "No se encontraron errores."
                
                errores_output.value = errores_texto
                page.update()
            
            #Función para abrir el selector de archivos
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
                            leading=ft.IconButton(ft.icons.ARROW_BACK, 
                                                on_click=lambda _: page.go("/")),
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
                                                ft.Text("Código fuente", 
                                                       size=14, 
                                                       weight=ft.FontWeight.W_500),
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
                                    
                                    #Resultados y errores
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Container(
                                                    content=ft.Column(
                                                        [
                                                            ft.Text("Resultados", 
                                                                   size=14, 
                                                                   weight=ft.FontWeight.W_500),
                                                            resultados_output
                                                        ],
                                                        spacing=5
                                                    ),
                                                    expand=True,
                                                    padding=5
                                                ),
                                                #Errores
                                                ft.Container(
                                                    content=ft.Column(
                                                        [
                                                            ft.Text("Errores", 
                                                                   size=14, 
                                                                   weight=ft.FontWeight.W_500),
                                                            errores_output
                                                        ],
                                                        spacing=5
                                                    ),
                                                    expand=True,
                                                    padding=5
                                                )
                                            ],
                                            spacing=0
                                        ),
                                        padding=ft.padding.only(bottom=10)
                                    ),
                                    #Btones
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
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Rodrigo Torres • Jesús Araujo",
                                            size=12,
                                            color=ft.colors.GREY_400,
                                            text_align=ft.TextAlign.RIGHT
                                        ),
                                        padding=ft.padding.only(top=10),
                                        alignment=ft.alignment.center_right
                                    )
                                ],
                                spacing=0
                            ),
                            padding=20,
                            border_radius=10
                        )
                    ]
                )
            )

        #vista sintactico
        elif page.route == "/sintactico":
            page.views.append(
                ft.View(
                    "/sintactico",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.ARROW_BACK, 
                                                on_click=lambda _: page.go("/")),
                            title=ft.Text("Analizador Sintáctico"),
                            center_title=True,
                            bgcolor="#121212",
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Analizador Sintáctico - En construcción", 
                                           size=20, 
                                           weight=ft.FontWeight.BOLD,
                                           text_align=ft.TextAlign.CENTER),
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