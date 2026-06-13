vad_project/
│
├── dataset/                    # CARPETA PRINCIPAL
│   │
│   ├── train/                  # 📚 El material de estudio (80% de los datos)
│   │   ├── 0_Normal/          
│   │   └── 1_Pelea_Agresion/
        └── 2_Robo_Hurto/           
│   │
│   └── val/                    # 📝 El examen sorpresa (20% de los datos)
│   │   ├── 0_Normal/          
│       └── 1_Pelea_Agresion/
│       └── 2_Robo_Hurto/    
│
├── config/                     # Configuraciones globales y variables de entorno
│   └── settings.yaml           # Aquí definiremos límites de RAM, uso de RTX 4050, FPS, etc.
│
├── data/                       # Almacenamiento de archivos locales
│   ├── input/                  # Videos de prueba locales (.mp4)
│   └── output/                 # Alertas generadas, logs o frames guardados
│
├── src/                        # CÓDIGO FUENTE PRINCIPAL
│   │
│   ├── core/                   # 🧠 EL NÚCLEO (Dominio y Casos de Uso)
│   │   ├── entities/           # Objetos básicos (ej: EventoAnomalo, Frame)
│   │   │   └── anomaly.py
│   │   └── use_cases/          # Lógica de negocio (orquestación)
│   │       └── video_analyzer.py # Coordina la entrada de video y el modelo R(2+1)D
│   │
│   ├── ports/                  # 🔌 LOS CONTRATOS (Interfaces)
│   │   ├── inbound/            # Interfaces para quien llama a tu sistema (ej: UI)
│   │   └── outbound/           # Interfaces que tu sistema necesita (Video y Alertas)
│   │       ├── video_source_port.py
│   │       ├── alert_notifier_port.py
│   │       └── anomaly_model_port.py # Interfaz estricta para tu IA
│   │
│   └── adapters/               # 🛠️ LA INFRAESTRUCTURA (El mundo exterior)
│       ├── inbound/            # Adaptadores que controlan la aplicación
│       │   └── console_ui.py   # Interfaz de consola/ventana para la simulación
│       │
│       └── outbound/           # Implementación real de los puertos
│           ├── ai_models/      # Aquí vivirá PyTorch
│           │   └── r2plus1d_adapter.py
│           ├── video_sources/  # Captura de video
│           │   ├── local_cv2_adapter.py  # Para leer los .mp4 de prueba
│           │   └── hikvision_rtsp_adapter.py # Listo para cuando uses las cámaras reales
│           └── notifiers/      # Salida de resultados
│               └── local_logger_adapter.py
│
├── tests/                      # Pruebas unitarias para validar tu código
│   ├── test_video_reader.py
│   └── test_use_cases.py
│
├── main.py                     # 🚀 PUNTO DE ENTRADA
├── requirements.txt            # Dependencias del proyecto (librerías)
└── README.md                   # Documentación de tu tesis para reproducir el entorno

¿Por qué esta estructura es a prueba de balas?
Gestión de Hardware Centralizada (config/settings.yaml): Al separar la configuración, podrás ajustar el batch size (lote de fotogramas) o limitar el uso de VRAM de la RTX 4050 en un solo archivo de texto, sin tener que buscar números mágicos perdidos en el código.

Aislamiento del Modelo IA (adapters/outbound/ai_models/): Si el día de mañana decides que el modelo preentrenado R(2+1)D necesita un ajuste o encuentras uno mejor, solo modificas el archivo r2plus1d_adapter.py. El resto del sistema (la lectura de video, las alertas, el main.py) ni se enterará del cambio.

Transición Transparente a la Realidad (video_sources/): Actualmente simularás de manera local con local_cv2_adapter.py. Cuando la municipalidad te dé acceso a las cámaras Hikvision, simplemente escribiremos el código en hikvision_rtsp_adapter.py y cambiaremos una sola línea en main.py para inyectar la nueva fuente. La lógica de detección seguirá intacta.
# proyecCAM
