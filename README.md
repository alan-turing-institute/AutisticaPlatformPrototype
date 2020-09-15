# Autistica Platform Prototype

## Development environment

### pipenv

Application dependencies are managed using `pipenv`. So rather than running 
application commands directly, run them using `pipenv <COMMAND>`.

E.g. `python manage.py runserver` is bad (python will complain that dependencies
are not installed). `pipenv run python manage.py runserver` is good
(`pipenv` is aware of the dependencies, so will serve the application correctly).

### Docker

You can develop the application using docker containers, to isolate your development
environment from the rest of your machine.

The following command spins up containers to host the application and database.
This uses the application files on your host machine, rather than baking them into the image.
So if you update files in your IDE, the container will serve the updated file.

From the repo root, run the following command:

```bash
docker-compose -f docker-compose-localdev.yml up
```

This will serve the application at http://localhost:8000/.

Data files for the PostgreSQL database are stored on the host file system in the 
folder `localdev-data`.

To run commands against the container, use `docker exec -it <CONTAINER_ID> <COMMAND>`.
Examples are:

```bash
# install a new dependency
docker exec -it <CONTAINER_ID> pipenv install <DEPENDENCY_NAME>

# make migrations
docker exec -it <CONTAINER_ID> pipenv run python manage.py makemigrations

# run migrations
docker exec -it <CONTAINER_ID> pipenv run python manage.py migrate
```
