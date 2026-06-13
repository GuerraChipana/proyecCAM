from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np

class IAnomalyModel(ABC):
    @abstractmethod
    def predict(self, frame_batch: List[np.ndarray]) -> Tuple[bool, float, str]:
        """
        Retorna:
        - bool: True si es anómalo.
        - float: Nivel de certeza.
        - str: Nombre de la acción detectada por la IA.
        """
        pass