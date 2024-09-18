#Step 1: Use an official Python runtime as a parent image
FROM python:3.10.12-slim

#Step 2: Set the working directory inside the container
WORKDIR /app

COPY requirements.txt .

#Step 4: Install the dependencies
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

RUN pip install --upgrade numpy scikit-learn

COPY . .
#Step 5: Define the command to run the application (run the Python script)
CMD ["python", "predict.py"]
