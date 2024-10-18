# Usa una imagen base de Python
FROM python:3.10.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /code

# Copia el archivo requirements.txt en el contenedor
COPY requirements.txt /code/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación en el contenedor
COPY . /code/

# Comando por defecto para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]