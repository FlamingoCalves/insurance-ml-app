# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the Docker container
WORKDIR /app

# Copy the files from your host to your current location (.)
COPY . /app

# Install the Python dependencies
RUN pip install -r requirements_v1.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]