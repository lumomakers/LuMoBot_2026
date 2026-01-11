'''
------------------------------------------------------------------------
LUMOBOT 2026

Utiliza Encoder V2
------------------------------------------------------------------------
'''

from machine import Pin, PWM, I2C, UART
from ssd1306 import SSD1306_I2C
import framebuf
import utime


# -------------------------------------------
# 					 CLASE OLED SD1306 
# -------------------------------------------
class Pantalla:
    def __init__(self, ancho=128, alto=64, i2c_id=0, scl_pin=9, sda_pin=8):
        self.ancho = ancho
        self.alto = alto
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.oled = SSD1306_I2C(self.ancho, self.alto, self.i2c)
        self.caras = ['mirando.pbm', 'cerrados.pbm', 'derecha.pbm', 'izquierda.pbm', 'enfado.pbm',
                      'risa.pbm', 'sospecha.pbm', 'triste.pbm', 'golpe.pbm']
    
    def limpiar(self):
        self.oled.fill(0)
    
    def mostrar(self):
        self.oled.show()
    
    def texto(self, texto, x, y, color=1):
        # color=1 es generalmente BLANCO (encendido)
        self.oled.text(str(texto), x, y, color)
    
    def texto_centrado(self, texto, x, y, color=1):
        # color=1 es generalmente BLANCO (encendido)
        texto_str = str(texto)
        ancho_texto = len(texto_str) * 8
        x = (self.ancho - ancho_texto) //2        
        self.oled.text(str(texto), x, y, color)
    
    def linea(self, x1, y1, x2, y2, color = 1):
        # Dibuja un alinea
        self.oled.line(x1, y1, x2, y2, color)
        
        
    def rectangulo (self, x, y, ancho, alto, color=1, relleno = False):
        # Dibuja un rectángulo
        if relleno:
            self.oled.fill_rect(x,y,ancho, alto, color)
        else:
            self.old.rect(x, y, ancho, alto, color)
    
    def barra_progreso(self, x, y, ancho, alto, porcentaje):
        # Dibuja barra de progreso
        
        # Marco
        self.rectangulo(x,y,ancho,alto, 1, False)
        # Relleno
        ancho_relleno = int(ancho - 2) * (porcentaje / 100)
        if ancho_relleno > 0:
            self.rectangulo (x + 1, y + 1, ancho_relleno, alto-2, 1, True)
    
    def mostrar_calibracion(self, titulo, valor, pulsos_izq=0, pulsos_der=0):
        '''
            Args:
                valor: valor actual
                pulsos_izq: Pulsos encoder izquierdo
                pulsos_der: Pulsos encoder derecho
        '''
        self.limpiar()
        self.texto_centrado(titulo, 0, 8)
        self.linea(0,20,self.ancho, 20)
        
        self.texto_centrado(f"Valor: {valor}",0,23)
        self.texto(f"Izq: {pulsos_izq}", 10, 35)
        self.texto(f"Der: {pulsos_der}", 10, 45)
        self.mostrar()
        
        
    def muestra_cara(self, num_cara):
        # Abre un archivo PBM
        archivo = '/imgs/'+self.caras[num_cara]
        with open(archivo, 'rb') as f:
            f.readline() # Numero magico
            f.readline() # Informacion
            f.readline() # Dimensiones
            data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
        self.oled.fill(0)
        self.oled.blit(fbuf, 0, 0)
        self.oled.show()
            
            
