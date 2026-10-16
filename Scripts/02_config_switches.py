"""
Despliegue de VLANs y puertos de acceso en los tres switches.

Recorre un inventario (lista de diccionarios) y aplica a cada switch sus comandos.
Pide usuario y contraseña al ejecutar: no hay credenciales escritas en el código.
Uso, con el entorno virtual activo:  python 02_config_switches.py
"""
import getpass
from netmiko import ConnectHandler

print("=== Automatización de VLANs y Puertos de Acceso ===")

usuario_ssh = input("Ingresa el usuario SSH: ")
clave_ssh = getpass.getpass("Ingresa la contraseña: ")

# Inventario estructurado con comandos específicos por equipo (IPs de gestión de laboratorio)
inventario_switches = [
    {
        'host': '192.168.99.2',  # SW1 (Distribución)
        'comandos': [
            'vlan 10', 'name ADMINISTRACION',
            'vlan 20', 'name PRODUCCION'
            # SW1 solo distribuye, no tiene PCs conectadas directamente
        ]
    },
    {
        'host': '192.168.99.3',  # Switch Administración
        'comandos': [
            'vlan 10', 'name ADMINISTRACION',
            'vlan 20', 'name PRODUCCION',
            # Asignar PCs a VLAN 10
            'interface range e0/1-3',
            'switchport mode access',
            'switchport access vlan 10',
            'spanning-tree portfast'
        ]
    },
    {
        'host': '192.168.99.4',  # Switch Producción
        'comandos': [
            'vlan 10', 'name ADMINISTRACION',
            'vlan 20', 'name PRODUCCION',
            # Asignar PC a VLAN 20
            'interface e0/1',
            'switchport mode access',
            'switchport access vlan 20',
            'spanning-tree portfast'
        ]
    }
]

# Recorrer el inventario y aplicar configuraciones
for equipo in inventario_switches:
    dispositivo = {
        'device_type': 'cisco_ios',
        'host': equipo['host'],
        'username': usuario_ssh,
        'password': clave_ssh,
        'secret': clave_ssh
    }

    try:
        print(f"\n--- Conectando a {equipo['host']} ---")
        conexion = ConnectHandler(**dispositivo)
        conexion.enable()

        print("Aplicando configuración...")
        salida = conexion.send_config_set(equipo['comandos'])

        # El equipo rechaza los comandos inválidos con líneas que empiezan con %
        errores = [linea for linea in salida.splitlines() if linea.strip().startswith('%')]
        if errores:
            print(f"Atención: {equipo['host']} rechazó estos comandos:")
            for linea in errores:
                print(linea)
        else:
            print(f"¡Éxito! Configuración aplicada en {equipo['host']}")

        conexion.save_config()
        conexion.disconnect()

    except Exception as error:
        print(f"Error al configurar {equipo['host']}: {error}")

print("\n=== Despliegue finalizado ===")
