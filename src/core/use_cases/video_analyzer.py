class AlertManager:
    """
    Núcleo de Reglas de Negocio.
    Actúa como un filtro anti-falsos positivos entre la IA cruda y las alarmas de la policía.
    """

    def __init__(self, umbral_consecutivo: int = 3, enfriamiento_lotes: int = 5):
        self.umbral_consecutivo = umbral_consecutivo
        self.enfriamiento_lotes = enfriamiento_lotes

        self.estado_actual = "NORMAL"
        self.contador_anomalias = 0
        self.contador_enfriamiento = 0

    def evaluar_deteccion(self, es_anomalo: bool) -> str:
        # 1. Si estamos en enfriamiento, ignoramos a la IA temporalmente
        if self.estado_actual == "ENFRIAMIENTO":
            self.contador_enfriamiento -= 1
            if self.contador_enfriamiento <= 0:
                self.estado_actual = "NORMAL"
            return self.estado_actual

        # 2. Lógica de acumulación (El filtro anti-errores)
        if es_anomalo:
            self.contador_anomalias += 1

            # Si acaba de detectarlo, es solo una sospecha
            if self.contador_anomalias < self.umbral_consecutivo:
                self.estado_actual = "SOSPECHA"
            # Si lo mantiene por N lotes seguidos, es un crimen real
            else:
                self.estado_actual = "ALERTA_CRITICA"
                self.contador_anomalias = 0  # Reiniciamos
                self.contador_enfriamiento = (
                    self.enfriamiento_lotes
                )  # Activamos escudo de spam
        else:
            # Si la IA deja de ver el delito antes de llegar al umbral, fue una falsa alarma
            if self.estado_actual == "SOSPECHA":
                self.contador_anomalias = 0
            self.estado_actual = "NORMAL"

        return self.estado_actual
