# More info: https://github.com/javierSande/AutonomusCar
#
# Import libraries
import threading
import socketserver
import socket
import cv2
import numpy as np
import math
import time
import os

# Config vars
log_enabled = True
server_ip = '192.168.1.51' #Your ip
server_port_camera = 8001
server_port_controller = 8002

# Video configuration
image_gray_enabled = False
image_fps = 24
image_width = 640
image_height = 480
image_height_half = int( image_height / 2 )

# Other vars
blue = (255, 0, 0)
yellow = (0,255,255)
red = (48, 79, 254)
green = (0, 168, 0)

# Font used in opencv images
#image_font = cv2.FONT_HERSHEY_PLAIN
image_font_size = 1.0
image_font_stroke = 2


# Datos para lineas de control visual. Array stroke_lines contiene 3 componentes:
#   0: Punto inicial (x,y)
#   1: Punto final (x,y)
#   2: Color de linea
#   3: Ancho de linea en px
# Para activarlo/desactivarlo: stroke_enable = True|False
stroke_enabled = True
stroke_width = 3
stroke_lines = [
   [ (0,image_height), ( int( image_width * 0.25 ), int( image_height/2 ) ), green, stroke_width ],
   [ (image_width,image_height), ( int( image_width * 0.75 ), int( image_height/2 ) ), green, stroke_width ]
];

# Class to handle the jpeg video stream received from client
class StreamHandlerVideocamera(socketserver.StreamRequestHandler):


    def handle(self):
        stream_bytes = b' '

        # stream video frames one by one
        try:
            print( 'Videocamera: Receiving images in server!' )
            while True:
                stream_bytes += self.rfile.read(1024)

                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last+2]
                    stream_bytes = stream_bytes[last+2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    image_gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # Visualization of lower half of the gray image
                    if image_gray_enabled:
                        half_gray = image_gray[image_height_half:image_height, :]

                    # Dibujamos lineas "control"
                    if stroke_enabled:
                        for stroke in stroke_lines:
                            cv2.line( image, stroke[0], stroke[1], stroke[2], stroke[3])

                    # Show images
                    cv2.imshow('image', image)
                    if image_gray_enabled:
                        cv2.imshow('mlp_image', half_gray)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        finally:
            cv2.destroyAllWindows()
            print( 'Connection closed on videostream thread' )

# Class to handle the actions received from the client during the training
class StreamHandlerConrols(socketserver.BaseRequestHandler):

    data = ' '

    def handle(self):
        global move
        move_float = 0.0

        try:
            print( 'Control sensor measure: Receiving data in server!' )
            while self.data:
                self.data = self.request.recv(1024)
                try:
                    move_float = float( self.data )
                except ValueError:
                    # No es float... porque hemos recibido algo del tipo b'123.123456.456' (es decir, por lag de la red
                    # o sobrecarga de nuestro sistema hemos recibido dos valores antes de ser capaces de procesarlo)
                    move_float = 1000.0

                move = round( move_float, 0)
                if log_enabled: print( 'Contol sensor measure received: ' + str( move ) )

        finally:
            print( 'Connection closed on control thread' )

# Class to handle the different threads
class ThreadServer( object ):

    # Server thread to handle the video
    def server_thread_camera(host, port):
        print( '+ Starting videocamera stream server in ' + str( host ) + ':' + str( port ) )
        server = socketserver.TCPServer((host, port), StreamHandlerVideocamera)
        server.serve_forever()


    # Server thread to handle ultrasonic distances to objects
    def server_thread_controller(host, port):
        print( '+ Starting control stream server in ' + str( host ) + ':' + str( port ) )
        server = socketserver.TCPServer((host, port), StreamHandlerConrols)
        server.serve_forever()

    print( '+ Starting server - Logs ' + ( log_enabled and 'enabled' or 'disabled'  ) )


    thread_controller = threading.Thread( name = 'thread_controller', target = server_thread_controller, args = ( server_ip, server_port_controller ) )
    thread_controller.start()

    thread_videocamera = threading.Thread( name = 'thread_videocamera', target = server_thread_camera, args = ( server_ip, server_port_camera ) )
    thread_videocamera.start()



# Starting thread server handler
if __name__ == '__main__':
    try:
        ThreadServer()

    except KeyboardInterrupt:
        # Rename the folder that collected all of the test frames. Then make a new folder to collect next round of test frames.
        #os.rename(  './test_frames_temp', './test_frames_SAVED/test_frames_{}'.format(timestr))
        #os.makedirs('./test_frames_temp')
        print ( 'Server stopped!' )