# -------------------------------------------
# 					 CLASE SENSOR VL6180X 
# -------------------------------------------
class VL6180X:
    """Driver para sensor VL6180X TOF"""
    
    # Registros del VL6180X
    IDENTIFICATION_MODEL_ID = 0x000
    SYSTEM_INTERRUPT_CONFIG = 0x014
    SYSTEM_INTERRUPT_CLEAR = 0x015
    SYSTEM_FRESH_OUT_OF_RESET = 0x016
    SYSRANGE_START = 0x018
    SYSRANGE_INTERMEASUREMENT_PERIOD = 0x01B
    RESULT_RANGE_STATUS = 0x04D
    RESULT_INTERRUPT_STATUS_GPIO = 0x04F
    RESULT_RANGE_VAL = 0x062
    
    def __init__(self, i2c_id=1, scl_pin=27, sda_pin=26, direccion=0x29):
        self.direccion = direccion
        self.i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
        self.init_sensor()
    
    def write_reg(self, reg, value):
        """Escribe en un registro de 16 bits"""
        self.i2c.writeto_mem(self.direccion, reg, bytes([value]), addrsize=16)
    
    def read_reg(self, reg):
        """Lee un registro de 16 bits"""
        return self.i2c.readfrom_mem(self.direccion, reg, 1, addrsize=16)[0]
    
    def init_sensor(self):
        """Inicializa el sensor VL6180X"""
        # Verificar si el sensor necesita inicialización
        if self.read_reg(self.SYSTEM_FRESH_OUT_OF_RESET) == 0x01:
            # Configuración obligatoria del sensor
            self.write_reg(0x0207, 0x01)
            self.write_reg(0x0208, 0x01)
            self.write_reg(0x0096, 0x00)
            self.write_reg(0x0097, 0xFD)
            self.write_reg(0x00e3, 0x00)
            self.write_reg(0x00e4, 0x04)
            self.write_reg(0x00e5, 0x02)
            self.write_reg(0x00e6, 0x01)
            self.write_reg(0x00e7, 0x03)
            self.write_reg(0x00f5, 0x02)
            self.write_reg(0x00D9, 0x05)
            self.write_reg(0x00DB, 0xCE)
            self.write_reg(0x00DC, 0x03)
            self.write_reg(0x00DD, 0xF8)
            self.write_reg(0x009f, 0x00)
            self.write_reg(0x00a3, 0x3c)
            self.write_reg(0x00b7, 0x00)
            self.write_reg(0x00bb, 0x3c)
            self.write_reg(0x00b2, 0x09)
            self.write_reg(0x00ca, 0x09)
            self.write_reg(0x0198, 0x01)
            self.write_reg(0x01b0, 0x17)
            self.write_reg(0x01ad, 0x00)
            self.write_reg(0x00FF, 0x05)
            self.write_reg(0x0100, 0x05)
            self.write_reg(0x0199, 0x05)
            self.write_reg(0x01a6, 0x1b)
            self.write_reg(0x01ac, 0x3e)
            self.write_reg(0x01a7, 0x1f)
            self.write_reg(0x0030, 0x00)
            
            # Configuraciones recomendadas
            self.write_reg(self.SYSTEM_INTERRUPT_CONFIG, 0x24)
            self.write_reg(self.SYSRANGE_INTERMEASUREMENT_PERIOD, 0x0A)
            
            # Limpiar bit de reset
            self.write_reg(self.SYSTEM_FRESH_OUT_OF_RESET, 0x00)
    
    def leer_distancia(self):
        """Lee la distancia en milímetros"""
        # Iniciar medición
        self.write_reg(self.SYSRANGE_START, 0x01)
        
        # Esperar a que termine la medición
        timeout = 100
        while timeout > 0:
            status = self.read_reg(self.RESULT_INTERRUPT_STATUS_GPIO)
            if (status & 0x04) != 0:
                break
            utime.sleep_ms(1)
            timeout -= 1
        
        if timeout == 0:
            return None
        
        # Leer distancia
        distancia = self.read_reg(self.RESULT_RANGE_VAL)
        
        # Limpiar interrupciones
        self.write_reg(self.SYSTEM_INTERRUPT_CLEAR, 0x07)
        
        return distancia



