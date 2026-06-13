import cv2
import numpy as np
from typing import List, Tuple
from src.ports.outbound.video_source_port import IVideoSource


class LocalVideoAdapter(IVideoSource):
    def __init__(self, video_path: str, target_size: tuple = (112, 112)):
        self.cap = cv2.VideoCapture(video_path)
        self.target_size = target_size

        if not self.cap.isOpened():
            raise ValueError(f"Error al abrir el video: {video_path}")
        print(f"✅ Origen de video local cargado: {video_path}")

    # ACTUALIZAMOS PARA DEVOLVER DOS LISTAS
    def get_frame_batch(
        self, batch_size: int
    ) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        frames_originales = []
        frames_ia = []

        for _ in range(batch_size):
            ret, frame = self.cap.read()
            if not ret:
                break

            # 1. Guardamos el frame original intacto para la interfaz visual
            frames_originales.append(frame)

            # 2. Creamos la versión miniatura y convertimos a RGB para PyTorch
            frame_resized = cv2.resize(frame, self.target_size)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frames_ia.append(frame_rgb)

        return frames_originales, frames_ia

    def release(self):
        self.cap.release()
        print("🔌 Origen de video desconectado.")
