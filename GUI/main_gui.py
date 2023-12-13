import pygame as pg, sys, os
from Button import Button
from InputBox import InputBox
from Slider import Slider

path_juego = r'C:\Users\joaqu\OneDrive\Desktop\Joaquin Montiel-TP Juego'
sys.path.append(path_juego)
from Juego2 import Juego

path_db = r'C:\Users\joaqu\OneDrive\Desktop\Joaquin Montiel-TP Juego\DB.py'
sys.path.append(path_db)
from DB import obtener_puntuaciones


pg.init()

ANCHO = 800
ALTO = 600

pantalla = pg.display.set_mode((ANCHO, ALTO))
pg.display.set_caption("Menu")
fondo_menu = pg.transform.scale(pg.image.load(r"./sprites_juego\Fondo\fondo_menu.jpg"), (ANCHO, ALTO))

reloj = pg.time.Clock()
en_ejecucion = True
pausa = False

def get_font(tamanio):
    font_path = "./Fonts\ConcertOne-Regular.ttf"
    try:
        font = pg.font.Font(font_path, tamanio)
        return font
    except pg.error:
        print("Error al cargar la fuente.")
        return None

def iniciar_juego(jugador_nombre, nivel_seleccionado):
    # Instancio de la clase Juego 
    juego = Juego(jugador_nombre, nivel_seleccionado)
    # Ejecutar el juego
    juego.ejecutar_juego()
    # Puedes agregar más lógica aquí después de que el juego haya terminado, si es necesario
    print(f"Juego terminado para {jugador_nombre} en el nivel {nivel_seleccionado}")

def entrar_al_nivel(jugador_nombre):
    nivel_seleccionado = None
    title_font = get_font(60)
    level_font = get_font(30)
    level_buttons = [
        Button(image=None, pos=(400, 300), text_input="Nivel 1", font=level_font, base_color="Black",
                color="White"),
        Button(image=None, pos=(400, 345), text_input="Nivel 2", font=level_font, base_color="Black",
                color="White"),
        Button(image=None, pos=(400, 390), text_input="Nivel 3", font=level_font, base_color="Black",
                color="White")
    ]

    PLAY_BACK = Button(image=None, pos=(700, 500), text_input="<- Atrás", font=get_font(45),
                        base_color="Black", color="Blue")

    while True:
        pantalla.blit(fondo_menu, (0, 0))

        title_text = title_font.render(f"Selecciona un nivel, {jugador_nombre}:", True, "Black")
        title_rect = title_text.get_rect(center=(400, 200))
        pantalla.blit(title_text, title_rect)

        PLAY_BACK.changeColor(pg.mouse.get_pos())
        PLAY_BACK.update(pantalla)

        for button in level_buttons:
            button.changeColor(pg.mouse.get_pos())
            button.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(pg.mouse.get_pos()):
                    return None  # Volver al menú principal

                for button in level_buttons:
                    if button.checkForInput(pg.mouse.get_pos()):
                        nivel_seleccionado = button.text_input
                        return nivel_seleccionado

        pg.display.update()

def mostrar_tabla_posiciones():
    pantalla_resolucion = (800, 600)
    tabla_resolucion = (600, 500)

    # Calcular posición de la tabla centrada
    x_pos = (pantalla_resolucion[0] - tabla_resolucion[0]) // 2
    y_pos = (pantalla_resolucion[1] - tabla_resolucion[1]) // 2

    while True:
        fondo_tabla = pg.transform.scale(pg.image.load(r"./sprites_juego/Fondo/tabla_posiciones.png"), (600, 500))  
        pantalla.blit(fondo_tabla, (x_pos, y_pos))

        # Obtener las puntuaciones desde la base de datos
        puntuaciones = obtener_puntuaciones()

        # Mostrar las puntuaciones
        y_pos_puntuaciones = y_pos + 100
        for i, (nombre, puntuacion) in enumerate(puntuaciones, start=1):
            fila_texto = get_font(30).render(f"{i}. {nombre}: {puntuacion}", True, "Black")
            fila_rect = fila_texto.get_rect(center=(x_pos + tabla_resolucion[0] // 2, y_pos_puntuaciones))
            pantalla.blit(fila_texto, fila_rect)
            y_pos_puntuaciones += 50

        QUIT_BUTTON = Button(image=None, pos=(660, 80), text_input="X", font=get_font(45),
                                base_color="Blue", color="Black")

        posicion_mouse = pg.mouse.get_pos()
        QUIT_BUTTON.changeColor(posicion_mouse)
        QUIT_BUTTON.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(posicion_mouse):
                    ranking()

        pg.display.update()


def play():
    pg.display.set_caption("Play")
    nombre_jugador = ""
    entrada_activa = False
    input_box = InputBox(300, 300, 200, 40, get_font(30))

    while True:
        PLAY_MOUSE_POS = pg.mouse.get_pos()

        pantalla.blit(fondo_menu, (0, 0))

        PLAY_TEXT = get_font(60).render("Iniciar Juego", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 200))
        pantalla.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(700, 500), text_input="<- Atras", font=get_font(45),
                            base_color="Black", color="Blue")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pg.KEYDOWN:
                if entrada_activa:
                    if event.key == pg.K_RETURN:
                        entrada_activa = False
                        jugador_nombre = nombre_jugador
                        nivel_seleccionado = entrar_al_nivel(jugador_nombre)
                        if nivel_seleccionado is not None:
                            print(f"Jugador: {jugador_nombre}, Nivel seleccionado: {nivel_seleccionado}")
                            # Inicia el juego aquí
                            iniciar_juego(jugador_nombre, nivel_seleccionado)
                            return  # Salgo del bucle 
                    elif event.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        nombre_jugador += event.unicode
                elif event.key == pg.K_RETURN:
                    entrada_activa = True

            # Verifico si se ha presionado "Enter"
            if input_box.is_enter_pressed(event):
                entrada_activa = False
                jugador_nombre = input_box.text
                nivel_seleccionado = entrar_al_nivel(jugador_nombre)
                if nivel_seleccionado is not None:
                    print(f"Jugador: {jugador_nombre}, Nivel seleccionado: {nivel_seleccionado}")
                    # Inicia el juego aquí
                    iniciar_juego(jugador_nombre, nivel_seleccionado)
                    return
                
            input_box.handle_event(event)

        pantalla.blit(fondo_menu, (0, 0))

        PLAY_TEXT = get_font(60).render("Iniciar Juego", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400, 200))
        pantalla.blit(PLAY_TEXT, PLAY_RECT)

        input_box.update()
        input_box.draw(pantalla)

        PLAY_BACK.changeColor(pg.mouse.get_pos())
        PLAY_BACK.update(pantalla)

        pg.display.update()

