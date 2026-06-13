import cv2
import numpy as np
import ctypes


class MonitorUI:

    def __init__(self, fps_simulacion: int = 30):

        self.nombre_ventana = "HELLVISION VAD - Centro de Monitoreo"

        user32 = ctypes.windll.user32
        self.screen_w = user32.GetSystemMetrics(0)
        self.screen_h = user32.GetSystemMetrics(1)

        self.osd_height = 130

        self.fullscreen = True
        self.window_created = False

    def _crear_ventana(self):

        cv2.namedWindow(
            self.nombre_ventana,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            self.nombre_ventana,
            self.screen_w,
            self.screen_h
        )

        if self.fullscreen:
            cv2.setWindowProperty(
                self.nombre_ventana,
                cv2.WND_PROP_FULLSCREEN,
                cv2.WINDOW_FULLSCREEN
            )

        self.window_created = True

    def generar_panel_osd(
        self,
        frame,
        estado,
        accion,
        certeza,
        latencia,
        lote_num,
        id_camara
    ) -> np.ndarray:

        if frame is None:
            frame = np.zeros((720, 1280, 3), dtype=np.uint8)

        color_estado = (0, 255, 80)
        icono = "[OK]"

        if estado == "ALERTA":
            color_estado = (0, 0, 255)
            icono = "[!]"
        elif estado == "SOSPECHA":
            color_estado = (0, 220, 255)
            icono = "[?]"
        elif estado == "ENFRIAMIENTO":
            color_estado = (0, 140, 255)
            icono = "[-]"

        altura_video = self.screen_h - self.osd_height

        panel_w = self.screen_w // 2

        frame = cv2.resize(
            frame,
            (panel_w, altura_video)
        )

        panel = np.zeros(
            (
                self.screen_h,
                panel_w,
                3
            ),
            dtype=np.uint8
        )

        panel[:altura_video] = frame

        osd = panel[altura_video:]

        cv2.rectangle(
            osd,
            (0, 0),
            (panel_w, self.osd_height),
            (22, 22, 28),
            -1
        )

        cv2.line(
            osd,
            (0, 0),
            (panel_w, 0),
            (60, 60, 60),
            2
        )

        fuente = cv2.FONT_HERSHEY_SIMPLEX

        # CAMARA
        cv2.putText(
            osd,
            id_camara,
            (20, 35),
            fuente,
            0.8,
            (255, 255, 255),
            2
        )

        # ESTADO
        cv2.putText(
            osd,
            f"{icono} {estado}",
            (20, 75),
            fuente,
            1.0,
            color_estado,
            3
        )

        # IA
        cv2.putText(
            osd,
            accion.upper(),
            (260, 75),
            fuente,
            0.9,
            (0, 255, 120),
            2
        )

        # CERTEZA
        cv2.putText(
            osd,
            f"Certeza: {certeza*100:.1f}%",
            (20, 110),
            fuente,
            0.6,
            (220, 220, 220),
            1
        )

        barra_x = 180
        barra_y = 96
        barra_w = 240
        barra_h = 18

        cv2.rectangle(
            osd,
            (barra_x, barra_y),
            (barra_x + barra_w, barra_y + barra_h),
            (50, 50, 50),
            -1
        )

        progreso = int(barra_w * certeza)

        cv2.rectangle(
            osd,
            (barra_x, barra_y),
            (barra_x + progreso, barra_y + barra_h),
            color_estado,
            -1
        )

        # METRICAS
        cv2.putText(
            osd,
            f"Lote #{lote_num:04d}",
            (470, 35),
            fuente,
            0.55,
            (180, 180, 180),
            1
        )

        cv2.putText(
            osd,
            f"Latencia: {latencia:.1f} ms",
            (470, 75),
            fuente,
            0.55,
            (180, 180, 180),
            1
        )

        cv2.putText(
            osd,
            "ESC = salir | CTRL+E = salir",
            (470, 110),
            fuente,
            0.55,
            (120, 120, 120),
            1
        )

        return panel

    def renderizar_dashboard(self, paneles: list) -> bool:

        if not paneles:
            return False

        if not self.window_created:
            self._crear_ventana()

        cantidad = len(paneles)

        if cantidad == 1:

            dashboard = cv2.resize(
                paneles[0],
                (self.screen_w, self.screen_h)
            )

        elif cantidad == 2:

            dashboard = np.hstack(
                (
                    paneles[0],
                    paneles[1]
                )
            )

        elif cantidad == 4:

            top = np.hstack((paneles[0], paneles[1]))
            bottom = np.hstack((paneles[2], paneles[3]))

            dashboard = np.vstack((top, bottom))

        else:

            dashboard = np.hstack(paneles)

        cv2.imshow(
            self.nombre_ventana,
            dashboard
        )

        key = cv2.waitKey(1) & 0xFF

        # ESC
        if key == 27:
            return True

        # CTRL + E
        if key == 5:
            return True

        return False

    def mostrar_conectando(self):

        pantalla = np.zeros(
            (
                self.screen_h,
                self.screen_w,
                3
            ),
            dtype=np.uint8
        )

        cv2.putText(
            pantalla,
            "HELLVISION VAD",
            (self.screen_w // 2 - 250,
             self.screen_h // 2 - 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            (255, 255, 255),
            3
        )

        cv2.putText(
            pantalla,
            "Conectando camaras RTSP...",
            (self.screen_w // 2 - 260,
             self.screen_h // 2 + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 120),
            2
        )

        cv2.imshow(
            self.nombre_ventana,
            pantalla
        )

        cv2.waitKey(1)

    def cerrar(self):
        cv2.destroyAllWindows()