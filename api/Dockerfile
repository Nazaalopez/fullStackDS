# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos y instalar las dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar todos los archivos de código fuente al directorio de trabajo
COPY . /app

# Exponer los puertos para FastAPI y Streamlit
EXPOSE 8000 8501

# Copiar y configurar el script de inicio
COPY run_api.sh /app/
RUN chmod +x /app/run_api.sh

# Establecer el script de shell como el punto de entrada
CMD ["/app/run_api.sh"]
