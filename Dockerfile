## Stage 1: Base
# Use the official Python image as the base image
FROM python:3.10-slim AS base
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file to the working directory
COPY requirements.txt .
# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt
# Expose the port on which the Flask app will run
EXPOSE 5000


## Stage 2: Development
FROM base AS development
ENV PYTHONNUNBUFFERED=1
# Run Flask with the --debug flag for auto-reloading
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]


## Stage 3: Production
FROM base AS production
# Create non-root user
RUN useradd -m myuser
# Copy code and set ownership to 'myuser'
COPY --chown=myuser:myuser . .
# Switch to the non-root user
USER myuser
# Use a production server like Gunicorn instead of Flask's built-in one.
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]