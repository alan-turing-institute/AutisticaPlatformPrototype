# Autistica Platform Prototype

## Development environment

### pipenv

Application dependencies are managed using `pipenv`. So rather than running 
application commands directly, run them using `pipenv <COMMAND>`.

E.g. `python manage.py runserver` is bad (python will complain that dependencies
are not installed). `pipenv run python manage.py runserver` is good
(`pipenv` is aware of the dependencies, and will serve the application correctly).

### Docker

You can develop the application using docker containers, to isolate your development
environment from the rest of your machine.

If you don't want to use docker, you'll have to set environment variables for the
database in `settings.py`.

The following command spins up containers for the application and database.
This uses the application files on your host machine, rather than baking them into the image.
So if you update files in your IDE on the host machine, the container will serve the updated file.

From the repo root, run the following commands:

```bash
# the following command only needs to be run once, when you clone the git repo
chmod +x install-dependencies.sh

# run this command to spin up the containers
docker-compose up
```

This will serve the application at http://localhost:8000/.

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

These commands will create or update the relevant files on the host file system, so you can use
git as you normally would.