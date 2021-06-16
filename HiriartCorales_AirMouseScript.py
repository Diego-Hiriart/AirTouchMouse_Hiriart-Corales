"""
Diego Hiriart, Luis Corales
ISW2401-01 COmputación ubicua
2021-Junio-14

@author: DiegoH
@author: LuisC
"""

#Importacion de librerias
from serial import Serial
import numpy as np#Para promedios
import win32api#Librerias para comunicarse con el Windows y poder mover el mouse
import win32con
import sys#Librerias para salir del programa
import signal

def clickIzquierdo():#Presiona y desperesiona el boton de clic izquierdo
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def clickDerecho():#Presiona y desperesiona el boton de clic derecho
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    
def salir(signal, frame):#Se llama esta funcion si en algún momento se presiona el keyboard interrupt
    print("Programa terminado")
    sys.exit(0)


def main():
    print("AirTouch Mouse -  Diego Hiriart & Luis Corales")
    input("Recuerde conectar el mouse mediante Bluetooth a la PC, presione enter una vez que haya hecho esto")
    try:
        BTHiriartCorales = Serial(port = 'COM18', baudrate = 9600, timeout = None)
        calibraciones = 0
        centroX = float(0.0)#Centro o posicion inical de mouse en base a la calibracion
        centroY = float(0.0)
        umbral = 0.5#Rango en el que no se mueve el mouse, si se pasa de esto se mueve
        xs=np.array([])#Arreglos para guardar mediciones
        ys=np.array([])
        
        input("Presione enter para empezar la calibración, mantenga el mouse en su posición de descanso mientras esto se hace")    
        print("Calibrando",end="")#End permite imprimir los puntos que siguen en la misma linea
        #Calibracion
        while(calibraciones<60):
            while(BTHiriartCorales.inWaiting() == 0):
                pass
            data = (BTHiriartCorales.readline().decode('utf-8'))
            comandos = data.split(',')            
            if(len(comandos)==4):#A veces, no lee el string entero, por eso esta revision, sino da error
                xs=np.append(xs, float(comandos[2]))#Aniadir datos al array
                ys=np.append(ys, float(comandos[3]))
                calibraciones+=1
            if(calibraciones%20==0 and calibraciones!=0):#Anadir puntos a Calibrando cada vez que hay un multiplo de 20
                print(".",end="")
        
        #Sacar media de lecturas para obtener los centros, se usa media (no promedio) para saber el dato en el centro de todas las lecturas
        centroX = np.nanmean(xs)#Nanmean ignora algun dato que se haya leido mal
        centroY = np.nanmean(ys)
        
        print("\nMouse Calibrado, puede seguir usando el AirMouse, cuando termine, cierre o presione Ctrl+C")
        
        #MLectura de comando y movimiento del mouse
        while True:
            signal.signal(signal.SIGINT, salir)#Si se presiona el comando para keyboard interrupt, se llama esta funcion
            while(BTHiriartCorales.inWaiting() == 0):
                pass
            data = (BTHiriartCorales.readline().decode('utf-8'))
            comandos = data.split(',')
            if(len(comandos)==4):#se continua solo si se leyo el string completo
                #La multiplicación por -1 es para invertir los ejes, así se mueve bien de izq a der, y apuntar para abajo o arriba baja o sube el mouse
                Ax = float(comandos[2])*-1#Aceleracion en x y y
                Ay = float(comandos[3])*-1        
                clickIzq = int(comandos[0])#Estados del clic, 1 es presionado 0 es no presionado
                clickDer = int(comandos[1])
                
                #Llamar a las funciones de click correspondientes si se presiono uno de los botones
                if(clickIzq==1):
                   clickIzquierdo()
                if(clickDer==1):
                    clickDerecho()
                    
                #Movimiento del mouse
                posActual = win32api.GetCursorPos()#Posicion actual del mouse, se lo pondra en la variable nueva que se modifica despues
                nuevaX = posActual[0]#Es necesario esto porque posActual es una tuple, y no se podra modificar en los ifs
                nuevaY = posActual[1]            
    
                #Si se entra al if, se multiplica por 50% de la misma aceleración, haciendo que mientras mas inclinado 
                #(de 90 grados) mas rapido se mueva, se usa valor absoluto para no daniar la inversion que se hizo antes con *-1
                if(abs(Ax)>(abs(centroX)+umbral)):#Mover en eje x solo si se pasa del umbral con respecto a centroX
                    if(abs(Ax)!=0):#Se hace esto porque, segun la calibracion, puede que cero no este dentro del umbral, y habria un error de division al hacer *0.5
                        nuevaX+=Ax*abs(Ax*0.5)
                    else:
                        nuevaX+=Ax
                if(abs(Ay)>(abs(centroY)+umbral)):#Mover en eje x solo si se pasa del umbral con respecto a centroY                    
                    if(abs(Ax)!=0):
                        nuevaY+=Ay*abs(Ay*0.5)
                    else:
                        nuevaY+=Ay
                
                #Para que el movimiento sea mas suave, mover unidad por unidad, hasta que llegue a la nueva posicion
                diferenciaX=nuevaX-win32api.GetCursorPos()[0]#Obtener la diferencia de posicion para el while
                diferenciaY=nuevaY-win32api.GetCursorPos()[1]  
                while(abs(diferenciaX)>1 or abs(diferenciaY)>1):#Mover hasta llegar a la nueva posicion x y, con una tolerancia de +-1, cero da problemas por la precision
                    #Se define la nueva posicion del mouse
                    #Se deben enviar ints a esta funcion del api, dentro de una tupla como se lo recibe.                                    
                    #Se divide para su mismo abs para mover unidad por unidad, abs para que sea positivo y no se altere la inversion de eje
                    if(abs(diferenciaX)>1):
                        win32api.SetCursorPos((int(win32api.GetCursorPos()[0]+diferenciaX/abs(diferenciaX)), win32api.GetCursorPos()[1]))
                    if(abs(diferenciaY)>1):
                        win32api.SetCursorPos((win32api.GetCursorPos()[0], int(win32api.GetCursorPos()[1]+diferenciaY/abs(diferenciaY))))
                    #win32api.SetCursorPos((int(win32api.GetCursorPos()[0]+diferenciaX/abs(diferenciaX)), int(win32api.GetCursorPos()[1]+diferenciaY/abs(diferenciaY))))     
                    diferenciaX=nuevaX-win32api.GetCursorPos()[0]#Volver a obtener las diferencias para la condicion while
                    diferenciaY=nuevaY-win32api.GetCursorPos()[1]
                
    except Exception as error:
        print("Se desconectó el mouse, reconéctelo y corra el script de nuevo")
        print(error)#Para debug
    finally:
        BTHiriartCorales.close()
        
if __name__=="__main__":#Punto de entrada del programa
    main()#Llamado a funcion main
