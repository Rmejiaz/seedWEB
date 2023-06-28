import RPi.GPIO as GPIO
import time

class MoverCamara():
    def __init__(self):
        self.DIR_PIN_MOTOR_1 = 2
        self.STEP_PIN_MOTOR_1 = 3
        self.ENABLE_PIN_MOTOR_1 = 4
        self.DIR_PIN_MOTOR_2 = 5
        self.STEP_PIN_MOTOR_2 = 6
        self.ENABLE_PIN_MOTOR_2 = 7

        self.LED_PIN = 17

        # Configuración de los finales de carrera
        self.X_ENDSTOP = 21
        self.Y_ENDSTOP = 26

        # Configuración de pasos y distancia
        self.PASOS_POR_VUELTA = 200
        self.DISTANCIA_POR_VUELTA = 38.39

        self.MM_PER_STEP_X = self.DISTANCIA_POR_VUELTA / self.PASOS_POR_VUELTA
        self.MM_PER_STEP_Y = self.DISTANCIA_POR_VUELTA / self.PASOS_POR_VUELTA

        # Configuración de la Raspberry Pi GPIO
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.X_ENDSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.Y_ENDSTOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.DIR_PIN_MOTOR_1, GPIO.OUT)
        GPIO.setup(self.STEP_PIN_MOTOR_1, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN_MOTOR_1, GPIO.OUT)
        GPIO.setup(self.DIR_PIN_MOTOR_2, GPIO.OUT)
        GPIO.setup(self.STEP_PIN_MOTOR_2, GPIO.OUT)
        GPIO.setup(self.ENABLE_PIN_MOTOR_2, GPIO.OUT)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.posiciones = [
                        (10, 10),  # Coordenadas para matriz[0][0]
                        (20, 15),  # Coordenadas para matriz[0][1]
                        (15, 20),  # Coordenadas para matriz[0][2]
                        (10, 20),  # Coordenadas para matriz[1][0]
                        (15, 15),  # Coordenadas para matriz[1][1]
                        (20, 10),  # Coordenadas para matriz[1][2]
                        (10, 15),  # Coordenadas para matriz[2][0]
                        (20, 20),  # Coordenadas para matriz[2][1]
                        (15, 10)   # Coordenadas para matriz[2][2]  
                    ]


    def girar_motores_ejexpositivo(self, pasos):
        # Configuración de dirección
        GPIO.output(self.DIR_PIN_MOTOR_1,GPIO.HIGH)
        GPIO.output(self.DIR_PIN_MOTOR_2,GPIO.LOW)

        # Activar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)

        # Girar los motores al mismo tiempo
        for _ in range(pasos):
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
            time.sleep(0.001)

        # Desactivar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)

    
    def girar_motores_ejexnegativo(self, pasos):
        # Configuración de dirección
        GPIO.output(self.DIR_PIN_MOTOR_1,  GPIO.LOW)
        GPIO.output(self.DIR_PIN_MOTOR_2,  GPIO.HIGH)

        # Activar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)

        # Girar los motores al mismo tiempo
        for _ in range(pasos):
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
            time.sleep(0.001)

            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
            time.sleep(0.001)
        
        # Desactivar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)    

    def girar_motores_ejeynegativo(self, pasos):
        # Configuración de dirección
        GPIO.output(self.DIR_PIN_MOTOR_1, not GPIO.LOW)
        GPIO.output(self.DIR_PIN_MOTOR_2, GPIO.HIGH)

        # Activar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)

        # Girar los motores al mismo tiempo
        for _ in range(pasos):
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
            time.sleep(0.002)
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
            time.sleep(0.002)

        # Desactivar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)
    
    def girar_motores_ejeypositivo(self, pasos):
        # Configuración de dirección
        GPIO.output(self.DIR_PIN_MOTOR_1, not GPIO.HIGH)
        GPIO.output(self.DIR_PIN_MOTOR_2, GPIO.LOW)

        # Activar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)

        # Girar los motores al mismo tiempo
        for _ in range(pasos):
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
            time.sleep(0.001)

        # Desactivar motores
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)

    # Función para mover el eje X hacia la posición de home
    def x_home(self):
        while GPIO.input(self.X_ENDSTOP) == GPIO.HIGH:
            # Mover el eje Y en dirección negativa hasta tocar el final de carrera
         GPIO.output(self.DIR_PIN_MOTOR_1,  GPIO.LOW)
         GPIO.output(self.DIR_PIN_MOTOR_2,  GPIO.HIGH)

        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)
        while GPIO.input(self.X_ENDSTOP) == GPIO.HIGH:
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
            GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
            time.sleep(0.001)
        GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
        GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)

    # Función para mover el eje Y hacia la posición de home
    def y_home(self):
        while GPIO.input(self.Y_ENDSTOP) == GPIO.HIGH:
        # Mover el eje Y en dirección negativa hasta tocar el final de carrera
         GPIO.output(self.DIR_PIN_MOTOR_1, not GPIO.LOW)
         GPIO.output(self.DIR_PIN_MOTOR_2, GPIO.HIGH)
         GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.LOW)
         GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.LOW)
         while GPIO.input(self.Y_ENDSTOP) == GPIO.HIGH:
             GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.HIGH)
             GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.HIGH)
             time.sleep(0.001)
             GPIO.output(self.STEP_PIN_MOTOR_1, GPIO.LOW)
             GPIO.output(self.STEP_PIN_MOTOR_2, GPIO.LOW)
             time.sleep(0.001)
         GPIO.output(self.ENABLE_PIN_MOTOR_1, GPIO.HIGH)
         GPIO.output(self.ENABLE_PIN_MOTOR_2, GPIO.HIGH)


    def home(self):
        #self.y_home()
        #self.x_home()
        print("Camara en home")

    # Movimiento de la cámara a una posición específica en mm
    def mover_camara(self, x_mm, y_mm):
        x_steps = int(x_mm / self.MM_PER_STEP_X)
        y_steps = int(y_mm / self.MM_PER_STEP_Y)
    
        self.girar_motores_ejexpositivo(x_steps)
        time.sleep(1)
        self.girar_motores_ejeypositivo(y_steps)
        time.sleep(1)
        
        
        print(x_steps,y_steps,"pasos")
    
    def pos_camara(self, pos):
        self.mover_camara(self.posiciones[pos-1][0], self.posiciones[pos-1][1])
        print("Camara en posición")

    def release_control(self):
        GPIO.cleanup()

    def led_on(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        print("Led prendido")
    
    def led_off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
        print("Led apagado")


