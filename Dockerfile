# 1. Use the official Python 3.12 slim image
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code
COPY main.py .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
