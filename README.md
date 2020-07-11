# AutonomusCar

## Intorducción al proyecto
El obejetivo del proyecto es crear un coche autónomo capaz de detectar señales y obstáculos, contorlado por una Raspberry Pi 3.

## Hardware

- RaspberryPi 3
- Driver controlador de motores L298n
- piCamera
- Powerbank
- Coche Rc

## Entrenamiento

En un primer momento, configuraremos el coche para poder ser contolado a través de la RaspberryPi, que recibirá las instrucciones vía Wifi. Al mismo tiempo, la Raspberry compartirá las imágenes en tiempo real y la instrucción asociada a cada una, lo qeu servirá para entrenar la red neuronal.

Para ello nos serviremos del servicio Webiopi, creando un servidor a través del que activar los GPIO de la Raspberry.



Proyecto y código basado en el trabajod de:

Zheng Wang: https://zhengludwig.wordpress.com/projects/self-driving-rc-car/

Jorge Casas: https://jorgecasas.github.io/2017/08/22/autonomous-rc-car-construyendo-un-coche-autonomo

Hacker Players: https://www.hackplayers.com/2013/12/construye-tu-propio-rover-teledirigido-con-rpi-webiopi.html
