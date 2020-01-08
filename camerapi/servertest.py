import socket
import io
import tkinter as tk
import struct
import PIL.Image
import matplotlib.pyplot as pl
from tkinter import ttk
from threading import Thread

class class1(tk.Tk):
    def __init__(self):
        super().__init__()
        # Init GUI
        self.title("Camera Server")
        self.geometry('250x30')
        self.set_button = ttk.Button(self, text='Start server', command=self.start_server)
        self.set_button.grid(row=2, column=0, columnspan=1)    # Start server
        self.set_button = ttk.Button(self, text='Exit', command=exit)
        self.set_button.grid(row=2, column=3, columnspan=1)    # Exit program

    # Starting server
    def start_server(self):
        server.daemon = True # Szerver bezárása a főszál (GUI) leállásakor
        server.start()       # szál indítása
        print("Server started...")

# Creating Server
class Server(Thread):
    def __init__(self):
        self.data = {} # initial data value
        super().__init__()

    def run(self):
        server_socket = socket.socket()
        server_socket.bind(('192.168.0.158', 8000)) 
        server_socket.listen(1)

        while True:
            connection = server_socket.accept()[0].makefile('rb')
            try:
                img = None
                while True:
                    # Kép hosszának beolvasása 32-bit unsigned int ként.
                    # Ha ez 0, a program lépjen ki a ciklusból.
                    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break
                    # Stream létrehozása a kép adatainak, ezen keresztül "olvassuk be" a képet
                    image_stream = io.BytesIO()
                    image_stream.write(connection.read(image_len))
                    # Streamelés
                    image_stream.seek(1)
                    image = PIL.Image.open(image_stream)
                    
                    if img is None:
                        img = pl.imshow(image)
                    else:
                        img.set_data(image)

                    pl.pause(0.01)
                    pl.draw()

                    print('Image is %dx%d' % image.size)
                    image.verify()
                    print('Image is verified')
            finally:
                connection.close()
                server_socket.close()

#Init server
server = Server()

# starting the GUI
root = class1()
root.mainloop()
