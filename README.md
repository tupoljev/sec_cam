Raspberry Pi Kamera
===================

Leírás
------

Projektünk egy biztonsági kamera beprogramozása, amelyet python3-ban végeztünk el.

### Szükséges eszközök:
* 2 db gép
* 1 db Raspberry Pi (akár Pi 1 is lehet)
* 1 db Raspberry Pi Camera modul
* 1 db ethernet kábel
* 1 db micro SD kártya
* 1 db microUSB kábel

### Működés
A Raspberry Pi-t a micro USB kábellel egy külső áramforráshoz kell csatlakoztatni.
Az ethernet kábel segítségével internetet kell biztosítani a Pi számára, hogy az SSH protokoll segítségével rá lehessen csatlakozni.
Előtte azonban az SSH-t és a kamerát külön engedélyezni kell a Pi-ben. Első használatkor ezért egy monitorra és billentyűre kell kötni a Pi-t, bekapcsolni
és terminál megnyitása után raspi-config parancs után Interface, Camera Enable-t, valamint SSH Enable-t kiválasztani.
Ezután már elég az ethernet kábellel összekötni a Pi-t egy géppel és már működik is az SSH.
Tudni kell a Pi IP címét. (Van lehetőség távoli asztal, azaz RDP csatlakozásra, de ez nem feltétlenül szükséges)

### A szoftver
Python 3-ban írtunk egy szerver és egy kliens .py kiterjesztésű programot.
Szükség volt a matplotlib, valamint a Pillow modulok installálására is.
* Windows: python -m pip install matplotlib (ill. Pillow)
* Linux: sudo apt python3 -m pip install matplotlib (ill. Pillow)

Először a server.py fájlt kell elindítani azon a gépen, amelyen az élő képet szeretnénk megtekinteni. (python3 camserver.py)
Ez a szerver létrehoz egy socket-et (IP cím + port), amelyen keresztül a kliens a későbbiekben csatlakozni tud.
A kliens maga a Pi lesz ebben az esetben, az küldi a szerver számára az élő képet. (python3 camclient.py)
