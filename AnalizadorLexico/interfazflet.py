import flet as ft
from analizador import analizar_lexicamente, obtener_errores

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Analizador Léxico"
    page.window_width = 800
    page.window_height = 600
    page.padding = 20
    page.bgcolor = "#003135"  # Color de fondo de la ventana

    # Título (en blanco)
    title = ft.Text("Analizador Léxico", size=24, weight="bold", color="white")

    # Área para introducir código
    code_input = ft.TextField(
        multiline=True,
        min_lines=10,
        max_lines=10,
        hint_text="Introduzca su código aquí...",
        expand=True,
        bgcolor="#ffffff",  # Fondo blanco para el área de texto
    )

    # Sección de Resultados
    highlights = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=5,
        max_lines=5,
        hint_text="Resultados",
        expand=True,
        bgcolor="#ffffff",  # Fondo blanco para el área de texto
    )

    # Sección de Errores
    errores = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=5,
        max_lines=5,
        hint_text="Errores",
        expand=True,
        bgcolor="#ffffff",  # Fondo blanco para el área de texto
    )

    # Función para el botón de Resultados
    def on_highlights_click(e):
        codigo = code_input.value
        tokens = analizar_lexicamente(codigo)
        resultado = "\n".join([f"{token[0]} → {token[1]}" for token in tokens])
        highlights.value = resultado
        page.update()

    # Función para el botón de Errores
    def on_errores_click(e):
        codigo = code_input.value
        errores = obtener_errores(codigo)
        resultado = "\n".join(errores)
        errores.value = resultado
        page.update()

    # Botones
    button_highlights = ft.ElevatedButton(
        text="Resultados",
        bgcolor="#ffffff",
        color="#003135",
        on_click=on_highlights_click,
    )

    button_errores = ft.ElevatedButton(
        text="Errores",
        bgcolor="#ffffff",
        color="#003135",
        on_click=on_errores_click,
    )

    # Nombres de los autores (alineados a la derecha)
    autores = ft.Text("Rodrigo Torres\nJesús Araujo", size=14, italic=True, color="white")
    autores_container = ft.Container(autores, alignment=ft.alignment.center_right)

    # Diseño de la ventana
    page.add(
        ft.Column(
            [
                ft.Container(title, alignment=ft.alignment.center),  # Título
                ft.Container(code_input, expand=True),  # Área de código
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(highlights, expand=True),  # Resultados
                                ft.Container(button_highlights),  # Botón Resultados
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            [
                                ft.Container(errores, expand=True),  # Errores
                                ft.Container(button_errores),  # Botón Errores
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                autores_container,  # Autores (alineados a la derecha)
            ],
            expand=True,
        )
    )

# Ejecutar la aplicación
ft.app(target=main)
