#include <SoftwareSerial.h>   // Se incluye SoftwareSerial para usar el HC-05
#include <Adafruit_MPU6050.h> //Para manejar el MPU6050
#include <Adafruit_Sensor.h>  //Para la libreria de MPU6050, es necesaria para que funcione
#include <Wire.h>//Se necesita para comunicarse con el MPU pues es comunicacion con I2C

SoftwareSerial BTHirCor(10,11); //Declaramos un bluetooth. Definimos los pines RX y TX del Arduino conectados al Bluetooth, estan conectados RX-TX como siempre
Adafruit_MPU6050 MPUHirCor; //Se declara el mpu que se usa

int clickIz = 6;
int clickDer = 7;
String comando;//Para guardar clicks y aceleracion, iz,der,Ax,Ay


void setup() {
  
  BTHirCor.begin(9600);
  //Serial.begin(9600);//Para debug
  pinMode(clickDer, INPUT);
  pinMode(clickIz, INPUT); 
  if(MPUHirCor.begin()){//Si se encuentra se hacen los seteos, sino nada porque daria error 
    MPUHirCor.setAccelerometerRange(MPU6050_RANGE_8_G);//Se pone el rango que devuelve el acelerometro de -9.8*8m/s2 a +9.8*8m/s2
  }else{
    //Serial.write("No se encontro el MPU");//Para debug
  }
}

void loop() {
  delay(10);//Delay para evitar que se llenen buffers y cosas similares, sobre todo para no mandar tantos clics de mouse porque se da doble clic todo
  comando = "";//Resetear el string de envio
  if(MPUHirCor.begin()){//Solo iniciar el loop si se puede conectar al MPU, para evitar errores    
    sensors_event_t aceleracion, g, t;//Se declara un evento del MPU, en este caso aceleraciones. Es un struct de C
    //Se declaran 3 eventos porque la libreria no permite guardar solo 1 en getEvent() mas adelante
    MPUHirCor.getEvent(&aceleracion, &g, &t); ///Se guarda la aceleracion en el evento declarado, solo se usa aceleracion pero sin los otros dos la funcion no sirve, necesita guardar los 3
       
    if(digitalRead(clickIz)==HIGH){//Aniadir un indicador de clic izquierdo activado o no
      comando="1";
    }else{
      comando="0";
    }
    if(digitalRead(clickDer)==HIGH){//Aniadir un indicador de clic derecho activado o no
      comando.concat(",1");
    }else{
      comando.concat(",0");
    }

    //Lectura y aniadido de datos de acelerometro, se les transforma a String
    comando+=","+String(aceleracion.acceleration.x);//Aniadir aceleracion en x (izq a der) a comando
    comando+=","+String(aceleracion.acceleration.y);//Aniadir aceleracion en y (atras a adelante) a comando
  
    comando+="\n";//Aniadir salto de linea al comando para la lectura
  
    //Se envia el comando por bluetooth a la computadora
    BTHirCor.write(comando.c_str());//Se transforma el string comando a un string estilo C para poder enviarlo
    //Serial.write(comando.c_str());//Para debug
  }else{//Debug de MPU no encontrado
    //Serial.write("No se encontro el MPU");//Para debug
  }
  
  
} 