# -------------------------------------------
# 					 CLASE MOTOR 
# -------------------------------------------
class Motor:
    # Clase para controlar un motor DC a través del TB6612FNG
    def __init__(self, pwm_pin, in1_pin, in2_pin, nombre = "Motor"):
        '''
        Inicializa el motor
        Args:
            pwm_pin : Pin GPIO para PWM (velocidad)
            in1_pin : Pin GPIO para dirección 1
            in2_pin : Pin GPIO para dirección 2
            nombre: Nombre del motor para debugging
        '''
        self.nombre = nombre
        self.pwm = PWM(Pin(pwm_pin))
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.pwm.freq(1000)
        self.velocidad_actual = 0
        self.direccion_actual = 0
        
    def avanzar (self, velocidad=40000):
        # Gira el motor hacia adelante
        self.in1.value(0)
        self.in2.value(1)
        self.pwm.duty_u16(velocidad)
        self.velocidad_actual = velocidad
        self.direccion_actual = 1
    
    def retroceder(self, velocidad=40000):
        # Gira el motor hacia atrás
        self.in1.value(1)
        self.in2.value(0)
        self.pwm.duty_u16(velocidad)
        self.velocidad_actual = velocidad
        self.direccion_actual = -1        
    
    def parar(self):
        # Detiene el motor
        self.in1.value(0)
        self.in2.value(0)
        self.pwm.duty_u16(0)
        self.velocidad_actual = 0
        self.direccion_actual = 0
    
    def set_velocidad(self, velocidad, direccion):
        '''
        Establece la velocidad del motor
    
        Args:
            velocidad: 0 - 65535
            direccion: 1 (adelante), -1 (atrás), 0 (parar)
        '''
        if direccion == 1:
            self.avanzar(velocidad)
        elif direccion == -1:
            self.retroceder(velocidad)
        else:
            self.parar()
    
    
# -------------------------------------------
# 					 CLASE ENCODER 
# -------------------------------------------
class EncoderV2:
    # Clase para manejar encoder de cuadratura (canales A y B)
    
    def __init__(self, pin_a, pin_b, nombre = "Encoder"):
        '''
        Inicializar el encoder
        
        Args:
            pin_a: Pin GPIO para canal A
            pin_b: Pin GPIO para canal B
            nombre: Nombre del encoder
        '''
        self.nombre = nombre
        self.pin_a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(pin_b, Pin.IN, Pin.PULL_UP)
        self.pulsos = 0
        self.direccion = 1
        self.ultimo_estado_a = self.pin_a.value()
        
        # Configurar interrupcion
        self.pin_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._handler_irq)
        
    def _handler_irq(self, pin):
        # Manejador de interrupcion privado
        estado_a = self.pin_a.value()
        estado_b = self.pin_b.value()
        
        if estado_a != self.ultimo_estado_a:
            if estado_a == estado_b:
                self.pulsos += 1
                self.direccion = 1
            else:
                self.pulsos -= 1
                self.direccion = -1
        self.ultimo_estado_a = estado_a
        
    
    def reset(self):
        # Reinicia el contador de pulsos
        self.pulsos = 0
    
    def get_pulsos(self):
        # Devuelve el valor absoluto de pulsos
        return abs(self.pulsos)
    
    def get_direccion(self):
        # Devuelve la direccion de giro
        return self.direccion
        
# ---------------------------------------------------
# 					 CLASE CONTROLADOR DE MOTORES 
# ---------------------------------------------------    
class ControladorMotores:
    # Clase para controla el driver TB6612FNG con dos motores
    
    def __init__(self, motor_izq_config, motor_der_config, stby_pin):
        '''
        Inicializa el controlador de motores
        
        Args:
            motor_izq_config: tupla (pwm_pin, in1_pin, in2_pin)
            motor_der_config: tupla (pwm_pin, in1_pin, in2_pin
            stby_pin: Pin GPIO para STANBY
        '''
        
        self.motor_izq = Motor(*motor_izq_config, nombre="Motor Izquierdo")
        self.motor_der = Motor(*motor_der_config, nombre="Motor Derecho")
        self.stby = Pin(stby_pin, Pin.OUT)
        self.stby.value(1) # Activar controlador
    
    def avanzar(self, velocidad=40000):
        # Ambos motores hacia adelante
        self.motor_izq.avanzar(velocidad)
        self.motor_der.avanzar(velocidad)

    def retroceder(self, velocidad=40000):
        # Ambos motores hacia atrás
        self.motor_izq.retroceder(velocidad)
        self.motor_der.retroceder(velocidad)

    # Los sentidos de los giros estan cambniados por un error
    # en la conexion de los cables en la placa
    def girar_derecha(self, velocidad=35000):
        # Gira a izquierda (motor izq atrás, motor der adelante)
        self.motor_izq.retroceder(velocidad)
        self.motor_der.avanzar(velocidad)    
        
    def girar_izquierda(self, velocidad=35000):
        # Gira a derecha (motor izq adelante, motor der atrás)
        self.motor_izq.avanzar(velocidad)
        self.motor_der.retroceder(velocidad)
    
    def parar(self):
        # Detiene ambos motores
        self.motor_izq.parar()
        self.motor_der.parar()
    
    def set_velocidades(self, vel_izq, vel_der, dir_izq=1, dir_der=1):
        '''
        Establece velocidades individuales para cada motor
        
        Args:
            vel_izq: velocidad motor izquierdo (0-65535)
            vel_der: velocidad motor derecho (0-65535)
            dir_izq: direccion motor izquierdo (1/-1/0)
            dir_der: direccion motor derecho (1/-1/0)
        '''
        self.motor_izq.set_velocidad(vel_izq, dir_izq)
        self.motor_der.set_velocidad(vel_der, dir_der)
    

            

