import io
import socket
import struct
import time
import picamera

# Serverre csatlakozás a megadott porton keresztül (8000)
client_socket = socket.socket()
client_socket.connect(('10.4.158.162', 8000))

# Fájl objektum létrehozása
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.vflip = True
    # Preview létrehozása + 2 mp várakozás
    camera.start_preview()
    time.sleep(2)

    # Kezdési idő feljegyzése + stream készítése (kép adatainak mentése)
    # ideiglenesen
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Kód hosszának streambe írása + flush
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # stream visszatekerése és a kép adatainak küldése
        stream.seek(0)
        connection.write(stream.read())
        # Időzítő (ebben a példában 30 mp után leáll a közvetítés)
        #if time.time() - start > 30:
        #    break
        # stream resetelése a következő fényképhez
        stream.seek(0)
        stream.truncate()
    # "Jelzés" hogy végeztünk
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
