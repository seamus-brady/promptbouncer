FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/promptbouncer /app/src/promptbouncer
COPY server /app/server
COPY bin/promptbouncer-fastapi /app/bin/promptbouncer-fastapi

# Give execution permissions to the script
RUN chmod +x /app/bin/promptbouncer-fastapi

# Expose port
EXPOSE 10001

# Set the script as the entry point
ENTRYPOINT ["/app/bin/promptbouncer-fastapi"]
