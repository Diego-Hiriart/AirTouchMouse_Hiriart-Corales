# AirTouchMouse_Hiriart-Corales
Código fuente para air mouse de Diego Hiriart y Luis Corales

El código para usar el Arduino con su acelerómetro y sus botones touch como si fuera un mouse inalámbrico está compuesto de:
- Un sketch de Arduino
    - Controla el funcionamiento de herdware del mouse, recibe los inputs (movimientos y botones presionados) del usuario y los envía mediante Bluetooth al computador.
- Un script de Python
    - Este script actua como el driver del mouse, usa la información recibida por Bluetooth para mover el cursor en la pantalla y dar click izquierdo y derecho
