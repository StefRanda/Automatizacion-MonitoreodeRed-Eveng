# 🚀 Automatización y Monitoreo de Red Corporativa (Etapa 1)

Este repositorio contiene la primera etapa de mi laboratorio integrador, donde uno los fundamentos de infraestructura de redes (CCNA) con la programabilidad y la observabilidad. El objetivo principal es simular un entorno corporativo, automatizar su despliegue y monitorearlo en tiempo real.

## 🛠️ Tecnologías Utilizadas
* **Simulación de Red:** EVE-NG (Cisco IOL)
* **Programabilidad:** Python 3.11, librería Netmiko
* **Monitoreo:** Zabbix (Desplegado vía Docker sobre Debian Linux)
* **Protocolos Clave:** SSHv2, SNMPv2c, 802.1Q (VLANs)

## ⚙️ Características del Proyecto
* **Infraestructura Capa 2 y 3:** Diseño de una topología jerárquica con enrutamiento Inter-VLAN (Router-on-a-Stick) y segmentación de tráfico en VLANs dedicadas (Producción, Administración y Gestión).
* **Automatización Segura:** Scripts interactivos en Python que solicitan credenciales y parámetros de red en tiempo de ejecución mediante el uso de `getpass` e `input()`. Garantiza que no queden contraseñas expuestas (hardcodeadas) en el código.
* **Monitoreo Centralizado:** Integración de la topología con Zabbix configurando el servicio SNMP y asegurándolo con Listas de Acceso (ACLs). Incluye dashboards dinámicos para la medición del tráfico troncal.

## 📂 Contenido del Repositorio

### 📄 Documentación
* **`Proyecto_Automatizacion_Monitoreo_Etapa1.pdf`**: Documento completo con el diseño detallado de la arquitectura, tablas de direccionamiento, configuraciones manuales iniciales (Día 0) y el *troubleshooting* de los problemas resueltos durante el desarrollo del laboratorio.

### 🐍 Scripts de Automatización
* **`00_leer_config_router.py`**: Comprueba la conexión SSH y extrae de forma segura la configuración actual del equipo de borde (`show ip interface brief` y `show running-config`).
* **`01_config_router.py`**: Automatiza el despliegue de seguridad base (SSH, contraseñas cifradas), configura y levanta las subinterfaces, y habilita el agente SNMP restringido.
* **`02_config_switches.py`**: Utiliza un inventario estructurado (lista de diccionarios) para crear VLANs de forma masiva y asignar los puertos de acceso (`spanning-tree portfast`) en todos los switches de la topología.

## 🚀 Cómo ejecutar este proyecto

1. Clonar el repositorio.
2. Crear y activar un entorno virtual de Python:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
## Instalar las dependencias necesarias:

   pip install netmiko

## Ejecutar el script deseado. Por ejemplo:

python 01_config_router.py

## Nota de seguridad: Los scripts están diseñados para no imprimir las credenciales en pantalla durante la ejecución.
## Solo devolverán por consola los errores o rechazos generados por el sistema operativo IOS (líneas que comiencen con %).

## 🗺️ Próximos pasos

**Cierre de la etapa 1**
- [ ] Restringir las VLANs permitidas en los troncales (`allowed vlan`) y apagar los puertos sin uso.
- [x] Configurar DHCP (Se aplico ROAS, el DHCP server es el mismo router script subido).
- [x] Crear una plantilla personalizada en Zabbix.
- [x] Integrar Zabbix con Grafana para armar dashboards más completos.

**Etapa 2: conexión entre sedes**
- [ ] Sumar las sucursales 2 y 3 al laboratorio.
- [ ] Conectar las sedes por VPN.

**Etapa 3: enlaces redundantes**
- [ ] Agregar EtherChannel entre los switches.

Soy técnica en redes en formación, una apasionada por la infraestructura, la resolución de problemas y el monitoreo. Construí este laboratorio como un entorno de aprendizaje continuo y desafío personal mientras busco mi primera oportunidad laboral en el sector IT.

📫 ¡Conectemos! Podés encontrarme en LinkedIn https://www.linkedin.com/in/stefania-eliana-randazzo/ 
