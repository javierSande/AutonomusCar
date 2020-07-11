#imports
import webiopi

# Libreria GPIO
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Definicion constantes                           #
# -------------------------------------------------- #

# GPIOs motor izquierdo
L1=17  # H-Bridge 1
L2=27 # H-Bridge 2

# GPIOs motor derecho
R1=10 # H-Bridge 3
R2=9 # H-Bridge 4

# -------------------------------------------------- #
# Funciones motor izquierdo                          #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)


def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Funciones motor derecho                            #
# -------------------------------------------------- #

def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

def right_forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

def right_backward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

# -------------------------------------------------- #
# Definicion macros                               #
# -------------------------------------------------- #

@webiopi.macro
def go_forward():
    left_forward()

@webiopi.macro
def go_backward():
    left_backward()

@webiopi.macro
def turn_left():
    right_forward()

@webiopi.macro
def turn_right():
    right_backward()

@webiopi.macro
def stop():
    left_stop()
    right_stop()

# -------------------------------------------------- #
# Iniciacializacion                                  #
# -------------------------------------------------- #

def setup():
# Instalacion GPIOs
    GPIO.setFunction(L1, GPIO.OUT)
    GPIO.setFunction(L2, GPIO.OUT)

    GPIO.setFunction(R1, GPIO.OUT)
    GPIO.setFunction(R2, GPIO.OUT)


def destroy():
    # Resetea las funciones GPIO
    GPIO.setFunction(L1, GPIO.IN)
    GPIO.setFunction(L2, GPIO.IN)

    GPIO.setFunction(R1, GPIO.IN)
    GPIO.setFunction(R2, GPIO.IN)
