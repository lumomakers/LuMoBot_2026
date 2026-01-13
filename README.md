# LuMoBot 2026

El control del robot se reliza mediande la libreria LumoBotLib.py.
En esta librería se encuentran las clases que gestionan los distintos elementos del robot y la clase principal **Robot**.

## Dispositivos que conforman LuMoBot 2026
1. **Raspberry Pi Pico**: Es el microcontrolador el robot
2. **Pantalla SSD1306**: Nos permite mostrar información en forma de texto o con expresiones de ojos para darle un poco de animación al robot.
3. **Sensor VL6180X**: Es un sensor de distancia óptico basado en tecnología FlightSense™ de STMicroelectronics, que utiliza el principio de tiempo de vuelo (Time-of-Flight, ToF) para medir con precisión la distancia a un objeto, independientemente de su reflectancia, color o textura. El VL6180X mide el tiempo que tarda la luz láser en viajar hasta el objeto y regresar al sensor, lo que permite mediciones más precisas y estables.
4. **Array de 5 sensores TCRT5000**: Este grupo de sensores IR se usa para el seguimiento de linea negra.
5. **Motores TT con encoders**: Este tipo de motores permite mayor precisión en el movimiento del robot gracias a los encoders.

## Acciones que podemos realizar con LuMoBot
Estas acciones son los métodos de la clase Robot a la que deberemos instanciar para poder usarlas. Son las siguintes:

1. **Movimientos bñasicos:**
    - parar()
    - avanzar()
    - retroceder()
    - girar_izquierda()
    - girar_derecha()
2. **Movimientos con encoders:**
    - girar_90_izquierda()
    - girar_90_derecha()
    - girar_180()
    - avanzar_distancia()
3. **Otras operaciones:**
    - seguir_linea()
    - evadir_obstaculo()
    - calibrar_distancia()
    - recorrido_cuadrado(lado_cm)
    - distancia()
4. **Uso de la pantalla:**
    - limpiar()
    - mostrar()
    - texto(text, x, y)
    - texto_centrado(texto, x, y)
    - muestra_cara(num)
    
## Funcionamiento de LuMoBot
Para poder usar el robot necesitaremos crear un **objeto** de la clase **Robot**, de esta manera podremos acceder a las diferentes funcionalidades.
```python
coche = Robot() # De esta manera ya tenemos acceso a las acciones del robot

# Movilidad el robot
coche.retroceder()
coche.parar()
coche.girar_izquierda()
coche.girar_derecha()
coche.avanzar(coche.VEL_LENTA) # VEL_LENTA, VEL_NORMAL

# Podemos hacer giros precisos
coche.girar_90_izquierda()
coche.girar_90_derecha()
```

## Usando la clase *Pantalla* para mostrar texto
```python
coche = Robot()

# Texto inicial
coche.limpiar() # Primero limpiamos la pantalla
coche.texto_centrado('L U M O B O T', 0,15) # Indicámos qué vamos a mostrar
coche.texto_centrado('2026', 0, 35)
coche.mostrar() # Damos la orden de mostrar la información deseada
```

## Usando la pantalla para mostrar una expresión
```python
coche.muestra_cara(3) # El número indica la expresión a mostrar según tabla
```

## Usando el sensor de distancia SVL6180X:
```python
coche = Robot()
# Mostramos los ojos abiertos 
coche.muestra_cara(0)
while True:
    distancia = coche.distancia() # Leemos la distancia con el sensor
    if distancia == None: # Por si obtiene lecturas falsas
        distancia = 255
    elif distancia < 100:
        coche.muestra_cara(8)      
    else:
        coche.muestra_cara(0)
```

## :smile: Prueba