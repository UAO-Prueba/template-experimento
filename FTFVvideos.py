import cv2
import os

# ==========================
# CONFIGURAR ARCHIVO DE SALIDA
# ==========================
archivo_salida = "mediciones_gravedad.txt"

# Crear archivo con encabezado si no existe
if not os.path.exists(archivo_salida):
    with open(archivo_salida, "w") as f:
        f.write("Video,Altura(m),Delta_frames,Delta_t(s),g(m/s^2)\n")

# ==========================
# BUCLE PRINCIPAL (VARIOS VIDEOS)
# ==========================
while True:

    video_path = input("\nIngrese ruta del video (o 'q' para salir): ")

    if video_path.lower() == 'q':
        break

    altura = float(input("Ingrese la altura en metros: "))

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("No se pudo abrir el video")
        continue

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    current_frame = 0
    mark1 = None
    mark2 = None

    print("Controles:")
    print("d → siguiente frame")
    print("a → frame anterior")
    print("1 → marcar inicio")
    print("2 → marcar final")
    print("g → guardar medición")
    print("r → resetear marcas")
    print("ESC → cerrar video")

    while True:

        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        if not ret:
            break

        delta_frames = None
        delta_t = None
        gravedad = None

        if mark1 is not None and mark2 is not None:
            delta_frames = mark2 - mark1
            delta_t = delta_frames / fps

            if delta_t > 0:
                gravedad = 2 * altura / (delta_t ** 2)

        # Mostrar info
        cv2.putText(frame, f"Video: {os.path.basename(video_path)}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.putText(frame, f"Frame: {current_frame}/{total_frames}", (10, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        if delta_t is not None:
            cv2.putText(frame, f"Delta t: {delta_t:.6f} s", (10, 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        if gravedad is not None:
            cv2.putText(frame, f"g = {gravedad:.4f} m/s^2", (10, 105),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.imshow("Medicion", frame)

        key = cv2.waitKey(0) & 0xFF

        # Navegación
        if key == ord('d'):
            current_frame = min(current_frame + 1, total_frames - 1)

        elif key == ord('a'):
            current_frame = max(current_frame - 1, 0)

        # Marcas
        elif key == ord('1'):
            mark1 = current_frame
            print(f"Marca 1 en frame {mark1}")

        elif key == ord('2'):
            mark2 = current_frame
            print(f"Marca 2 en frame {mark2}")

        # Guardar medición
        elif key == ord('g'):
            if gravedad is not None:
                with open(archivo_salida, "a") as f:
                    f.write(f"{os.path.basename(video_path)},{altura},{delta_frames},{delta_t:.6f},{gravedad:.6f}\n")

                print("Medición guardada ✅")
            else:
                print("Primero debes marcar 1 y 2")

        # Reset
        elif key == ord('r'):
            mark1 = None
            mark2 = None
            print("Marcas reiniciadas")

        # Salir del video actual
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

print("\nProceso finalizado.")
