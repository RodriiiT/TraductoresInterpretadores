import flet as ft
import os
from analizador_lexico import analizar_lexicamente, obtener_errores
from analizador_sintactico import generar_arbol_sintactico
from analizador_semantico import analizar_semanticamente, obtener_tabla_simbolos_texto, obtener_ast_anotado

def main(page: ft.Page):
    page.title = "Fases de un compilador"
    page.theme_mode = "dark"
    page.bgcolor = "#121212" 
    page.padding = 20
    page.scroll = "auto"

    # Configurar la altura de la ventana
    page.window.height = 900
    page.window_resizable = True
    
    # Variable global para el código
    codigo_global = ft.TextField(
        multiline=True,
        min_lines=15,
        max_lines=15,
        hint_text="Introduzca su código Java aquí...",
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

    def on_file_picked(e):
        if e.files and len(e.files) > 0:
            selected_file = e.files[0]
            try:
                with open(selected_file.path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    codigo_global.value = content
                    page.update()
            except Exception as ex:
                print(f"Error al leer el archivo: {ex}")

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def route_change(route):
        page.views.clear()

        def abrir_selector_archivos(e):
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["java"]
            )

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
                                ft.Container(height=20),
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
                                codigo_global,
                                ft.Container(height=20),
                                ft.Row(
                                    [
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
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10
                                ),
                                ft.Container(height=20),
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

        # Vista Léxico
        elif page.route == "/lexico":
            resultados_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=300
            )

            errores_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=300
            )

            def analizar_codigo(e):
                codigo = codigo_global.value
                tokens = analizar_lexicamente(codigo)

                resultados_table.controls.clear()
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
                codigo = codigo_global.value
                errores = obtener_errores(codigo)

                errores_table.controls.clear()
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

            botones_accion = ft.Row(
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
                                    botones_accion,
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
                                        height=400
                                    ),
                                ],
                                spacing=10
                            ),
                            padding=20,
                            border_radius=10
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )

        # Vista Sintáctico
        elif page.route == "/sintactico":
            tree_image = ft.Image(src="arbol_sintactico.png", width=400, height=300)
            errores_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=300
            )

            def generar_arbol(e):
                codigo = codigo_global.value
                generar_arbol_sintactico(codigo)
                tree_image.src = "arbol_sintactico.png"
                page.update()

            def mostrar_errores(e):
                codigo = codigo_global.value
                errores = obtener_errores(codigo)
                errores_table.controls.clear()
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
                errores_table.controls.clear()
                page.update()

            botones_accion = ft.Row(
                [
                    ft.ElevatedButton(
                        "Errores",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            bgcolor={"": "#1DB954"}
                        ),
                        on_click=mostrar_errores
                    ),
                    ft.ElevatedButton(
                        "Árbol",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            bgcolor={"": "#1DB954"}
                        ),
                        on_click=generar_arbol
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

            page.views.append(
                ft.View(
                    "/sintactico",
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
                                    botones_accion,
                                    ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Text("Errores", size=14, weight=ft.FontWeight.W_500),
                                                    errores_table
                                                ]),
                                                expand=True,
                                                padding=ft.padding.all(10)
                                            ),
                                            tree_image
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            ),
                            padding=20,
                            border_radius=10,
                            expand=True,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )

        # Vista Semántico
        elif page.route == "/semantico":
            errores_semanticos_table = ft.ListView(
                auto_scroll=True,
                expand=True,
                height=200
            )
            
            tabla_simbolos_text = ft.TextField(
                multiline=True,
                min_lines=10,
                max_lines=10,
                read_only=True,
                bgcolor="#282828",
                border_color="transparent",
                border_radius=8,
                text_size=14,
                color="#FFFFFF"
            )
            
            ast_anotado_text = ft.TextField(
                multiline=True,
                min_lines=10,
                max_lines=10,
                read_only=True,
                bgcolor="#282828",
                border_color="transparent",
                border_radius=8,
                text_size=14,
                color="#FFFFFF"
            )
            
            def analizar_semantica(e):
                codigo = codigo_global.value
                tabla, errores = analizar_semanticamente(codigo)
                
                tabla_simbolos_text.value = obtener_tabla_simbolos_texto(tabla)
                ast_anotado_text.value = obtener_ast_anotado(tabla)
                
                errores_semanticos_table.controls.clear()
                errores_semanticos_table.controls.append(
                    ft.Row([
                        ft.Text("Línea", weight=ft.FontWeight.BOLD, width=50),
                        ft.Text("Error", weight=ft.FontWeight.BOLD, width=300)
                    ])
                )
                
                if errores:
                    for linea, mensaje in errores:
                        linea_str = str(linea) if linea != 0 else "Global"
                        errores_semanticos_table.controls.append(
                            ft.Row([
                                ft.Text(linea_str, width=50),
                                ft.Text(mensaje, width=300)
                            ])
                        )
                else:
                    errores_semanticos_table.controls.append(
                        ft.Row([
                            ft.Text(""),
                            ft.Text("No se encontraron errores semánticos.", width=300)
                        ])
                    )
                
                page.update()
            
            def mostrar_errores_semanticos(e):
                codigo = codigo_global.value
                _, errores = analizar_semanticamente(codigo)
                
                errores_semanticos_table.controls.clear()
                errores_semanticos_table.controls.append(
                    ft.Row([
                        ft.Text("Línea", weight=ft.FontWeight.BOLD, width=50),
                        ft.Text("Error", weight=ft.FontWeight.BOLD, width=300)
                    ])
                )
                
                if errores:
                    for linea, mensaje in errores:
                        linea_str = str(linea) if linea != 0 else "Global"
                        errores_semanticos_table.controls.append(
                            ft.Row([
                                ft.Text(linea_str, width=50),
                                ft.Text(mensaje, width=300)
                            ])
                        )
                else:
                    errores_semanticos_table.controls.append(
                        ft.Row([
                            ft.Text(""),
                            ft.Text("No se encontraron errores semánticos.", width=300)
                        ])
                    )
                
                page.update()
            
            def mostrar_tabla_simbolos(e):
                codigo = codigo_global.value
                tabla, _ = analizar_semanticamente(codigo)
                tabla_simbolos_text.value = obtener_tabla_simbolos_texto(tabla)
                page.update()
            
            def limpiar_resultados(e):
                errores_semanticos_table.controls.clear()
                tabla_simbolos_text.value = ""
                ast_anotado_text.value = ""
                page.update()
                
            botones_accion = ft.Row(
                [
                    ft.ElevatedButton(
                        "Analizar",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            bgcolor={"": "#1DB954"}
                        ),
                        on_click=analizar_semantica
                    ),
                    # ft.ElevatedButton(
                    #     "Errores",
                    #     style=ft.ButtonStyle(
                    #         shape=ft.RoundedRectangleBorder(radius=20),
                    #         bgcolor={"": "#1DB954"}
                    #     ),
                    #     on_click=mostrar_errores_semanticos
                    # ),
                    # ft.ElevatedButton(
                    #     "Tabla de Símbolos",
                    #     style=ft.ButtonStyle(
                    #         shape=ft.RoundedRectangleBorder(radius=20),
                    #         bgcolor={"": "#1DB954"}
                    #     ),
                    #     on_click=mostrar_tabla_simbolos
                    # ),
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
            
            page.views.append(
                ft.View(
                    "/semantico",
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                            title=ft.Text("Analizador Semántico"),
                            center_title=True,
                            bgcolor="#121212",
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    botones_accion,
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Errores Semánticos", size=14, weight=ft.FontWeight.W_500),
                                            errores_semanticos_table
                                        ]),
                                        padding=ft.padding.all(10)
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Tabla de Símbolos", size=14, weight=ft.FontWeight.W_500),
                                            tabla_simbolos_text
                                        ]),
                                        padding=ft.padding.all(10)
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("AST Anotado", size=14, weight=ft.FontWeight.W_500),
                                            ast_anotado_text
                                        ]),
                                        padding=ft.padding.all(10)
                                    ),
                                ],
                                spacing=15
                            ),
                            padding=20,
                            border_radius=10,
                            expand=True,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO
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