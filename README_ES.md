![BLE Adjustable Base](images/hacs.png)
# Base Ajustable BLE (Mattress Firm 900) para Home Assistant

Un componente personalizado de Home Assistant para integrar la **Base Ajustable Mattress Firm 900** mediante **Bluetooth Low Energy (BLE)**.  
Esta integración permite el control local y la automatización de los ajustes de la cama sin depender de servicios en la nube.

---

## Antecedentes

La aplicación original para iPhone de esta base ajustable fue descontinuada alrededor del año 2020, dejando el hardware completamente funcional pero sin una solución oficial para control inteligente.

En ese momento, observé manualmente la comunicación Bluetooth Low Energy utilizada por la aplicación móvil y posteriormente confirmé que los mismos comandos podían replicarse de forma confiable utilizando una Raspberry Pi con Python y la librería Bleak.

Una vez confirmado que los comandos funcionaban correctamente desde una Raspberry Pi usando Python/Bleak, convertí el proyecto en una integración para Home Assistant, permitiendo que cualquiera pueda instalarla mediante HACS y automatizarla de forma local.

Para mejorar la confiabilidad y el alcance del Bluetooth, también implementé un proxy Bluetooth usando un ESP32 alimentado directamente desde el puerto USB de la base. Este paso es opcional, pero resulta muy útil si Home Assistant no se encuentra dentro del alcance Bluetooth de la cama.

Este proyecto se comunica **únicamente de forma local mediante BLE** y no depende de ninguna API en la nube.

---

## Funcionalidades

- **Configuración mediante interfaz gráfica (Config Flow)**, sin necesidad de YAML
- Descubrimiento Bluetooth filtrado a dispositivos cuyo nombre comience con **`iFlex`**
- Conexión BLE confiable utilizando `bleak-retry-connector`
- Secuencia de **inicialización requerida** ejecutada automáticamente al conectar
- Entidades de tipo botón para:
  - Subir / bajar cabeza
  - Subir / bajar pies
  - Subir / bajar lumbar
  - Posiciones predefinidas (Plano, Gravedad Cero, Lounge, Inclinación, Anti-ronquidos)
  - Controles de masaje
  - Control de luz:
    - **Luz (Cambiar color)**
    - **Apagar luz (Mantener presionado 3 segundos)** — simula el comportamiento del control físico
- **Desconexión automática** para asegurar que el control remoto físico continúe funcionando
- Registro opcional de notificaciones RX para depuración
- Operación completamente local (no requiere Internet)

---

## Requisitos

- Home Assistant con soporte Bluetooth  
  - Se recomienda Home Assistant OS o Supervised
- Base Ajustable Mattress Firm 900 (modelos iFlex con BLE)
- Opcional: ESP32 con ESPHome como proxy Bluetooth

---

## Instalación (HACS)

1. Abrir **HACS**
2. Agregar este repositorio como **Repositorio Personalizado**
   - Categoría: **Integración**
3. Instalar **BLE Adjustable Base**
4. Reiniciar Home Assistant
5. Ir a **Configuración → Dispositivos y Servicios → Añadir Integración**
6. Buscar **BLE Adjustable Bed**

---

## Proxy Bluetooth (Opcional)

Si tu instancia de Home Assistant no se encuentra dentro de un rango Bluetooth confiable de la cama, puedes utilizar un proxy Bluetooth con un ESP32.

En mi configuración, el ESP32 está alimentado directamente desde el puerto USB integrado en la base, lo que proporciona excelente proximidad y estabilidad.

Consulta la documentación oficial de Home Assistant para configurar un proxy Bluetooth con ESPHome:
https://www.home-assistant.io/integrations/bluetooth/#bluetooth-proxies

---

## Notas y Limitaciones

- Esta base ajustable **no expone información de posición o ángulo en tiempo real** mediante BLE.
- Los comandos se envían de forma optimista (sin confirmación), igual que el control remoto físico y la aplicación original.
- Solo puede existir una conexión BLE activa a la vez.  
  Si Home Assistant permanece conectado, el control remoto físico puede dejar de responder.
  - Por esta razón, la integración incluye desconexión automática y un botón manual de **Desconectar**.

---

## Descargo de Responsabilidad

Este proyecto es una integración comunitaria independiente y **no está afiliado con Mattress Firm ni con ningún fabricante**.

Utilízalo bajo tu propia responsabilidad.

---

## Contribuciones

Los reportes de errores, registros y solicitudes de cambio son bienvenidos.  
Si tienes una base ajustable similar que utilice diferentes comandos BLE, no dudes en abrir un issue y compartir los detalles.

📄 English version available: [README.md](README.md)