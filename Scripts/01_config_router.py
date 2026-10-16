"""
Configuración base del router (capa 3): seguridad, SSH, router-on-a-stick y SNMP.

Pide usuario y contraseña al ejecutar: no hay credenciales escritas en el código.
Uso, con el entorno virtual activo:  python 01_config_router.py
"""
import getpass
from netmiko import ConnectHandler

print("=== Configuración base del router ===")
usuario_ssh = input("Ingresa el usuario SSH: ")
clave_ssh = getpass.getpass("Ingresa la contraseña: ")

dispositivo = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.10',   # IP de laboratorio (red host-only)
    'username': usuario_ssh,
    'password': clave_ssh,
    'secret': clave_ssh,       # clave de enable (en este laboratorio es la misma)
}

try:
    # Inicia la sesión SSH y entra al modo privilegiado
    conexion = ConnectHandler(**dispositivo)
    conexion.enable()
    print("¡Conexión exitosa al router!")

    # Variables
    nombre = 'RouterCentral'
    passw = clave_ssh  # se usa para el enable secret y la línea AUX
    comunidad = getpass.getpass("Ingresa la comunidad SNMP (solo lectura): ")

    print("\n--- Configuración de Direccionamiento IP ---")
    print("Ingresa la IP y la máscara separadas por un espacio (Ej: 192.168.10.1 255.255.255.0)")

    vlan10 = input("Ingresa la IP para la subinterfaz de la VLAN 10: ")
    vlan20 = input("Ingresa la IP para la subinterfaz de la VLAN 20: ")
    vlan99 = input("Ingresa la IP para la subinterfaz de la VLAN 99 (Gestión): ")

    # Comandos de configuración
    comandos = [
        f'hostname {nombre}',
        'banner motd #Acceso solo a personal autorizado#',
        'service password-encryption',

        # Configurar SSH
        'ip ssh version 2',

        # Configurar consola
        'line console 0',
        'logging synchronous',
        'exit',

        # Configurar Enable Secret
        f'enable secret {passw}',

        # Configurar Aux
        'line aux 0',
        f'password {passw}',
        'login',
        'exit',

        # 1. Encender el puerto físico
        'interface e0/0',
        'no shutdown',
        'exit',

        # 2. Crear subinterfaz VLAN 10
        'interface e0/0.10',
        'encapsulation dot1Q 10',
        f'ip address {vlan10}',

        # 3. Crear subinterfaz VLAN 20
        'interface e0/0.20',
        'encapsulation dot1Q 20',
        f'ip address {vlan20}',

        # 4. Crear subinterfaz VLAN 99 (Gestión)
        'interface e0/0.99',
        'encapsulation dot1Q 99',
        f'ip address {vlan99}',
        'exit',

        # 5. SNMP de solo lectura, limitado a la red host-only
        'ip access-list standard SNMP-ZABBIX',
        'permit 192.168.56.0 0.0.0.255',
        'exit',
        f'snmp-server community {comunidad} RO SNMP-ZABBIX',
    ]

    salida = conexion.send_config_set(comandos, read_timeout=90)

    # No se imprime la salida completa porque incluye las claves enviadas.
    # Solo se muestran los comandos que el router rechazó (líneas que empiezan con %).
    errores = [linea for linea in salida.splitlines() if linea.strip().startswith('%')]
    print("\n--- Resultado de la configuración ---")
    if errores:
        print("El router rechazó estos comandos:")
        for linea in errores:
            print(linea)
    else:
        print("Sin errores: el router aceptó todos los comandos.")

    # Guarda la configuración en la NVRAM del router
    conexion.save_config()
    print("\n¡Configuración guardada exitosamente!")

    # Cierra la conexión
    conexion.disconnect()

except Exception as error:
    print(f"Ocurrió un error de conexión: {error}")