def options():
    pg.display.set_caption("Options")

    while True:
        # Obtener todos los eventos una vez
        eventos = pg.event.get()
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        pantalla.blit(fondo_menu, (0, 0))

        OPTIONS_TEXT = get_font(45).render("Configuracion", True, "black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 230))
        pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)

        texto_volumen = get_font(25).render("Volumen", True, "Black")
        texto_rect = texto_volumen.get_rect(center=(400, 310))
        pantalla.blit(texto_volumen, texto_rect)

        OPTIONS_BACK = Button(image=None, pos=(700, 500), text_input="<- Atras", font=get_font(45), base_color="Black",
                            color="Blue")

        # Ajusta las coordenadas x e y según tus necesidades
        VOLUMEN = Slider(pantalla, master_x=330, master_y=300, x=330, y=360, w=150, h=5,
                        value=0.5, color_background="Black", color_circulo="Blue")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(pantalla)

        # Usar los eventos para ambas partes del código
        VOLUMEN.update(eventos)
        VOLUMEN.draw()

        for event in eventos:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pg.display.update()

def ranking():
    pantalla.blit(fondo_menu, (0, 0))
    while True:
        posicion_mouse = pg.mouse.get_pos()

        ranking_texto = get_font(60).render("Seleccionar Ranking", True, "Black")
        ranking_rect = ranking_texto.get_rect(center=(400, 200))
        pantalla.blit(ranking_texto, ranking_rect)

        RANKING_BACK = Button(image=None, pos=(700, 500), text_input="<- Atras", font=get_font(45),
                            base_color="Black", color="Blue")
        RANKING_BACK.changeColor(posicion_mouse)
        RANKING_BACK.update(pantalla)

        VER_TABLA_BUTTON = Button(image=None, pos=(400, 350), text_input="Puntaje", font=get_font(40), base_color="Black", color="White")
        VER_TABLA_BUTTON.changeColor(posicion_mouse)
        VER_TABLA_BUTTON.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if RANKING_BACK.checkForInput(posicion_mouse):
                    main_menu()
                elif VER_TABLA_BUTTON.checkForInput(posicion_mouse):
                    mostrar_tabla_posiciones()

        pg.display.update()

def main_menu():
    while True:

        pantalla.blit(fondo_menu, (0, 0))
        posicion_mouse = pg.mouse.get_pos()

        menu_texto = get_font(75).render("Menu Principal", True, "Black")
        menu_rect = menu_texto.get_rect(center=(400, 200))

        PLAY_BUTTON = Button(image=pg.image.load(r"./sprites_juego\Fondo\play.png"), pos=(400, 350),
                            text_input="PLAY", font=get_font(25), base_color="Black",color="White")
        OPTIONS_BUTTON = Button(image=pg.image.load(r"./sprites_juego\Fondo\play.png"), pos=(400, 400),
                            text_input="OPTIONS", font=get_font(25), base_color="Black",color="White")
        RANKING_BUTTON = Button(image=pg.image.load(r"./sprites_juego\Fondo\play.png"), pos=(400, 450),
                            text_input="RANKING", font=get_font(25), base_color="Black",color="White")
        QUIT_BUTTON = Button(image=pg.image.load(r"./sprites_juego\Fondo\play.png"), pos=(400, 500),
                            text_input="QUIT", font=get_font(25), base_color="Black",color="White")
        
        pantalla.blit(menu_texto, menu_rect)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, RANKING_BUTTON, QUIT_BUTTON]:
            button.changeColor(posicion_mouse)
            button.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(posicion_mouse):
                    play()
                if OPTIONS_BUTTON.checkForInput(posicion_mouse):
                    options()
                if RANKING_BUTTON.checkForInput(posicion_mouse):
                    ranking()
                if QUIT_BUTTON.checkForInput(posicion_mouse):
                    pg.quit()
                    sys.exit()

        pg.display.update()

main_menu()