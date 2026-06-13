import os
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models.video as video_models
from torch.utils.data import Dataset, DataLoader
import numpy as np

class VideoDataset(Dataset):
    def __init__(self, root_dir, num_frames=16, size=(112, 112), is_train=False):
        self.root_dir = root_dir
        self.num_frames = num_frames
        self.size = size
        self.is_train = is_train  # Bandera para aplicar trucos visuales (Data Augmentation)
        
        # 🚨 Carpetas exactas (Asegúrate de que se llamen así en tu disco duro)
        self.classes = ["0_Normal", "1_Pelea_Agresion", "2_Robo_Hurto"]
        
        self.video_paths = []
        self.labels = []

        for label, class_name in enumerate(self.classes):
            class_dir = os.path.join(root_dir, class_name)
            if not os.path.exists(class_dir):
                print(f"⚠️ Advertencia: No se encontró la carpeta {class_dir}")
                continue
                
            for file in os.listdir(class_dir):
                if file.endswith(".mp4"):
                    self.video_paths.append(os.path.join(class_dir, file))
                    self.labels.append(label)

    def __len__(self):
        return len(self.video_paths)

    def __getitem__(self, idx):
        path = self.video_paths[idx]
        label = self.labels[idx]
        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames > self.num_frames:
            indices = np.linspace(0, total_frames - 1, self.num_frames, dtype=int)
        else:
            indices = np.arange(self.num_frames) % total_frames

        # Data Augmentation
        aplicar_espejo = self.is_train and (np.random.rand() > 0.5)
        cambio_brillo = self.is_train and (np.random.rand() > 0.5)
        factor_brillo = np.random.uniform(0.7, 1.3) 

        frames = []
        for i in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                frame = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
            else:
                frame = cv2.resize(frame, self.size)

                if aplicar_espejo:
                    frame = cv2.flip(frame, 1)

                if cambio_brillo:
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    hsv = np.array(hsv, dtype=np.float64)
                    hsv[:, :, 2] = hsv[:, :, 2] * factor_brillo
                    hsv[:, :, 2][hsv[:, :, 2] > 255] = 255
                    hsv = np.array(hsv, dtype=np.uint8)
                    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frames.append(frame)
        cap.release()

        video_np = np.stack(frames)
        video_tensor = torch.from_numpy(video_np).float().permute(3, 0, 1, 2) / 255.0

        return video_tensor, torch.tensor(label, dtype=torch.long)


def entrenar():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Iniciando entrenamiento MULTICLASE en: {device}")

    dataset_train = VideoDataset("dataset/train", is_train=True)
    dataset_val = VideoDataset("dataset/val", is_train=False) 
    
    # Lote de 4 para mantener el consumo de VRAM estable
    train_loader = DataLoader(dataset_train, batch_size=4, shuffle=True)
    val_loader = DataLoader(dataset_val, batch_size=4, shuffle=False)

    weights = video_models.R2Plus1D_18_Weights.DEFAULT
    model = video_models.r2plus1d_18(weights=weights)

    # Congelamos el cerebro base
    for param in model.parameters():
        param.requires_grad = False

    # 🚨 Ajuste automático de la última capa basado en el número de carpetas
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(dataset_train.classes)) 
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

    epochs = 15
    best_acc = 0.0

    for epoch in range(epochs):
        print(f"\n--- Época {epoch + 1}/{epochs} ---")

        model.train()
        train_loss, train_correct = 0.0, 0
        for videos, labels in train_loader:
            videos, labels = videos.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(videos)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * videos.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data)

        model.eval()
        val_loss, val_correct = 0.0, 0
        with torch.no_grad():
            for videos, labels in val_loader:
                videos, labels = videos.to(device), labels.to(device)
                outputs = model(videos)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * videos.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data)

        t_loss = train_loss / len(dataset_train)
        t_acc = train_correct.double() / len(dataset_train)
        v_loss = val_loss / len(dataset_val)
        v_acc = val_correct.double() / len(dataset_val)

        print(f"🎓 Entrenamiento -> Pérdida: {t_loss:.4f} | Precisión: {t_acc * 100:.2f}%")
        print(f"📊 Validación    -> Pérdida: {v_loss:.4f} | Precisión: {v_acc * 100:.2f}%")

        if v_acc > best_acc:
            best_acc = v_acc
            torch.save(model.state_dict(), "mi_modelo_vad.pth")
            print("💾 ¡Nuevo récord! Modelo guardado.")


if __name__ == "__main__":
    entrenar()