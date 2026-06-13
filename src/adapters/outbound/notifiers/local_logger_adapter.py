import os
import cv2
from datetime import datetime
from src.ports.outbound.alert_notifier_port import IAlertNotifier
from src.core.entities.anomaly import Anomaly

class LocalLoggerAdapter(IAlertNotifier):
    def __init__(self, output_dir: str = "data/output"):
        self.output_dir = output_dir
        self.log_file = os.path.join(self.output_dir, "registro_eventos.txt")
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Sistema de registro inicializado en: {self.output_dir}")

    def registrar_alerta(self, anomalia: Anomaly) -> None:
        # Generar nombre único para la evidencia
        nombre_archivo = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".jpg"
        ruta_imagen = os.path.join(self.output_dir, nombre_archivo)
        
        # 1. Extraemos la foto de la Entidad y la guardamos tal cual (Ya está en BGR)
        frame_bgr = anomalia.frame_evidencia
        cv2.imwrite(ruta_imagen, frame_bgr)
        
        # 2. Extraemos el resumen de la Entidad y lo escribimos en el Log
        mensaje_log = f"{anomalia.obtener_resumen()} | Evidencia: {nombre_archivo}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as archivo:
            archivo.write(mensaje_log)
            
        print(f"💾 Evidencia guardada exitosamente: {nombre_archivo}")