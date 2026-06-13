from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np

class IVideoSource(ABC):
    """
    Puerto de salida: Interfaz para leer flujos de video.
    """
    @abstractmethod
    def get_frame_batch(self, batch_size: int) -> Tuple[List[np.ndarray], List[np.ndarray], Tuple[int, int]]:
        """
        Obtiene un lote de fotogramas.
        
        Returns:
            List[np.ndarray]: Fotogramas originales en alta resolución (BGR).
            List[np.ndarray]: Fotogramas preprocesados para la IA (ej. 112x112 RGB).
            Tuple[int, int]: Resolución nativa del flujo (Ancho, Alto). <-- NUEVO RETORNO
        """
        pass

    @abstractmethod
    def release(self):
        """Libera los recursos de la fuente de video."""
        pass