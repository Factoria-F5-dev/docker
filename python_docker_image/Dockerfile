# Step 1: Use an official Python runtime as a parent image
# Esta imagen base contiene una versión mínima de Python (3.10.12) 
FROM python:3.10.12-slim

# Step 2: Set the working directory inside the container
# Esto significa que cualquier comando ejecutado posteriormente se hará desde dentro de este directorio.
WORKDIR /app

# Copia y lo mete en app
COPY requirements.txt .

#Step 4: Install the dependencies
RUN pip install --upgrade pip setuptools # Actualiza Python
RUN pip install -r requirements.txt

# Muéveles todo lo que tengo en ese directorio a app
COPY . .

#Step 5: Define the command to run the application (run the Python script)
CMD ["python", "predict.py"]





