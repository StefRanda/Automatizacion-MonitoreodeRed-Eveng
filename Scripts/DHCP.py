import getpass
from netmiko import ConnectHandler

# Solicitar credenciales de forma segura
usuario_ssh = input("Ingresa el usuario SSH: ")
clave_ssh = getpass.getpass("Ingresa la contraseña SSH: ")
secret_ssh = getpass.getpass("Ingresa la contraseña Enable (Secret): ")

dispositivo = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.10',
    'username': usuario_ssh,
    'password': clave_ssh,
    'secret': secret_ssh
}

try:
    # Inicia la sesión SSH
    conexion = ConnectHandler(**dispositivo)
    conexion.enable()  
    print("¡Conexión exitosa al router!")

    print("\n--- Configuración de DHCP server ---")
    cantidad = int(input("¿Cuántos pools querés configurar? "))
    comandos = ['service dhcp']

    for i in range(cantidad):

        print(f"\n--- Configuración del Pool {i+1} ---")

        excluded = input("Ingresa las direcciones IP excluidas (ej. 192.168.1.10 192.168.1.20): ")
        nombre_pool = input("Ingresa el nombre del pool: ")
        red = input("Ingresa la dirección de red (ej. 192.168.1.0): ")
        mascara = input("Ingresa la máscara (ej. 255.255.255.0): ")
        gateway = input("Ingresa la puerta de enlace (ej. 192.168.1.1): ")
        dns = input("Ingresa el DNS (ej. 8.8.8.8): ")

        # Agregar comandos al pool
        comandos.extend([
            f'ip dhcp excluded-address {excluded}',
            f'ip dhcp pool {nombre_pool}',
            f'network {red} {mascara}',
            f'default-router {gateway}',
            f'dns-server {dns}',
            'exit'
        ])

    # Enviar los comandos al dispositivo
    output = conexion.send_config_set(comandos)
    
    # Filtrar solo errores para no imprimir comandos con info sensible
    errores = [linea for linea in output.splitlines() if linea.strip().startswith('%')]
    if errores:
        print("\nAtención: El router rechazó estos comandos:")
        for linea in errores:
            print(linea)
    else:
        print("\n¡Configuración aplicada sin errores!")

    # Guardar la configuración
    conexion.save_config()
    print('¡Configuración guardada exitosamente!\n')
    
    # Mostrar el resultado final de los pools
    print("--- Estado actual de los Pools DHCP ---")
    salida_pool = conexion.send_command('show ip dhcp pool')
    print(salida_pool)

    # Cerrar la conexión
    conexion.disconnect()

except Exception as error:
    print(f"Ocurrió un error de conexión: {error}")