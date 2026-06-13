import os
import cv2

def verificar_dataset(ruta_base="dataset"):
    print(f"🔍 Iniciando auditoría del dataset en: {ruta_base}...\n")
    
    fases = ['train', 'val']
    clases = ['Anomalia', 'Normal']
    
    videos_corruptos = 0
    total_videos = 0
    
    for fase in fases:
        for clase in clases:
            ruta_carpeta = os.path.join(ruta_base, fase, clase)
            
            if not os.path.exists(ruta_carpeta):
                print(f"❌ Error: No se encontró la carpeta {ruta_carpeta}")
                continue
                
            archivos = os.listdir(ruta_carpeta)
            videos = [v for v in archivos if v.endswith('.mp4')]
            
            print(f"📁 {fase}/{clase}: {len(videos)} videos encontrados.")
            
            # Verificación de integridad
            for video in videos:
                total_videos += 1
                ruta_video = os.path.join(ruta_carpeta, video)
                cap = cv2.VideoCapture(ruta_video)
                
                if not cap.isOpened():
                    print(f"   ⚠️ ARCHIVO CORRUPTO: {video}")
                    videos_corruptos += 1
                cap.release()
                
    print("\n" + "="*40)
    print(f"📊 RESUMEN: {total_videos} videos revisados.")
    if videos_corruptos == 0:
        print("✅ ¡Laboratorio de datos en perfecto estado! Listo para entrenar.")
    else:
        print(f"🚨 Se encontraron {videos_corruptos} videos corruptos. Bórralos antes de continuar.")
    print("="*40)

if __name__ == "__main__":
    verificar_dataset()