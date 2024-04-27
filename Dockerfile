# Start with Ubuntu 18.04
FROM ubuntu:22.04

# Set DEBIAN_FRONTEND to noninteractive to skip interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set the timezone to Eastern Time (US)
ENV TZ=America/New_York

# Set the working directory
WORKDIR /app

# Update the package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y software-properties-common

# Add the deadsnakes PPA to get Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa

# Update the package lists again to include packages from the new PPA
RUN apt-get update

# List available Python packages to check if python3.11 is available
RUN apt-cache search python3.11

# Install Python 3.11 (replace with the correct package name if necessary)
RUN apt-get install -y python3.11 python3-pip

# Copy the requirements.txt file
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip, setuptools, and wheel
RUN python3.11 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN python3.11 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of your application code
COPY . /app

# Copy the run_scripts.sh script and make it executable
COPY run_scripts.sh /app
RUN chmod +x /app/run_scripts.sh

# Expose port 5000
EXPOSE 5000

# Run the script
CMD ["/app/run_scripts.sh"]
