import time
import yaml
import torch
from src.core.entities.anomaly import Anomaly
from src.adapters.outbound.video_sources.local_cv2_adapter import LocalVideoAdapter
from src.adapters.outbound.video_sources.hikvision_rtsp_adapter import HikvisionRTSPAdapter
from src.adapters.outbound.ai_models.r2plus1d_adapter import R2Plus1DAdapter
from src.adapters.outbound.notifiers.local_logger_adapter import LocalLoggerAdapter
from src.core.use_cases.video_analyzer import AlertManager
from src.adapters.inbound.console_ui import MonitorUI

class NodoCamara:
    """Estructura para encapsular los estados aislados de cada cámara."""
    def __init__(self, id_camara, adaptador_video, gestor_alertas):
        self.id = id_camara
        self.fuente = adaptador_video
        self.gestor = gestor_alertas
        self.lote_numero = 1

def cargar_configuracion(ruta_yaml="config/settings.yaml"):
    with open(ruta_yaml, 'r', encoding='utf-8') as archivo:
        return yaml.safe_load(archivo)

def main():
    config = cargar_configuracion()
    print("Iniciando Centro de Operaciones Multicámara Alta Calidad...")
    
    nodos_activos = []
    
    try:
        # 1. Componentes Compartidos
        motor_ia = R2Plus1DAdapter()
        registrador = LocalLoggerAdapter(output_dir=config['alertas']['directorio_salida'])
        interfaz = MonitorUI(fps_simulacion=config['video']['fps_simulacion'])
        
        tamano_objetivo = tuple(config['video']['target_size'])
        fps = config['video']['fps_simulacion']
        
        # 2. Construcción de Nodos
        for fuente in config['video']['fuentes']:
            print(f"Conectando Nodo: {fuente['id']}...")
            if fuente['tipo'] == "local":
                adaptador = LocalVideoAdapter(fuente['url'], target_size=tamano_objetivo)
            else: 
                adaptador = HikvisionRTSPAdapter(fuente['url'], target_size=tamano_objetivo, fps_muestreo=fps)
                
            gestor_aislado = AlertManager(
                umbral_consecutivo=config['reglas_negocio']['umbral_consecutivo'], 
                enfriamiento_lotes=config['reglas_negocio']['enfriamiento_lotes']
            )
            nodos_activos.append(NodoCamara(fuente['id'], adaptador, gestor_aislado))

        estados_guardar = config['alertas']['estados_guardar']
        batch_size = config['video']['batch_size']
        umbral_ia = config['ia']['umbral_certeza']
        
        print(f"\n--- Monitoreo Activo: {len(nodos_activos)} Cámaras en Operación ---")
        
        # 3. Orquestador Maestro
        while True:
            salir_global = False
            paneles_visuales = [] 
            
            for nodo in nodos_activos:
                inicio_tiempo = time.time()
                
                # A. Extracción Segura de Lotes (Puede devolver 2 o 3 valores)
                resultado_lote = nodo.fuente.get_frame_batch(batch_size=batch_size)
                if len(resultado_lote) == 3:
                    lote_originales, lote_ia, native_res = resultado_lote
                else:
                    lote_originales, lote_ia = resultado_lote
                
                if not lote_originales:
                    continue
                    
                # B. Inferencia
                es_anomalo, certeza, accion = motor_ia.predict(lote_ia)
                latencia_ms = (time.time() - inicio_tiempo) * 1000
                         
                # C. Reglas de Negocio
                if certeza < umbral_ia: 
                    es_anomalo = False
                estado_sistema = nodo.gestor.evaluar_deteccion(es_anomalo)
                
                # D. Registro
                if estado_sistema in estados_guardar:
                    evento = Anomaly(
                        tipo_delito=accion,
                        nivel_certeza=certeza,
                        frame_evidencia=lote_originales[-1] 
                    )
                    evento.estado_alerta = estado_sistema 
                    evento.id_camara = nodo.id 
                    registrador.registrar_alerta(evento)
                
                # E. Generación Visual en Alta Calidad
                panel = interfaz.generar_panel_osd(
                    lote_originales[-1], estado_sistema, accion, certeza, latencia_ms, nodo.lote_numero, nodo.id
                )
                paneles_visuales.append(panel)
                nodo.lote_numero += 1
                
           # F. Renderizamos todo el dashboard junto
            salir = interfaz.renderizar_dashboard(paneles_visuales)
            if salir:
                print("Operador solicitó cierre del sistema.")
                break 
                
            # Limpieza de memoria GPU anti-fugas (Basura residual)
            torch.cuda.empty_cache()
                
    except Exception as e:
        print(f"Error crítico en el orquestador: {e}")
    finally:
        print("\nCerrando conexiones de red y liberando VRAM...")
        for nodo in nodos_activos:
            nodo.fuente.release()
        if 'interfaz' in locals(): interfaz.cerrar() 
        print("Apagado del sistema completado.")

if __name__ == "__main__":
    main()