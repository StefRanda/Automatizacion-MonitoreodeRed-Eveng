🚀 Automatización y Monitoreo de Red Corporativa (Etapa 1)

Este repositorio contiene la primera etapa de mi laboratorio integrador, donde integro los fundamentos de infraestructura de redes (CCNA) con la programabilidad y la observabilidad. El objetivo es simular un entorno corporativo, automatizar su configuración y monitorearlo en tiempo real.

> Es un laboratorio virtual y aislado: no hay equipos físicos ni tráfico de producción. Las IPs y credenciales son de laboratorio.

<img width="1452" height="636" alt="image" src="https://github.com/user-attachments/assets/31665da9-c94b-48c2-bcd1-5d53e91d7238" />
<img width="1258" height="1354" alt="image" src="https://github.com/user-attachments/assets/edc47e43-5cf3-4858-9e23-e417c7bf1cdc" />


## 🛠️ Tecnologías utilizadas

- **Simulación de red:** EVE-NG (Cisco IOL)
- **Programabilidad:** Python 3.11 y la librería Netmiko
- **Monitoreo:** Zabbix (Docker sobre Debian Linux) y Grafana
- **Protocolos clave:** SSHv2, SNMPv2c, 802.1Q (VLANs), DHCP

## ⚙️ Características del proyecto

- **Infraestructura de capa 2 y 3:** topología jerárquica con enrutamiento inter-VLAN (router-on-a-stick) y segmentación en VLANs dedicadas (Producción, Administración y Gestión).
- **Automatización:** scripts interactivos en Python que piden credenciales y parámetros de red al ejecutarse (`getpass` e `input()`), para evitar escribir contraseñas en el código.
- **Monitoreo centralizado:** Zabbix consulta el router y los switches por SNMP, restringido con listas de acceso (ACL). Incluye una plantilla personalizada y dashboards en Grafana para tráfico y carga.

## 📂 Contenido del repositorio

```
.
├── README.md
├── Proyecto_Automatizacion_Monitoreo_Etapa1.pdf
└── scripts/
    ├── 00_leer_config_router.py
    ├── 01_config_router.py
    ├── 02_config_switches.py
    └── DHCP.py
```

### 📄 Documentación

- **`Proyecto_Automatizacion_Monitoreo_Etapa1.pdf`:** diseño de la arquitectura, tablas de direccionamiento, configuración inicial manual (Día 0) y los problemas resueltos durante el desarrollo.

### 🐍 Scripts

| Script | Qué hace |
|---|---|
| `00_leer_config_router.py` | Comprueba la conexión SSH y muestra `show ip interface brief` y `show running-config` del router. |
| `01_config_router.py` | Configuración base y de seguridad (SSH, contraseñas cifradas), subinterfaces con encapsulación 802.1Q y SNMP restringido por ACL. |
| `02_config_switches.py` | Usa un inventario (lista de diccionarios) para crear las VLANs y asignar los puertos de acceso en todos los switches. |
| `DHCP.py` | Crea uno o varios pools DHCP en el router en una sola ejecución: pide la cantidad de pools y, por cada uno, las IPs excluidas, la red, la máscara, el default-router y el DNS. Pide las credenciales al ejecutar y termina mostrando `show ip dhcp pool`. |

### 📡 Monitoreo

- Plantilla personalizada de Zabbix y capturas del dashboard de Grafana, subidas al repositorio.

## 🚀 Cómo ejecutar

1. Clonar el repositorio.
2. Crear y activar un entorno virtual (Windows, PowerShell):

   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea el script de activación, se puede permitir solo para tu usuario:

   ```
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

3. Instalar las dependencias:

   ```
   pip install netmiko
   ```

   > Compatibilidad: el laboratorio usa imágenes Cisco antiguas. En mi entorno fijé la versión 3.3.1 de paramiko (`pip install paramiko==3.3.1`). Si la conexión SSH falla, probá con esa versión.

4. Ejecutar el script que quieras. Por ejemplo:

   ```
   python scripts\01_config_router.py
   ```

   Cada script pide el usuario y la contraseña al ejecutarse.

## 🔒 Nota de seguridad

- Los scripts `01` y `02` no imprimen los comandos enviados ni las credenciales. Solo muestran los errores que devuelve IOS (líneas que empiezan con `%`).
- **Excepción:** `00_leer_config_router.py` muestra el `running-config` completo, que incluye las claves cifradas (hashes). No compartas esa salida sin taparlas.
- Antes de publicar capturas, tapá las IPs de tu red real, tu usuario y el valor de la comunidad SNMP.

## 🗺️ Próximos pasos

**Cierre de la etapa 1**

- [x] Configurar DHCP: el router de borde actúa como servidor (router-on-a-stick), sin necesidad de relay.
- [x] Crear una plantilla personalizada en Zabbix.
- [x] Integrar Zabbix con Grafana para armar dashboards más completos.
- [ ] Restringir las VLANs permitidas en los troncales (`allowed vlan`) y apagar los puertos sin uso.
- [ ] Hacer permanente la ruta de la VM de Zabbix hacia la VLAN de gestión.

**Etapa 2: conexión entre sedes**

- [ ] Sumar las sucursales 2 y 3 al laboratorio.
- [ ] Conectar las sedes por VPN.

**Etapa 3: enlaces redundantes**

- [ ] Agregar EtherChannel entre los switches.

## 👤 Autor

Soy técnica en redes en formación, apasionada por la infraestructura, la resolución de problemas y el monitoreo. Estudié los módulos 1, 2 y 3 de Cisco CCNA y me estoy preparando para certificarme. Construí este laboratorio como un entorno de aprendizaje continuo mientras busco mi primera oportunidad laboral en el sector IT.

📫 ¡Conectemos! Me podés encontrar en [LinkedIn](https://www.linkedin.com/in/stefania-eliana-randazzo/).