# ---------------------------------------------------
# 					 CLASE ROBOT PRINCIPAL 
# ---------------------------------------------------
class Robot:
    # Clase principal que integra todos los componentes del robot
    
    def __init__(self):
        # Inicializa el robot con todos sus componentes
        
        # Configuracion de pines
        print("Inicializando robot..")
        
        # Controlador de motores
        self.motores = ControladorMotores(
            motor_izq_config = (0, 1, 2), # PWM, IN1, IN2
            motor_der_config = (6, 4, 5), # PWM, IN1, IN2
            stby_pin = 3
        )
        
        # Encoders
        self.encoder_izq = EncoderV2(10, 11, "Encoder Izq")
        self.encoder_der = EncoderV2(12, 13, "Encoder Der")
        
        # Sensores
        # ------ Aqui van los datos de los sensores
        
        # Constantes de calibracion
        self.PULSOS_POR_CM = 52
        self.PULSOS_90_GRADOS = 455 #420
        self.DISTANCIA_SEGURA = 20
        
        # Velocidades
        self.VEL_NORMAL = 40000
        self.VEL_GIRO = 35000
        self.VEL_LENTA = 30000
        
        # Pantalla OLED
        self.pantalla = Pantalla(ancho=128, alto=64, i2c_id=0, scl_pin=9, sda_pin=8)
        self.sensor = VL6180X(i2c_id=1, scl_pin=27, sda_pin=26, direccion=0x29)
        
        print ("Robot inicializado correctamente")
        
    
    def reset_encoders(self):
        # Reinicia ambos encoders
        self.encoder_izq.reset()
        self.encoder_der.reset()
    
    def get_pulsos(self):
        # Obtiene los pulsos de ambos encoders
        return self.encoder_izq.get_pulsos(), self.encoder_der.get_pulsos()
    
    # -------- MOVIMIENTOS BÁSICOS --------
    
    def parar(self):
        # Detiene el robot
        self.motores.parar()
    
    def avanzar(self, velocidad = None):
        # Robot avanza
        if velocidad is None:
            velocidad = self.VEL_NORMAL
        self.motores.avanzar(velocidad)

    def retroceder(self, velocidad = None):
        # Robot retrocede
        if velocidad is None:
            velocidad = self.VEL_NORMAL
        self.motores.retroceder(velocidad)

    def girar_izquierda(self, velocidad = None):
        # Giro a izquierda
        if velocidad is None:
            velocidad = self.VEL_GIRO
        self.motores.girar_izquierda(velocidad)

    def girar_derecha(self, velocidad = None):
        # Giro a derecha
        if velocidad is None:
            velocidad = self.VEL_GIRO
        self.motores.girar_derecha(velocidad)
    
    # ------- MOVIMIENTOS PRECISOS CON ENCODERS -----
    
    def girar_90_izquierda(self):
        # gira 90 grados exactos a la izquierda
        self.reset_encoders()
        self.girar_izquierda()
        
        while True:
            p_izq, p_der = self.get_pulsos()
            #print(f"Giro 90º izq: {p_izq}, {p_der} pulsos")
            if p_izq >= self.PULSOS_90_GRADOS and p_der >= self.PULSOS_90_GRADOS:
                break
            utime.sleep_ms(5)
        
        self.parar()
        utime.sleep_ms(200)
        #print(f"Giro 90º izq: {p_izq}, {p_der} pulsos")
    
    
    def girar_90_derecha(self):
        # gira 90 grados exactos a la derecha
        self.reset_encoders()
        self.girar_derecha()
        
        while True:
            p_izq, p_der = self.get_pulsos()
            #print(f"Giro 90º der: {p_izq}, {p_der} pulsos")
            if p_izq >= self.PULSOS_90_GRADOS and p_der >= self.PULSOS_90_GRADOS:
                break
            utime.sleep_ms(5)
        
        self.parar()
        utime.sleep_ms(200)
        #print(f"Giro 90º der: {p_izq}, {p_der} pulsos")
    
    def girar_180(self):
        pass
    
    def avanzar_distancia(self, cm):
        pass
    
    # -------- SEGUIMIENTO DE LINEA -------
    
    def seguir_linea(self):
        pass
    
    # -------- EVITAR OBSTACULOS ----------
    
    def evadir_obstaculo(self):
        pass

    def distancia(self):
        return self.sensor.leer_distancia()
    
    # -------- CALIBRACION ----------------
    
    def calibrar_giro(self):
        """Calibra los pulsos necesarios para giro de 90°"""
        print("\n" + "="*50)
        print("CALIBRACIÓN DE GIRO 90°")
        print("="*50)
        print("Marca la posición inicial del robot")
        
        self.pantalla.limpiar()
        self.pantalla.texto_centrado("CALIBRACION", 0, 15)
        self.pantalla.texto_centrado("Giro 90", 0, 35)
        self.pantalla.mostrar()
        
        input("Presiona Enter para comenzar...")
        
        total_izq = 0
        total_der = 0
        
        for i in range(4):
            print(f"\nGiro {i+1}/4")
            self.pantalla.mostrar_calibracion(f"Giro {i+1}/4", "---", 0, 0)
            
            input("Presiona Enter...")
            
            self.reset_encoders()
            self.girar_derecha()
            utime.sleep_ms(330)
            self.parar()
            
            p_izq, p_der = self.get_pulsos()
            print(f"  Pulsos izq: {p_izq}, der: {p_der}")
            total_izq += p_izq
            total_der += p_der
            
            self.pantalla.mostrar_calibracion(f"Giro {i+1}/4", "OK", p_izq, p_der)
            utime.sleep_ms(1000)
        
        promedio = (total_izq + total_der) // 8
        
        print("\n" + "="*50)
        print("RESULTADO:")
        print(f"PULSOS_90_GRADOS = {promedio}")
        print("="*50)
        
        self.pantalla.limpiar()
        self.pantalla.texto_centrado("RESULTADO", 0,10)
        self.pantalla.texto_centrado(f"Pulsos 90:", 0, 20)
        self.pantalla.texto_centrado(str(promedio), 0, 35)
        self.pantalla.mostrar()
        utime.sleep_ms(2000)
        
        return promedio
    
    def calibrar_distancia(self):
        pass
    
    # -------- MODOS DE OPERACION ---------
    
    def modo_seguidor_linea(self):
        pass
    
    def modo_completo(self):
        pass
    
    def recorrido_cuadrado(self, lado_cm=50):
        pass
    
    # -------- PANTALLA --------------------

    def limpiar(self):
        self.pantalla.limpiar()
    
    def mostrar(self):
        self.pantalla.mostrar()
    
    def texto(self, texto, x, y):
        self.pantalla.texto(texto, x, y)
    
    def texto_centrado (self, texto, x, y):
        self.pantalla.texto_centrado(texto, x, y)
    
    def muestra_cara(self, num):
        self.pantalla.muestra_cara(num)
    
    
    # -------- TESTS -----------------------
    
    def test_motores(self):
        # Avanzar
        self.avanzar(self.VEL_LENTA)
        utime.sleep_ms(1000)
        self.parar()
        
        utime.sleep_ms(2000)
        
        # Retroceder
        self.retroceder(self.VEL_LENTA)
        utime.sleep_ms(1000)
        self.parar()
        
        utime.sleep_ms(2000)
        
        # Girar irquierda 1.5s
        self.girar_izquierda(self.VEL_LENTA)
        utime.sleep_ms(1500)
        self.parar()
        
    
    def test_encoders(self):
        pass
    
    def test_ultrasonido(self, num_mediciones=10):
        pass
    
    def test_sensores_ir(self, num_lecturas=20):
        pass
    
