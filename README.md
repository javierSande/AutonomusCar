# AutonomusCar

## Intorducción al proyecto
El obejetivo del proyecto es crear un coche autónomo capaz de detectar señales y obstáculos, contorlado por una Raspberry Pi 3.

<img src="https://github.com/javierSande/AutonomusCar/blob/master/coche.jpg?raw=true">

## Preparación

### Hardware

- RaspberryPi 3
- Driver controlador de motores L298n
- piCamera
- Powerbank
- Coche Rc

### Software

- Python >3.7
- OpenCV
- Gpiozero

### Preparación

1. Instalar [`gpiozero`](https://gpiozero.readthedocs.io)
2. Instalar OpenCv
3. Hacer  ```git clone https://github.com/javierSande/AutonomusCar```

## Funcionamiento

### Recolección de datos para el entrenamiento

Durante el entrenamiento, la RAspberry Pi enviará mediante streaming las imagenes que capte al ordenador principal en tiempo real. Simultáneamente, el usuario el ordenador enviará a la RPi el movimiento deseado y guardará un los bits de imagen y la dirección del coche tomada para ese caso.

Para ello debemos ejecutar el script `video_stream.py` en la RPi y collectData.py en el ordenador principal.

### Entrenamiento

Para el entrenamiento de la red neuronal usaremos los datos recolectados anteriormente. Para ello debemos ejecutar en el ordenador principal `training.py` y `model.py`. Estos programas generaran un modelo que se almacena en formato `.xml`.

### Conducción Autónoma

Para la conducción autónoma del coche, debemos ejecutar  `video_stream.py` en la RPi y los scripts `driver.py` y `driverHelp.py` en el ordenador principal, utilizando el `model.xml``generado durante el entrenamiento.


## Referencias
Proyecto y código basado en el trabajo de:

Zheng Wang: https://zhengludwig.wordpress.com/projects/self-driving-rc-car/

Jorge Casas: https://jorgecasas.github.io/2017/08/22/autonomous-rc-car-construyendo-un-coche-autonomo

Hacker Players: https://www.hackplayers.com/2013/12/construye-tu-propio-rover-teledirigido-con-rpi-webiopi.html
