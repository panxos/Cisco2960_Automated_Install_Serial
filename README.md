Este script es un ejemplo de cómo se puede automatizar la configuración de un switch Cisco 2960s GigaEthernet de 24 puertos mediante el uso de la librería de Python "argparse" y "serial". Utiliza argumentos de línea de comando para recibir información de configuración del usuario. Usa la librería serial para conectarse al switch a través de un puerto serial (en este caso /dev/ttyUSB0) con una velocidad de transmisión de 9600 baudios.

Una vez conectado, el script utiliza comandos específicos de Cisco para configurar el switch, como establecer el hostname, crear usuarios y contraseñas, configurar la VLAN nativa, configurar el gateway predeterminado, el dominio de red, el servidor DNS y el servidor NTP, y deshabilita la configuracion de https y http.

Al final, el script crea VLANs, las nombra y asigna IPs a cada una. También puede configurar diferentes aspectos de la red, como la seguridad, el cifrado de contraseñas, y otras configuraciones necesarias para hacer funcionar correctamente el switch en una red específica.

Para usar este script, primero necesitarás tener Python3 instalado en tu sistema. También necesitarás tener una conexión serial establecida con el switch Cisco 2960s GigaEthernet de 24 puertos al que deseas configurar.

Una vez que tengas Python3 y una conexión serial establecida, puedes ejecutar el script en tu terminal o línea de comando utilizando el siguiente formato:

```python3 Cisco_serial_2960s_24_Basico_v1.2.py hostname IP mascara gateway dominio dns usuario1 contrasena1 usuario2 contrasena2```

Un ejemplo serial:

```python3 Cisco_serial_2960s_24_Basico_v1.2.py MYNEWSW 10.0.0.2 255.255.255.0 10.0.0.1 MYDOMAIN.NET 1.1.1.1 admin passadmin user2 passuser2```


Donde cada uno de los argumentos es un parámetro necesario para configurar el switch, como el hostname, la IP de la VLAN 99, la máscara de red, el gateway predeterminado, el dominio de red, el servidor DNS, el nombre de usuario y la contraseña.

