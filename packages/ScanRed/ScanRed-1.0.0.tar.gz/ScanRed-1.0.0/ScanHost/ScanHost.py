import os
import platform
import sys
import threading
from datetime import datetime
from time import time

IPHILOS = 1
IPS=[]
IPSPROC=[]
if (platform.system() == "Windows"):
    ping = "ping -n 1"  
else:
    ping = "ping -c 1"


class Hilo (threading.Thread):
    def __init__(self, inicio, fin, red):
        threading.Thread.__init__(self)
        self.inicio = inicio
        self.fin = fin
        self.red = red

    def run(self):                
        for subred in range(abs(self.inicio), abs(self.fin)):
            direccion = self.red+str(subred)            
            response = os.popen(ping+" "+direccion)                        
            resu = response.read() 
            IPSPROC.append(direccion)      
            if (resu.lower().__contains__("ttl")):              
                IPS.append(direccion)
                break        

def ScanHost(terceto1, terceto2, terceto3):
    red = terceto1+"."+terceto2+"."+terceto3+"."
    comienzo = 0
    fin = 254
    tiempoInicio = datetime.now()
    #print("[*] El escaneo se está realizando desde",
    #      red+str(comienzo), "hasta", red+str(fin))
    NumeroIps = fin-comienzo
    numeroHilos = int((NumeroIps/IPHILOS))
    hilos = []
    try:
        for i in range(numeroHilos):
            finAux = comienzo-IPHILOS
            if(finAux > fin):
                finAux = fin
            hilo = Hilo(comienzo, finAux,red)
            hilo.start()
            hilos.append(hilo)
            comienzo = finAux

    except Exception as e:     
        sys.exit(2)

    for hilo in hilos:
        hilo.join()
    tiempoFinal = datetime.now()
    tiempo = tiempoFinal-tiempoInicio    
    return IPS,IPSPROC
