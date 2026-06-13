import cv2
import numpy as np
import threading
import time
from collections import deque
from typing import List, Tuple
from src.ports.outbound.video_source_port import IVideoSource

class HikvisionRTSPAdapter(IVideoSource):
    def __init__(self, rtsp_url: str, target_size: tuple = (112, 112), fps_muestreo: int = 30):
        self.rtsp_url = rtsp_url
        self.target_size = target_size
        self.batch_size = 16 
        
        source = int(self.rtsp_url) if self.rtsp_url.isdigit() else self.rtsp_url
        self.cap = cv2.VideoCapture(source)
        
        # Reducir buffer interno para IP
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        if not self.cap.isOpened():
            raise ValueError(f"❌ No se pudo conectar al flujo: {self.rtsp_url}")
            
        # NUEVO: Capturar resolución nativa de la cámara
        self.native_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.native_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"📡 Conexión EN VIVO established: {self.rtsp_url} ({self.native_width}x{self.native_height})")

        self.running = True
        self.lock = threading.Lock()
        self.frames_buffer = deque(maxlen=self.batch_size)

        self.thread = threading.Thread(target=self._actualizar_frame, daemon=True)
        self.thread.start()

        print("Cargando buffer de video en vivo...")
        while len(self.frames_buffer) < self.batch_size and self.running:
            time.sleep(0.1)

    def _actualizar_frame(self):
        """El hilo esclavo: lee la cámara a máxima velocidad con protección anti-congelamiento."""
        fallos_consecutivos = 0
        
        while self.running:
            # Si la cámara se desconecta físicamente, read() lanzará False
            ret, frame = self.cap.read()
            
            if ret:
                fallos_consecutivos = 0 # Todo en orden
                with self.lock:
                    self.frames_buffer.append(frame)
            else:
                fallos_consecutivos += 1
                
                # Si falla 5 veces seguidas (aprox 1 segundo), forzamos el reinicio
                if fallos_consecutivos > 5:
                    print(f"⚠️ [Nodo {self.rtsp_url}] Desconectado. Reiniciando socket RTSP...")
                    self.cap.release()
                    time.sleep(1.5) # Le damos tiempo al DVR para reaccionar
                    
                    source = int(self.rtsp_url) if self.rtsp_url.isdigit() else self.rtsp_url
                    self.cap = cv2.VideoCapture(source)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                    fallos_consecutivos = 0

    # NUEVO RETORNO DE 3 ELEMENTOS
    def get_frame_batch(self, batch_size: int) -> Tuple[List[np.ndarray], List[np.ndarray], Tuple[int, int]]:
        with self.lock:
            current_frames = list(self.frames_buffer)

        if len(current_frames) < batch_size:
            return [], [], (0, 0)

        frames_ia = []
        for frame in current_frames:
            # Redimensionar solo para la IA
            frame_resized = cv2.resize(frame, self.target_size)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frames_ia.append(frame_rgb)

        # Retornamos frames originales (HD), frames IA (112x112) y resolución nativa
        return current_frames, frames_ia, (self.native_width, self.native_height)

    def release(self):
        self.running = False
        if hasattr(self, 'thread'): self.thread.join()
        self.cap.release()