# IATI Website
[![Build Status](https://travis-ci.org/IATI/IATI-Standard-Website.svg?branch=master)](https://travis-ci.org/IATI/IATI-Standard-Website)

This repository hosts the new IATI website based on Django and Wagtail CMS.  A PostgreSQL database stores the underlaying content and user data.


## Local Development

### Pre-requites

- Docker _(See Docker documentation for installation instructions per OS [https://docs.docker.com/install/](https://docs.docker.com/install/))_
- Docker Compose

**Important:** Ensure that native Postgres and Elasticsearch services are stopped. Docker will attempt to use these ports for its own services.


### Dev setup

Build the project. The following will build linked `web` and `postgres` containers.

```
docker-compose build
```

Start the containers in detached mode. This will run migrations and run the Django server. Using in detached (`-d`) mode means that the containers will continue to run in the background - ommitting the `-d` flag will mean that the containers will run only until the command is exited.

```
docker-compose up -d
```

See the status of your containers by using

```
docker ps
```

You can interact with the `web` container directly (in this example, when running a `manage.py` command), like so:

```
docker-compose exec web python manage.py [command]
```

This can feel verbose, so making an alias could be a good idea.

```
echo 'alias dcrun="docker-compose exec web"' >>~/.bash_profile
dcrun python manage.py [command]

echo 'alias dcmanage="docker-compose exec web python manage.py"' >>~/.bash_profile
dcmanage [command]
```

Other useful commands (use with caution)

```
docker kill $(docker ps -q)  //stop all containers

docker rm $(docker ps -a -q)  //remove all containers

docker rmi $(docker images -q) //remove all images

docker volume ls -qf dangling=true | xargs -r docker volume rm  //remove all volumes

```

Create default pages for each of the main sections (e.g. home, about, events etc) of the website
```
docker-compose exec web python manage.py createdefaultpages
```

Create an initial superuser.

```
docker-compose exec web python manage.py createsuperuser
```

The website is browseable at `http://localhost/`. Make changes locally.

For logging, use:

```
docker-compose logs -f web
```

## Moving from `pyenv` development environment to `docker` development environment

Previous iterations of this project utilised `pyenv` for development. This included using postgres natively, and adding local database credentials to `local.py`. 

* Firstly, remove the `pyenv` directory.

```
rm -r pyenv/
```

* Secondly, remove the `DATABASES` dict from `local.py` entirely. The database config is now handled in `dev.py`, and does not need user customisation.

If you are receiving the following error on `web`:

```
psql: could not connect to server: Connection refused Is the server running on host "" and accepting TCP/IP connections on port 5432?
```

Follow the instructions on [this SO answer](https://stackoverflow.com/a/41161674). Your postgres configuration may need amending to listen for all addresses. Postgres will need restarting, and importantly, **your computer will require a restart** for changes to take place.

## Tests & linters

Tests are run using [pytest](https://pytest.org/) as it [provides a number of benefits](https://pytest-django.readthedocs.io/en/latest/#why-would-i-use-this-instead-of-django-s-manage-py-test-command) over stock Django test approaches.

Please be aware that very rarely tests using the database may return an OperationalError warning that the database cannot be destroyed as it is being accessed by other users. If the tests are otherwise passing it is advised that tests should be run again as this is a rare race condition glitch in pytest-django test teardown. The likelihood of this error occurring increases if subsets of tests that use the test database are run on their own. For example, if `pytest -k test_can_create_about_child_pages` is run.

Configurations for tests and linting can be found in the `iati/` directory.

```
# Run tests from the project root
docker-compose exec web pytest
```

Code linting is performed using [pylint](https://github.com/PyCQA/pylint) (with the [pylint-django](https://github.com/PyCQA/pylint-django) plugin), [flake8](http://flake8.pycqa.org) and [pydocstyle](http://www.pydocstyle.org).
```
docker-compose exec web pylint .
docker-compose exec web flake8
docker-compose exec web pydocstyle 
```

Alternatively, the Makefile can be used:
```
docker-compose exec web make test
docker-compose exec web make lint

# OR

docker-compose exec web make all
```
