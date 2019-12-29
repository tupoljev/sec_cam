import io
import socket
import struct
import time
import picamera

# Client socket csatlakozása: my_server:8000-ra
client_socket = socket.socket()
client_socket.connect(('192.168.0.158', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.vflip = True
    # preview indítása és 2 mp bemelegítés
    camera.start_preview()
    time.sleep(2)

    # Start ideje + stream létrehozása a képadatok ideiglenes megtartásához
    # (közvetlenül a kapcsolatba is beírhatnánk, de ebben az esetben
    # először minden egyes capture méretét ki kéne találnunk a protocolhoz)
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Capture hossza a streambe és flush
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Stream
        stream.seek(0)
        connection.write(stream.read())
        # Időzítő (adott mp után lépjünk ki
        #if time.time() - start > 30:
        #    break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    # Zero hossza a streambe -> signal -> végeztünk
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
