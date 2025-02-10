import flet as ft

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

    # Sección de Resaltados
    highlights = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=5,
        max_lines=5,
        hint_text="Resaltados",
        expand=True,
        bgcolor="#ffffff",  # Fondo blanco para el área de texto
    )

    # Sección de Errores
    errors = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=5,
        max_lines=5,
        hint_text="Errores",
        expand=True,
        bgcolor="#ffffff",  # Fondo blanco para el área de texto
    )

    # Botones
    button_highlights = ft.ElevatedButton(text="Botón Resaltados", bgcolor="#ffffff", color="#003135")
    button_errors = ft.ElevatedButton(text="Botón Errores", bgcolor="#ffffff", color="#003135")

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
                                ft.Container(highlights, expand=True),  # Resaltados
                                ft.Container(button_highlights),  # Botón Resaltados
                            ],
                            expand=True,
                        ),
                        ft.Column(
                            [
                                ft.Container(errors, expand=True),  # Errores
                                ft.Container(button_errors),  # Botón Errores
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