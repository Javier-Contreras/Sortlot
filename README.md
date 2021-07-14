# **Proyecto SORTLOT.**

Aplicación para la resolución del Problema de Ruteo de Vehículos (VRP) mediante Google OR Tools, ofreciendo una interfaz de usuario a través de una Aplicación Web.

## **Dependencias:**

* pip install -U Flask
* python -m pip install --upgrade --user ortools
* python -m pip install requests
* python -m pip install pymongo
* pip install pandas
* pip install numpy
* https://github.com/Project-OSRM/osrm-backend

## **Modo de empleo:**

* python3 app.py
* docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/spain-latest.osm.pbf
* En el navegador: 127.0.0.1:8080

### Menú Principal

En la primera pantalla se pueden ver dos botones:

* El primero resetea la BBDD. (ResetDB)
* El segundo es para el inicio del cálculo de un nuevo envío. (New)

### Selección de destinos

Al pulsar el boton "new", se presenta la pantalla de selección de destinos.

Los destinos están agrupados por provincias, que se eligen mediante un selector. Para cada provincia se presenta una tabla con los concesionarios localizados en esta y un mapa con la localización geográfica de los destinos.

En la tabla presentada, se deberá elegir la demanda de la localización; en caso de tener que recoger un paquete y entregarlo en otro destino, en la columna “deliver to” se deberá poner el índice de la localización destino; el usuario podrá elegir también la ventana de tiempo en la que hay que visitar el concesionario, en caso de tenerla. Es necesario marcar la casilla “use” si se quiere enviar a un destino. La Aplicación ignorará las localizaciones con esta casilla sin marcar. Al marcar un destino, se actualiza el mapa cambiando el marcador correspondiente al concesionario en cuestión, poniendo un marcador azul.

El usuario deberá ingresar un nombre para el envío en el campo de texto correspondiente. Este campo es obligatorio, ya que servirá para identificar unívocamente el envío. Debajo de este, se puede ver un botón donde el usuario podrá subir un archivo con una configuración de parámetros en caso de tenerla y, así, no tener que introducir manualmente los datos. Para una una plantilla de configuración de referencia se puede coger el fichero JSON localizado en “/src/json/destinations.json”.

Para acabar, debajo de este último campo y encima de la tabla, se encuentra el selector de provincia y una barra de búsqueda. Cuando el usuario selecciona una de las provincias se actualizará el mapa y la tabla con los concesionarios de la provincia elegida. Con la barra de búsqueda, el usuario podrá filtrar los concesionarios presentados en la tabla.

Una vez el usuario ha terminado de introducir los datos, deberá pulsar el botón “Confirm” para pasar a la siguiente pantalla.

### Selección de Origen

En esta pantalla el usuario deberá elegir las localizaciones de origen de donde deben partir los vehículos.

La pantalla se compone de una tabla con la localización de origen, junto con un botón que el usuario deberá pulsar para seleccionarla, y un mapa presentado esta localización.

### Selección de Vehículos:

En esta pantalla el usuario deberá seleccionar los vehículos disponibles para el envío. En la imagen se presentan 10 vehículos de ejemplo, con la matrícula y la carga máxima.

### Presentación de Resultados:

En esta quinta y última pantalla se presentan el resultado de la ejecución de Google OR Tools.

Esta pantalla se divide en dos partes bien diferenciadas. La primera es una tabla donde se presenta la información de las rutas de manera detallada. Cada fila corresponde a la ruta de un vehículo, identificado por su matrícula. Para cada destino se puede ver la hora de llegada estimada y la demanda del destino en cuestión. Los últimos elementos de cada fila son el tiempo total de viaje estimado, la distancia total recorrida por el vehículo y la carga con la que tiene que salir de la localización origen.

Debajo de la tabla se pueden observar dos botones. El primero sirve para exportar las rutas a PDF y descargar el archivo. El segundo es para realizar un nuevo envío, al pulsarlo se mostrará de nuevo la pantalla de selección de destinos.

La segunda parte de la pantalla consta de un mapa donde se muestra la representación de las rutas de los vehículos. Se generará un botón para cada uno de los vehículos empleados en el envío. Al pulsar en uno de estos botones, se actualizará el mapa presentando la ruta correspondiente.
