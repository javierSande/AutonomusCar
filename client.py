# More info: https://github.com/javierSande/AutonomusCar
#
# Importamos librerias RPi.GPIO (entradas/salidas GPIO de Raspberry Pi) y time (para sleeps, etc...)
# Requiere previamente instalarla (pip install RPi.GPIO)
import RPi.GPIO as GPIO
import time
import io
import socket
import struct
import picamera
import threading

# Configure Raspberry Pi GPIO in BCM mode
GPIO.setmode(GPIO.BCM)


# Config vars. These IP and ports must be available in server firewall
log_enabled = False
server_ip = 'xxx.xxx.x.xx'
server_port_controller = 8002
server_port_camera = 8001

# Camera configuration
image_width = 640
image_height = 480
image_fps = 10
recording_time = 600

# Definition of GPIO pins in Raspberry Pi 3 (GPIO pins schema needed!)

GPIO_avanzar=17  # H-Bridge 1
GPIO_Retroceder=27 # H-Bridge 2

# GPIOs motor derecho
GPIO_izquierda=10 # H-Bridge 3
GPIO_derecha=9 # H-Bridge 4

# Class to handle the moves stream in client
class StreamClientMoves():

    def measure(self):

        move = 0;

        #Moves:
        # stop = 0
        # forward = 1
        # backward = -1
        # right = 1
        # left = 2

        if GPIO.output( GPIO_avanzar ) == 1:

            if GPIO.output( GPIO_derecha ) == 1:
                move = 1;

            elif GPIO.output( GPIO_izquierda ) == 1:
                move = 2;
            else:
                move = 1;


        elif GPIO.output( GPIO_Retroceder ) == 1:
            move = -1;


        return move


    def __init__(self):

        # Connect a client socket to server_ip:server_port_controller
        print( '+ Trying to connect to ultrasonic streaming server in ' + str( server_ip ) + ':' + str( server_port_controller ) );

        # Configure GPIO pins
        GPIO.setup( GPIO_avanzar, GPIO.OUT )
        GPIO.setup( GPIO_Retroceder, GPIO.OUT )
        GPIO.setup( GPIO_derecha, GPIO.OUT )
        GPIO.setup( GPIO_izquierda, GPIO.OUT )

        # Create socket and bind host
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect( ( server_ip, server_port_controller ) )

        try:
            while True:
                # Measure and send data to the host every 0.5 sec,
                # pausing for a while to no lock Raspberry Pi processors
                move = self.measure()
                if log_enabled: print( "Ultrasonic sensor distance: %.1f cm" % move[0] )
                client_socket.send( str(move[0]).encode('utf-8') )
                time.sleep( 0.2 )

        finally:
            # Ctrl + C to exit app (cleaning GPIO pins and closing socket connection)
            print( 'Control sensor connection finished!' );
            client_socket.close()

# Class to handle the jpeg video stream in client
class StreamClientVideocamera():

    def __init__(self):

        # Connect a client socket to server_ip:server_port_camera
        print( '+ Trying to connect to videocamera streaming server in ' + str( server_ip ) + ':' + str( server_port_camera ) );

        # create socket and bind host
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port_camera))
        connection = client_socket.makefile('wb')

        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (image_width, image_height)
                camera.framerate = image_fps

                # Give 2 secs for camera to initilize
                time.sleep(2)
                start = time.time()
                stream = io.BytesIO()

                # send jpeg format video stream
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    stream.seek(0)
                    connection.write(stream.read())
                    if time.time() - start > recording_time:
                        break
                    stream.seek(0)
                    stream.truncate()
            connection.write(struct.pack('<L', 0))

        finally:
            connection.close()
            client_socket.close()
            print( 'Videocamera stream connection finished!' );



# Class to handle the different threads in client
class ThreadClient():

    # Client thread to handle the video
    def client_thread_camera(host, port):
        print( '+ Starting videocamera stream client connection to ' + str( host ) + ':' + str( port ) )
        StreamClientVideocamera()

    # Client thread to handle contreller stream for training
    def client_thread_controller(host, port):
        print( '+ Starting control stream client connection to ' + str( host ) + ':' + str( port ) )
        StreamClientController()

    print( '+ Starting client - Logs ' + ( log_enabled and 'enabled' or 'disabled'  ) )

    thread_controller = threading.Thread( name = 'thread_controller', target = client_thread_controller, args = ( server_ip, server_port_controller ) )
    thread_controller.start()


    thread_videocamera = threading.Thread( name = 'thread_videocamera', target = client_thread_camera, args = ( server_ip, server_port_camera ) )
    thread_videocamera.start()


# Starting thread client handler
if __name__ == '__main__':
    ThreadClient()
