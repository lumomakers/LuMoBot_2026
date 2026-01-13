
![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/LogoLUMOBOT.png)

<!--<h1 align="center">
  <span style="color: yellow;">LuMoBot 2026</span>
</h1>
-->
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

En el siguiente ejemplo el robot reacciona cuando le acercamos cualquier objeto a menos de **10cm**, cuando reacciona por **5ª vez** el programa se detiene y el robot muestra una cara de enfado.
```python
from LumobotLib import *
import utime

coche = Robot() # Creamos nuestro objeto coche

contador = 0 # Contaremos las veces que detecta un obstaculo
# Iniciando movimiento (esta es la parte que interesa)
coche.muestra_cara(0)
while True: # Nuestro bucle infinito
    distancia = coche.distancia()
    if distancia == None: # Por si se despista en la lectura
        distancia = 255
    elif distancia < 100:
        coche.muestra_cara(8)
        contador += 1
        utime.sleep_ms(1000)
        print(contador)
        if contador == 5: # Si detecta el obstáculo 5 veces, FIN
            break 
    else:
        coche.muestra_cara(0)
        
coche.muestra_cara(4)
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

## Expresiones predefinidas
 Para mostrar la expresión que deseemos bastará con indicar, en la función **muestra_cara()**, el número asignado a la misma que puedes ver en la siguiente tabla :

Valor | Gesto | Imagen
--|--|--
0 | ojos abiertos | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/mirando.png)
1 | ojos cerrados | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/cerrados.png)
2 | derecha| ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/derecha2.png)
3 | izquierda | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/izquierda2.png)
4 | enfado | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/enfado.png)
5 | risa | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/risa.png)
6 | sospecha | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/sospecha.png)
7 | triste | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/triste.png)
8 | golpe | ![](https://github.com/lumomakers/LuMoBot_2026/blob/main/imgs/golpe.png)