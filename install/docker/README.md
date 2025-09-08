# Jukeberry Docker Deployment

This directory contains the necessary files to build and run the Jukeberry application using Docker and Docker Compose. This is the recommended method for running Jukeberry as it provides a clean, isolated, and portable environment.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10.0+)
- Docker Compose (v2.0.0+ - included with recent Docker Desktop installations)

> **Note:** This setup uses the modern `docker compose` command (with a space) which is part of Docker Compose V2. If you're using an older version, please update to Docker Desktop 4.0.0 or later, or install the [Docker Compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository) manually.

## Quickstart

1.  **Prepare Directories:**

    From this directory (`install/docker`), create the `music` and `config` directories. These will be mounted into the container.

    ```bash
    mkdir music
    mkdir config
    ```

2.  **Add Your Music:**

    Place your MP3 files into the `music` directory you just created.

3.  **Build and Run the Container:**

    From this directory, run the following command to build the Docker image and start the Jukeberry service in the background:

    ```bash
    docker compose up --build -d
    ```

4.  **Access Jukeberry:**

    The application will be available at [http://localhost:5000](http://localhost:5000).

## Configuration

-   **Music Library:** The `docker-compose.yml` file is configured to mount the local `./music` directory into the container at `/music`. Simply add your music files to this directory.
-   **Configuration File:** The container will use a configuration file located at `/config/jukeberry.conf` inside the container. The local `./config` directory is mounted to this location. You can create your own `jukeberry.conf` file in the local `config` directory to override the defaults.

## Managing the Service

-   **To stop the service:**
    ```bash
    docker compose down
    ```
-   **To view the logs:**
    ```bash
    docker compose logs -f
    ```
