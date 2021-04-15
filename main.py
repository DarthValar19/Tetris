import tetris
import gamelib
import random
import csv
import time
ANCHO_PANTALLA = 330
ALTO_PANTALLA = 600
LADO_CUADRADOS = 30
ESPERA_DESCENDER = 8

class Juego():
    def __init__(self, grilla, superficies):
        self.grilla = grilla
        self.superficies = superficies
        self.siguiente_pieza = tetris.generar_pieza()
        self.puntaje = 0
      
def crear_juego(filas, columnas):
    grilla = {}
    for y in range(filas):
        for x in range(columnas):
            inicio_cuadrado = (LADO_CUADRADOS * (x + 1), LADO_CUADRADOS * (y + 2))
            final_cuadrado = (LADO_CUADRADOS * (x + 2), LADO_CUADRADOS * (y + 3))
            grilla[(x, y)] = [inicio_cuadrado, final_cuadrado]
    pieza_inicial = tetris.generar_pieza()
    game = tetris.crear_juego(pieza_inicial)
    juego = Juego(grilla, game)
    return juego   

def actualizar_juego(juego, tecla = None):
    if tecla == "r":
        juego.superficies[0] = tetris.rotar(juego.superficies)
    if tecla == None or tecla == "s":
        juego.superficies, cambiar_pieza, puntaje = tetris.avanzar(juego.superficies, juego.siguiente_pieza)
        juego.puntaje += puntaje
        if cambiar_pieza == True:
            juego.siguiente_pieza = tetris.generar_pieza()
    if tecla == "a":
        juego.superficies = tetris.mover(juego.superficies, tetris.IZQUIERDA)
    elif tecla == "d":
        juego.superficies = tetris.mover(juego.superficies, tetris.DERECHA)


def dibujar_interfaz(juego):
    if tetris.terminado(juego.superficies):
        lista_puntajes(juego, "puntajes.csv")
        return
    dibujar_grilla(tetris.ALTO_JUEGO, tetris.ANCHO_JUEGO)
    dibujar_piezas(juego)
    dibujar_siguiente(juego.siguiente_pieza)
    dibujar_puntaje(juego.puntaje)
    
def dibujar_piezas(juego):
    for i in juego.superficies[0]:
        inicio = juego.grilla[i][0]
        final = juego.grilla[i][1]
        gamelib.draw_rectangle(inicio[0], inicio[1], final[0], final[1], outline='white', fill="red")
    for n in juego.superficies[1]:
        inicio = juego.grilla[n][0]
        final = juego.grilla[n][1]
        gamelib.draw_rectangle(inicio[0], inicio[1], final[0], final[1], outline='white', fill="red")
        
    
def dibujar_grilla(filas, columnas):
    punto_inicial = (30, 60)
    for n in range(filas + 1):
        gamelib.draw_line(punto_inicial[0], punto_inicial[1] + LADO_CUADRADOS * n, ANCHO_PANTALLA - punto_inicial[0], punto_inicial[1] + LADO_CUADRADOS * n,
        fill='white', width=1)
    for n in range(columnas + 1):
        gamelib.draw_line(punto_inicial[0] + LADO_CUADRADOS * n, punto_inicial[1], punto_inicial[0] + LADO_CUADRADOS * n, ALTO_PANTALLA,
        fill='white', width=1)

def dibujar_siguiente(pieza):
    gamelib.draw_text('Siguiente pieza:', 210, 30)
    for x, y in pieza:
        inicio = (250 + 15 * (x + 2), 5 + 10 * (y + 1))
        final = (250 + 15 * (x + 3),5 + 10 * (y + 2))
        gamelib.draw_rectangle(inicio[0], inicio[1], final[0], final[1], outline='white', fill='red')

def dibujar_puntaje(puntaje):
    gamelib.draw_text(f"Puntaje: {puntaje}", 60, 30) 

def lista_puntajes(juego, ruta_lista_puntajes):
    lista_puntajes = []
    try:
        with open(ruta_lista_puntajes, "r", newline='') as f:
            lista_puntajes = csv.reader(f)
            lista_puntajes = list(lista_puntajes)
    except:
        with open(ruta_lista_puntajes, "x", newline='') as f:
            pass            
    with open(ruta_lista_puntajes, "w", newline='') as f:
        if len(lista_puntajes) < 10:
            nombre = gamelib.input("Ingresa tu nombre:")
            lista_puntajes.append([nombre, juego.puntaje])
        else:
            for nombre, puntaje in lista_puntajes:
                if int(puntaje) < juego.puntaje:
                    nombre = gamelib.input("Ingresa tu nombre:")
                    lista_puntajes.append([nombre, juego.puntaje])
                    break
        lista_puntajes = sorted(lista_puntajes, key = lambda elemento: int(elemento[1]), reverse = True)
        if len(lista_puntajes) > 10:
            lista_puntajes.pop(len(lista_puntajes) - 1)
        dibujar_lista_puntajes(lista_puntajes)
        escribir = csv.writer(f)
        for elem in lista_puntajes:
            escribir.writerow(elem)

def dibujar_lista_puntajes(lista):
    punto_inicial = (30,60)
    contador = 1
    for nombre, puntaje in lista:
        gamelib.draw_text(f"{nombre}:{puntaje}", punto_inicial[0] * 5, punto_inicial[1] + (punto_inicial[0] * contador))   
        contador += 1
    
def guardar_partida(juego, ruta):
    with open(ruta, "w") as f:
        escribir = [f"{juego.superficies[0]};",f"{juego.superficies[1]};",f"{juego.puntaje};",f"{juego.siguiente_pieza}"]
        f.writelines(escribir)

def cargar_partida(juego, ruta):
    with open(ruta) as f:
        partida = f.read()
        partida = partida.split(";")
        superficie = [convertir_partidas(partida[0]), convertir_partidas(partida[1])]
        game = Juego(juego.grilla, superficie)
        game.puntaje = int(partida[2])                 
        game.siguiente_pieza = convertir_partidas(partida[3])
    return game

def convertir_partidas(lista):
    nueva_lista = []
    lista = lista.split(",")
    contador = 0
    agregar = (0, 0)
    for elem in lista:
        numero = ""
        for x in elem:
            if x.isdigit():
                numero += x
        if contador == 0 and numero != "":
            contador += 1
            agregar = (int(numero), agregar[1])
            continue
        if contador == 1 and numero != "":
            contador = 0
            agregar = (agregar[0], int(numero))
            nueva_lista.append(agregar)
            agregar = (0,0)
        numero = ""
    return tuple(nueva_lista)
def main():
    # Inicializar el estado del juego
    gamelib.resize(ANCHO_PANTALLA, ALTO_PANTALLA)

    timer_bajar = ESPERA_DESCENDER
    
    juego = crear_juego(tetris.ALTO_JUEGO, tetris.ANCHO_JUEGO)
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        dibujar_interfaz(juego)
        gamelib.draw_end()
        
        if tetris.terminado(juego.superficies):
            time.sleep(10)
            return
        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              if tecla == "g":
                guardar_partida(juego, "partidas.txt")
              if tecla == "c":
                juego = cargar_partida(juego, "partidas.txt")
              if tecla == "Escape":
                return
              actualizar_juego(juego, tecla)
              # Actualizar el juego, según la tecla presionada

        timer_bajar -= 1
        if timer_bajar == 0:
            actualizar_juego(juego)
            timer_bajar = ESPERA_DESCENDER
            # Descender la pieza automáticamente

gamelib.init(main)