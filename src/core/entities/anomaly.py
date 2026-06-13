from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

@dataclass
class Anomaly:
    """
    Entidad Central del Dominio VAD.
    Representa un evento de violencia o delito validado por el sistema.
    """
    # Atributos Obligatorios
    tipo_delito: str        # Ej. "Robo o Hurto", "Pelea o Agresion"
    nivel_certeza: float    # Nivel de confianza de la IA (Ej. 0.85)
    frame_evidencia: np.ndarray # La fotografía del evento
    
    # Atributos Generados Automáticamente
    fecha_hora: str = field(init=False)
    estado_alerta: str = "ALERTA_CRITICA"
    id_camara: str = "CAM-01" 

    def __post_init__(self):
        """Se ejecuta automáticamente al instanciar la clase para sellar la hora exacta."""
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def obtener_resumen(self) -> str:
        """Devuelve un texto formateado útil para logs o SMS."""
        return (f"[{self.fecha_hora}] {self.estado_alerta} en {self.id_camara}: "
                f"{self.tipo_delito} detectado con {self.nivel_certeza*100:.1f}% de certeza.")