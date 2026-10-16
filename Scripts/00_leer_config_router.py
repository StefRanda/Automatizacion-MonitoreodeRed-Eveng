"""
Lectura del router: muestra 'show ip interface brief' y 'show running-config'.

Pide usuario y contraseña al ejecutar: no hay credenciales escritas en el código.
Uso, con el entorno virtual activo:  python 00_leer_config_router.py

Aviso: el running-config incluye las claves cifradas (hashes) de enable y de los
usuarios. No publiques ni compartas esa salida sin tapar esas líneas.
"""
import getpass
from netmiko import ConnectHandler

print("=== Lectura de la configuración del router ===")
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

    # Comandos de lectura: uno por llamada
    salida = conexion.send_command('show ip interface brief')
    salida2 = conexion.send_command('show running-config')
    print("\n--- Resultado ---")
    print(salida)
    print("\n--- Configuración en ejecución ---")
    print(salida2)

    # Cierra la conexión
    conexion.disconnect()

except Exception as error:
    print(f"Ocurrió un error de conexión: {error}")
