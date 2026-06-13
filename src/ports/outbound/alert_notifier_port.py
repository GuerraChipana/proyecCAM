from abc import ABC, abstractmethod
from src.core.entities.anomaly import Anomaly

class IAlertNotifier(ABC):
    """
    Puerto de salida: Interfaz estricta para notificar eventos.
    """
    @abstractmethod
    def registrar_alerta(self, anomalia: Anomaly) -> None:
        """
        Debe registrar el evento basándose en la Entidad Anomaly.
        """
        pass