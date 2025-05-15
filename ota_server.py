import socket
import machine

def start_ota_server(port=8080):
    #erstelle neuen socket und bindet deisen an die adresse (espIP + port)
    s = socket.socket()
    s.bind(('', port))
    s.listen(1)
    print(f"OTA-Server läuft auf Port:{port}")

    while True:
        #warte auf eine verbindung 
        cl, addr = s.accept()
        print("Verbindung von", addr)
        
        #Empfängt den HTTP-Header
        request = b""
        while True:
            data = cl.recv(1024) #liest maximal 1024 byte
            if not data:
                break
            request += data #fügt header und daten zusammen
            if b"\r\n\r\n" in request: #prüft ob header abgeschlossen sind
                break #springt raus wenn Header vollständig

        # Header parsen (Content-Length ermitteln)
        headers = request.decode().split("\r\n") #byte-string in text string und zerteilung des Headers
        content_length = 0
        for line in headers:
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        # Dateiinhalt empfangen
        body_start = request.find(b"\r\n\r\n") + 4
        body = request[body_start:]

        while len(body) < content_length:
            body += cl.recv(1024)

        # Speichern als main.py
        with open("main.py", "wb") as f:
            f.write(body)

        print("main.py wurde erfolgreich gespeichert.")

        # Antwort an Client
        cl.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nUpload OK")
        machine.reset()
        cl.send(b"rebooting...\r\n")
        cl.close()