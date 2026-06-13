import torch
import torch.nn as nn
import torchvision.models.video as video_models
import numpy as np
from typing import List, Tuple
from src.ports.outbound.anomaly_model_port import IAnomalyModel

# 🔥 1. ACTIVAR OPTIMIZADOR EXTREMO DE CUDNN
torch.backends.cudnn.benchmark = True

class R2Plus1DAdapter(IAnomalyModel):
    def __init__(self, ruta_pesos="mi_modelo_vad.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.usar_fp16 = torch.cuda.is_available() # Bandera para activar modo Turbo
        
        print(f"🚀 Iniciando motor IA R(2+1)D en: {self.device} (Modo Turbo FP16: {self.usar_fp16})")

        self.model = video_models.r2plus1d_18()
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 3)

        try:
            self.model.load_state_dict(
                torch.load(ruta_pesos, map_location=self.device, weights_only=True)
            )
        except Exception as e:
            print(f"❌ Error al cargar los pesos: {e}")

        self.model.to(self.device)
        self.model.eval()

        # 🔥 2. CONVERTIR EL CEREBRO A 16-BITS PARA USAR TENSOR CORES
        if self.usar_fp16:
            self.model.half()

        self.categorias = ["Comportamiento Normal", "Pelea o Agresion", "Robo o Hurto"]

    def predict(self, frame_batch: List[np.ndarray]) -> Tuple[bool, float, str]:
        if not frame_batch or len(frame_batch) == 0:
            return False, 0.0, "None"

        video_np = np.stack(frame_batch)
        video_tensor = torch.from_numpy(video_np).float().permute(3, 0, 1, 2) / 255.0
        video_tensor = video_tensor.unsqueeze(0).to(self.device)

        # 🔥 3. CONVERTIR EL VIDEO A 16-BITS ANTES DE ENTRAR A LA IA
        if self.usar_fp16:
            video_tensor = video_tensor.half()

        with torch.no_grad():
            outputs = self.model(video_tensor)

        probabilidades = torch.softmax(outputs, dim=1)
        certeza_maxima, indice_clase = torch.max(probabilidades, dim=1)

        certeza = certeza_maxima.item()
        nombre_accion = self.categorias[indice_clase.item()]
        es_anomalo = (indice_clase.item() != 0)

        return es_anomalo, certeza, nombre_accion