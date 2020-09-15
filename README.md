# Autistica Platform Prototype

## Development environment

You can develop the application using docker containers, to isolate your development
environment from the rest of your machine.

The following command spins up a docker containers to host the application and database.
This uses the application files on your host machine, rather than baking them into the container.
So if you update files in your IDE, the container will serve the updated file.

From the repo root, run the following commands:

```bash
docker-compose -f docker-compose-localdev.yml up
```

This will serve the application at http://localhost:8000/.

Data files for the PostgreSQL database are stored on the host file system in the folder `localdev-data`

To install a new dependency run the following command:

```bash
docker exec -it <CONTAINER_ID> pipenv install <DEPENDENCY_NAME>
```
