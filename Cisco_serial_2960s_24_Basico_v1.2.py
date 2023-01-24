#!/usr/bin/env python3

import argparse
import sys
import serial
import time
from datetime import datetime

# Define los argumentos del script
parser = argparse.ArgumentParser(description="Script para configurar un switch Cisco 2960s GigaEthernet de 24 puertos")
parser.add_argument("hostname", help="Nombre del host del switch")
parser.add_argument("ip", help="IP de la VLAN 99")
parser.add_argument("mascara", help="Máscara de red de la VLAN 99")
parser.add_argument("gateway", help="Gateway predeterminado")
parser.add_argument("dominio", help="Dominio de red")
parser.add_argument("dns", help="Servidor DNS")
parser.add_argument("usuario1", help="Nombre de usuario 1")
parser.add_argument("contrasena1", help="Contraseña de usuario 1")
parser.add_argument("usuario2", help="Nombre de usuario 2")
parser.add_argument("contrasena2", help="Contraseña de usuario 2")


args = parser.parse_args()

# Crea una conexión serial al switch
conn = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

#entran en modo privilegiado
conn.write(b"enable\n")
conn.write(b"configure terminal\n")

# Configura el hostname
conn.write(f"hostname {args.hostname}\n".encode())

# Pide la contraseña de MODO ENABLE
enable_secret = input("Ingrese la contraseña de enable secret deseada: ")
conn.write(b"enable\n")
conn.write(b"configure terminal\n")
conn.write(f"enable secret {enable_secret}\n".encode())

# Crear usuario 1
conn.write(f"username {args.usuario1} privilege 15 password {args.contrasena1}\n".encode())

# Crear usuario 2
conn.write(f"username {args.usuario2} privilege 15 password {args.contrasena2}\n".encode())

# Crear usuario monitor
conn.write(f"username m0n1t0r privilege 1 password m0n1t00r_2023\n".encode())

#Cifrado de Contraseñas
conn.write(b"service password-encryption\n")

#Configura el gateway predeterminado
conn.write(f"ip default-gateway {args.gateway}\n".encode())

# Configura el dominio de red
conn.write(f"ip domain-name {args.dominio}\n".encode())

# Desactiva la búsqueda de dominio
conn.write(b"no ip domain-lookup\n")

# Configura el servidor DNS
conn.write(f"ip name-server {args.dns}\n".encode())

# Configura el servidor NTP
conn.write(b"ntp server 200.54.149.24\n")

#desabilita la configuradion de https y http
conn.write(b"no ip http server\n")
conn.write(b"no ip http secure-server\n")

# Configura la VLAN nativa o IP de administración en la VLAN 99
conn.write(b"interface VLAN 99\n")
conn.write(f"ip address {args.ip} {args.mascara}\n".encode())
conn.write(b"no shutdown\n")
conn.write(b"exit\n")



# Crear VLANs
conn.write(b"vlan 100\n")
conn.write(b"name RED_LOCAL\n")
conn.write(b"exit\n")
conn.write(b"interface VLAN 100\n")
conn.write(b"ip address 10.200.236.253 255.255.255.0\n")
conn.write(b"no shutdown\n")
conn.write(b"exit\n")

conn.write(b"vlan 200\n")
conn.write(b"name RED_TV\n")
conn.write(b"exit\n")
conn.write(b"interface VLAN 200\n")
conn.write(b"ip address 10.200.237.253 255.255.255.0\n")
conn.write(b"no shutdown\n")
conn.write(b"exit\n")

conn.write(b"vlan 300\n")
conn.write(b"name RED_WIFI\n")
conn.write(b"exit\n")
conn.write(b"interface VLAN 300\n")
conn.write(b"ip address 172.15.100.253 255.255.255.192\n")
conn.write(b"no shutdown\n")
conn.write(b"exit\n")

conn.write(b"vlan 400\n")
conn.write(b"name RED_SEC\n")
conn.write(b"exit\n")
conn.write(b"interface VLAN 400\n")
conn.write(b"ip address 192.168.145.253 255.255.255.192\n")
conn.write(b"no shutdown\n")
conn.write(b"exit\n")

conn.write(b"vlan 500\n")
conn.write(b"name RED_SEC2\n")
conn.write(b"exit\n")
conn.write(b"interface VLAN 500\n")
conn.write(b"ip address 192.168.146.253 255.255.255.192\n")
conn.write(b"no shutdown\n")
conn.write(b"exit\n")

# Configurar la interface 23 y 24 como TRUNK
conn.write(b"interface range gigabitEthernet 0/23 - 24\n")
conn.write(b"switchport mode trunk\n")
conn.write(b"switchport trunk native vlan 99\n")
conn.write(b"spanning-tree portfast\n")
conn.write(b"exit\n")

# Configurar GIGA 0/1 - en Vlan99
conn.write(b"interface gigabitEthernet 0/1\n")
conn.write(b"switchport mode access\n")
conn.write(b"switchport access vlan 99\n")
conn.write(b"spanning-tree portfast\n")
conn.write(b"exit\n")

# Crear Link Aggregation
conn.write(b"interface port-channel 1\n")
conn.write(b"channel-group 23 mode active\n")
conn.write(b"exit\n")
conn.write(b"interface port-channel 23\n")
conn.write(b"description TRONCAL RT-SW\n")
conn.write(b"switchport mode trunk\n")
conn.write(b"switchport trunk native vlan 99\n")
conn.write(b"exit\n")

#Configure SSH
conn.write(b"crypto key generate rsa\n")
conn.write(b"ip ssh version 2\n")
conn.write(b"ip ssh time-out 60\n")
conn.write(b"ip ssh authentication-retries 2\n")
conn.write(b"line vty 0 15\n")
conn.write(b"transport input ssh\n")

#Configura la Vty de la consola
conn.write(b"line vty 0 4\n")
conn.write(b"login local\n")
conn.write(b"transport input all\n")
conn.write(b"exit\n")

# Guarda la configuración
conn.write(b"end\n")
conn.write(b"wr\n")

# Mostrar configuración
conn.write(b"end\n")
conn.write(b"show running-config\n")

# Cerrar conexión
conn.close()