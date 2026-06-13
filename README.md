# HELLVISION VAD

## Sistema Inteligente de Detección de Anomalías en Video para Videovigilancia Urbana

Sistema basado en Deep Learning y Arquitectura Hexagonal para la detección automática de eventos anómalos en secuencias de video provenientes de cámaras de vigilancia y archivos multimedia.

---

# 📌 Descripción

**HELLVISION VAD (Video Anomaly Detection)** es una solución de Visión por Computadora orientada a la identificación automática de eventos de riesgo en entornos urbanos.

El sistema analiza secuencias de video y clasifica los eventos observados en tres categorías:

* 🟢 Comportamiento Normal
* 🟠 Pelea / Agresión
* 🔴 Robo / Hurto

La plataforma utiliza un modelo de Deep Learning basado en la arquitectura **R(2+1)D (Residual Spatiotemporal Convolutional Network)** optimizada para GPU NVIDIA mediante inferencia acelerada por CUDA.

---

# 🚀 Características Principales

### Dashboard de Monitoreo

* Visualización de video en tiempo real.
* Información operativa en pantalla (OSD).
* Adaptación a diferentes resoluciones de monitor.
* Supervisión centralizada de eventos detectados.

### Procesamiento Multihilo

* Separación entre captura de video e inferencia.
* Uso de colas asíncronas (`deque`) para reducir bloqueos.
* Procesamiento continuo de flujos RTSP.

### Optimización para GPU

* Compatibilidad con CUDA.
* Inferencia FP16.
* Aprovechamiento de Tensor Cores.
* Activación de `cudnn.benchmark`.

### Gestión de Alertas

* Umbrales configurables.
* Validación por eventos consecutivos.
* Tiempo de enfriamiento entre alertas.
* Reducción de falsos positivos mediante reglas de negocio.

### Arquitectura Escalable

* Basada en Hexagonal Architecture (Ports & Adapters).
* Separación entre dominio e infraestructura.
* Facilidad para incorporar nuevas fuentes de video y modelos de IA.

---

# 🏗️ Arquitectura del Proyecto

```text
HELLVISION_VAD/
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
├── train.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 🧠 Dataset

El conjunto de datos está organizado en tres clases:

| Clase            | Descripción                                 |
| ---------------- | ------------------------------------------- |
| 0_Normal         | Actividad cotidiana sin incidentes          |
| 1_Pelea_Agresion | Agresiones físicas o enfrentamientos        |
| 2_Robo_Hurto     | Sustracción de bienes o conductas asociadas |

Distribución recomendada:

* 80% Entrenamiento
* 20% Validación

---

# ⚙️ Requisitos del Sistema

## Hardware Recomendado

* NVIDIA RTX 4050 o superior
* 16 GB RAM
* Procesador Intel Core i5 / Ryzen 5 o superior
* Monitor Full HD (1920×1080)

## Software

* Python 3.10+
* Git
* CUDA Toolkit 11.8+
* Drivers NVIDIA actualizados

---

# 🛠️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/GuerraChipana/proyecCAM.git
cd proyecCAM
```

## 2. Crear entorno virtual

### Windows

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar PyTorch con CUDA

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```text
opencv-python==4.8.1.78
numpy==1.26.4
PyYAML==6.0.1
requests==2.31.0

torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
```

---

# 🧠 Entrenamiento del Modelo

Para entrenar nuevamente la red neuronal:

## 1. Organizar el dataset

```text
dataset/
├── train/
└── val/
```

Cada carpeta debe contener las clases:

```text
0_Normal
1_Pelea_Agresion
2_Robo_Hurto
```

## 2. Ejecutar entrenamiento

```bash
python train.py
```

Al finalizar se generará un archivo de pesos:

```text
mi_modelo_vad.pth
```

Este archivo almacena el conocimiento aprendido por la red neuronal.

> Una vez generado el archivo `.pth`, los videos de entrenamiento ya no son necesarios para ejecutar el sistema, aunque se recomienda conservarlos para futuros reentrenamientos.

---

# 🚦 Configuración de Cámaras

Toda la configuración se encuentra en:

```text
config/settings.yaml
```

Ejemplo:

```yaml
fuentes:
  - id: CAM-INDEPENDENCIA-01
    tipo: rtsp
    url: rtsp://usuario:password@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0
```

---

# ▶️ Ejecución

Iniciar el sistema:

```bash
python main.py
```

Controles:

* ESC → Salir del sistema.
* CTRL + E → Cierre seguro de la aplicación.

---

# 📈 Mejoras Futuras

* Persistencia de eventos mediante SQLite.
* Dashboard Web.
* Notificaciones por Telegram.
* Exportación de reportes PDF.
* Integración con YOLO para análisis contextual.
* Almacenamiento de evidencias visuales.

---

# 

Ingeniería de Sistemas e Informática
Universidad Tecnológica del Perú (UTP) – Ica

Proyecto de Investigación Académica.
