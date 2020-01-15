import socket
import io
import tkinter as tk
import struct
import PIL.Image
import matplotlib.pyplot as pl
from tkinter import ttk
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import glob

class class1(tk.Tk):

    def __init__(self):
        super().__init__()
        # Init GUI
        self.title("Camera Server")
        self.geometry('280x60+250+250')
        global entr
        entr = tk.Entry(self)
        entr.grid(row=1, column=0)
        start_button = ttk.Button(self, text='Start server', width=20, command=self.start_server)
        start_button.grid(row=2, column=0, columnspan=1)    # Start server
        send_button = ttk.Button(self, text='Send pictures', command=self.send_pictures)
        send_button.grid(row=1, column=1, columnspan=1)    # Send pictures
        exit_button = ttk.Button(self, text='Exit', width=11, command=exit)
        exit_button.grid(row=2, column=1, columnspan=1)    # Exit program 

    # Starting server
    def start_server(self):
        server.daemon = True # Szerver bezárása a főszál (GUI) leállásakor
        server.join()       # szál indítása
        print("Server started...")
        start_button = ttk.Button(self, text='Stop server', width=20, command=self.stop_server)
        start_button.grid(row=2, column=0, columnspan=1)

    def stop_server(self):
        server.join()
        print("Server stopped...")
        start_button = ttk.Button(self, text='Start server', width=20, command=self.start_server)
        start_button.grid(row=2, column=0, columnspan=1)    # Start server
    
    def send_pictures(self):
        send_from = 'test@gmail.com'
        password = 'jelszo'
        send_to = entr.get()
        
        path = '../pictures/'
        files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = ', '.join(send_to)  
        msg['Subject'] = 'Pi Projekt teszt'
        text = "Ez egy próba email, amelyet a Pi-hez írt programmal küldünk el."
        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil: 
                ext = f.split('.')[-1:]
                attachedfile = MIMEApplication(fil.read(), _subtype = ext)
                attachedfile.add_header(
                    'content-disposition', 'attachment', filename=basename(f) )
            msg.attach(attachedfile)


        smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
        smtp.starttls()
        smtp.login(send_from,password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()

        print("Pictures sent to:", send_to)

# Creating Server
class Server(Thread):
    def __init__(self):
        self.running = True # initial data value
        super().__init__()
        

    def join(self):
        running = False

    def run(self):
        server_socket = socket.socket()
        server_socket.bind(('10.4.158.162', 8000)) 
        server_socket.listen(1)
        self.running = True
        
        while running:
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
