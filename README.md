# proyecCAM

Sistema Inteligente de Detección de Anomalías en Video para Videovigilancia Urbana utilizando Deep Learning y Arquitectura Hexagonal.

---

## Descripción

**proyecCAM** es una solución basada en Visión por Computadora y Deep Learning diseñada para detectar automáticamente eventos anómalos en secuencias de video provenientes de cámaras de vigilancia.

El sistema clasifica los eventos en tres categorías:

* 🟢 Normal
* 🟠 Pelea / Agresión
* 🔴 Robo / Hurto

La solución utiliza un modelo basado en **R(2+1)D (Residual Spatiotemporal Convolutional Network)** y está desarrollada siguiendo los principios de **Arquitectura Hexagonal (Ports & Adapters)** para facilitar la escalabilidad, mantenibilidad e integración con sistemas reales de videovigilancia.

---

## Estructura del Proyecto

```text
proyecCAM/
│
├── dataset/
│   ├── train/
│   │   ├── 0_Normal/
│   │   ├── 1_Pelea_Agresion/
│   │   └── 2_Robo_Hurto/
│   │
│   └── val/
│       ├── 0_Normal/
│       ├── 1_Pelea_Agresion/
│       └── 2_Robo_Hurto/
│
├── config/
│   └── settings.yaml
│
├── data/
│   ├── input/
│   └── output/
│
├── src/
│   ├── core/
│   │   ├── entities/
│   │   └── use_cases/
│   │
│   ├── ports/
│   │   ├── inbound/
│   │   └── outbound/
│   │
│   └── adapters/
│       ├── inbound/
│       └── outbound/
│           ├── ai_models/
│           ├── video_sources/
│           └── notifiers/
│
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

## Arquitectura del Sistema

El proyecto está basado en el patrón **Hexagonal Architecture (Ports & Adapters)**.

### Core

Contiene la lógica de negocio independiente de tecnologías externas.

* Entidades del dominio.
* Casos de uso.
* Reglas de negocio.

### Ports

Define contratos e interfaces para desacoplar la lógica del sistema.

* Entrada de datos.
* Modelos de IA.
* Sistemas de alerta.
* Fuentes de video.

### Adapters

Implementa las interfaces definidas por los puertos.

* Lectura de video mediante OpenCV.
* Integración con cámaras RTSP.
* Modelos de Deep Learning.
* Registro y notificación de eventos.

---

## Ventajas de la Arquitectura

### Configuración Centralizada

Toda la configuración se encuentra en:

```text
config/settings.yaml
```

Permite modificar:

* FPS de procesamiento.
* Umbrales de detección.
* Uso de GPU.
* Batch Size.
* Configuración de cámaras.

sin alterar el código fuente.

### Independencia del Modelo de IA

El modelo se encuentra encapsulado en:

```text
src/adapters/outbound/ai_models/
```

Esto permite reemplazar o actualizar la arquitectura de detección sin afectar el resto del sistema.

### Integración con Cámaras Reales

Actualmente se soporta:

```text
local_cv2_adapter.py
```

para videos locales.

Y se encuentra preparado para:

```text
hikvision_rtsp_adapter.py
```

mediante transmisión RTSP desde cámaras IP.

---

## Dataset

El conjunto de datos está organizado en tres clases:

| Clase            | Descripción                        |
| ---------------- | ---------------------------------- |
| 0_Normal         | Actividad cotidiana sin incidentes |
| 1_Pelea_Agresion | Eventos de violencia física        |
| 2_Robo_Hurto     | Eventos de robo o hurto            |

Distribución:

* 80% Entrenamiento
* 20% Validación

---

## Tecnologías Utilizadas

* Python 3.10+
* PyTorch
* OpenCV
* NumPy
* Pandas
* YAML
* Deep Learning
* Arquitectura Hexagonal

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/GuerraChipana/proyecCAM.git
cd proyecCAM
```

### 2. Crear entorno virtual

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución

Ejecutar el sistema:

```bash
python main.py
```

---

## Entrenamiento del Modelo

Si deseas entrenar nuevamente el modelo:

```bash
python train.py
```

El modelo generado se almacenará en:

```text
models/
```

> Nota: Los archivos `.pth` no se incluyen en este repositorio debido a las limitaciones de tamaño de GitHub.

---

## Objetivo de Investigación

Desarrollar un sistema inteligente capaz de detectar automáticamente eventos anómalos en entornos urbanos mediante técnicas de Inteligencia Artificial y Visión por Computadora, contribuyendo al fortalecimiento de la seguridad ciudadana.

---

## Autor

**Anthony Guerra Chipana**

Ingeniería de Sistemas e Informática
Universidad Tecnológica del Perú (UTP) – Ica

---

## Licencia

Este proyecto es desarrollado con fines académicos y de investigación.
