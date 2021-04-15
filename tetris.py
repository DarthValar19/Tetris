import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

"""PIEZAS = (
    ((0, 0), (1, 0), (0, 1), (1, 1)), # Cubo
    ((0, 0), (1, 0), (1, 1), (2, 1)), # Z (zig-zag)
    ((0, 0), (0, 1), (1, 1), (1, 2)), # S (-Z)
    ((0, 0), (0, 1), (0, 2), (0, 3)), # I (línea)
    ((0, 0), (0, 1), (0, 2), (1, 2)), # L
    ((0, 0), (1, 0), (2, 0), (2, 1)), # -L
    ((0, 0), (1, 0), (2, 0), (1, 1)), # T
)
"""
with open("piezas.txt") as f:
    PIEZAS = []
    for linea in f:
        linea = linea.split("#")
        linea.pop(1)
        linea = linea[0].split(" ")
        for i in range(len(linea)):
            linea[i] = linea[i].split(";")
            for n in linea[i]:
                elemento = n.split(",")
                elemento = (int(elemento[0]), int(elemento[1]))
                linea[i][linea[i].index(n)] = elemento
            linea[i] = tuple(linea[i])
        PIEZAS.append(tuple(linea))
    tuple(PIEZAS)



def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    
    if pieza == None:
        numero_pieza = random.randrange(CUBO, T + 1)
        return PIEZAS[numero_pieza][0]
   
    return PIEZAS[pieza][0]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    posicion = ()
    
    for i in range(len(pieza)):
        x, y = pieza[i]
        posicion = posicion + ((x + dx, y + dy),)
           
    return posicion

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    pieza_inicial = trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0)
    superficie_consolidada = []
    juego = [pieza_inicial, superficie_consolidada]
     
    return juego

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    
    dimensiones_juego = (ANCHO_JUEGO , ALTO_JUEGO)
    
    return dimensiones_juego

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """

    return juego[0]

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    for i in juego[1]:
        if (x, y) == i:
            return True
      
def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    for x, y in juego[0]:
        if x == ANCHO_JUEGO - ANCHO_JUEGO and (x + direccion) == -1:
            return juego
        if x == ANCHO_JUEGO - 1 and (x + direccion) == 9:
            return juego
        for i in juego[1]:
            if (x + direccion, y) == i:
                return juego
    
    pieza_movida = trasladar_pieza(juego[0], direccion, 0)
    juego[0] = pieza_movida
    
    return juego

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    puntaje = 0
    cambiar_pieza = False
    if terminado(juego):
        cambiar_pieza = False
        return (juego, cambiar_pieza, puntaje)
 
    juego_nuevo = juego.copy()
    for x, y in juego_nuevo[0]:
        if y == ALTO_JUEGO - 1:
            if juego_nuevo[1] == []:
                juego_nuevo[1] = juego_nuevo[0]
            else:
                juego_nuevo[1] = juego_nuevo[1] + juego_nuevo[0]
            juego_nuevo[0] = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
            cambiar_pieza = True
            juego_nuevo[1], puntaje = buscar_y_borrar(juego_nuevo[1])
            return (juego_nuevo, cambiar_pieza, puntaje)

    juego_nuevo[0] = trasladar_pieza(juego_nuevo[0], 0 , 1)
    
    for x, y in juego_nuevo[0]: 
        for n in juego_nuevo[1]:
            if (x, y) == n:
                juego_nuevo[0] = juego[0]
                juego_nuevo[1] = juego_nuevo[1] + juego_nuevo[0]
                juego_nuevo[0] = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)
                cambiar_pieza = True
                juego_nuevo[1], puntaje = buscar_y_borrar(juego_nuevo[1])
                return(juego_nuevo, cambiar_pieza, puntaje)
    
    juego_nuevo[1] = tuple(juego_nuevo[1])
    
    return (juego_nuevo, cambiar_pieza, puntaje) 

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    
    for i in juego[0]:
        x, y = i
        for n in juego[1]:
            if (x, y) == n:
                return True
    return False
    
def buscar_y_borrar(superficie):
    """
    Recibe una lista o tupla y comprueba si hay una linea completada, si la hay la funcion elimina esa linea
    y devuelve la lista con la linea eliminada
    """
    
    filas_eliminadas = True
    superficie = list(superficie)
    puntaje_final = 0
    while filas_eliminadas:
        superficie_a_eliminar = buscar_filas_completas(superficie)
        if superficie_a_eliminar == []:
            break
        superficie, puntaje = borrar_filas_y_contar_puntaje(superficie, superficie_a_eliminar)
        puntaje_final += puntaje
    return tuple(superficie), puntaje_final
    
def borrar_filas_y_contar_puntaje(superficie, superficie_a_eliminar):
    numero_fila = 0
    puntaje = 0
    for y in range(ALTO_JUEGO):
        for n in superficie_a_eliminar:
            if y == n[1]:
                superficie.remove(n)
                numero_fila = y
        if numero_fila != 0:
            puntaje += 10
        for n in superficie:
            if n[1] < numero_fila:
                superficie[superficie.index(n)] = (n[0], n[1] + 1)
        numero_fila = 0
    return superficie, puntaje
    
def buscar_filas_completas(lista):
    eliminar_definitivo = []
    for y in range(ALTO_JUEGO):
        contador = 0
        eliminar_provisorio = []
        for n in lista:
            if n[1] == y:
                contador += 1
                eliminar_provisorio.append(n)
            if contador == 9:
                eliminar_definitivo += eliminar_provisorio 
                break
    return eliminar_definitivo      

def rotar(juego):
    pieza_ordenada = sorted(juego[0])
    primera_posicion = pieza_ordenada[0]
    pieza_en_origen = trasladar_pieza(pieza_ordenada, -primera_posicion[0], -primera_posicion[1])
    siguiente_rotacion = buscar_rotacion(pieza_en_origen)
    pieza_rotada = trasladar_pieza(siguiente_rotacion, primera_posicion[0], primera_posicion[1])
    for n in pieza_rotada:
        if n[0] not in range(ANCHO_JUEGO) or n[1] not in range(ALTO_JUEGO):
            return juego[0]
        elif n in juego[1]:
            return juego[0]
    return pieza_rotada
  
def buscar_rotacion(pieza):
    for elementos in PIEZAS:
        for rotacion in elementos:
            if pieza == rotacion:
                posicion_rotacion = elementos.index(rotacion) + 1
                if posicion_rotacion == len(elementos):
                    posicion_rotacion = 0
                return elementos[posicion_rotacion]