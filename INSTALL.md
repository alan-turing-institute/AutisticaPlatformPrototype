# Local Deployment and Development

This app is designed to be deployable to *heroku* ([see README.md](https://github.com/OpenHumans/oh-app-demo/blob/master/README.md)).

To install it locally to develop [django-open-humans](https://www.github.com/OpenHumans/django-open-humans/)
or this app itself, see the guide below.

### *Step 1: Install pipenv and needed packages*

This project [uses the recommended `pipenv` workflow for installing dependencies](http://pipenv.readthedocs.io/en/latest/).

If you already have a `Python` installation on your end do the following to get started with all required Python packages do the following from the main `oh-app-demo` folder:

```
pip install pipenv
pipenv install --three
pipenv shell
```

You should now be in a shell that is specifically set up with all the required Python packages. You can exit this shell any time by just writing `exit`. If new packages have been added to this repository any time, you can upgrade all the packages for it by typing `pipenv install` again and it will use the existing `Pipfile` and `Pipfile.lock` to install the appropriate modules.

### *Step 2: Install a local copy of django-open-humans*

For local development of [django-open-humans](https://www.github.com/OpenHumans/django-open-humans/),
you should use `pip` to install your local version of that package in editable mode.

While in your virtual environment for `oh-app-demo`:
* Clone a copy of `django-open-humans` if you haven't already!
* Navigate to your `django-open-humans` repository
* Run `pip install -e .`

### *Step 3: Install Heroku Command Line Interface (CLI)*

You should install the Heroku CLI to run this app locally.
Heroku has [installation instructions for MacOS, Windows, and Linux](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

If you are running MacOS the easiest way to do this is using [Homebrew](https://brew.sh/). After installing Homebrew you have two options:

Simply run:
`brew install heroku/brew/heroku`

Or

```
brew tap heroku/brew
brew install heroku
```

The second option shown above adds the Heroku repository to your Homebrew configuration allowing you to access all of the Heroku library rather than the single `heroku` application.


### *Step 4: Set-up the local `.env` file*
Once this is done you can complete minimal setup by:
* Create an `.env` file from the example: `cp .env.sample .env`
* Edit `.env` to set a random string for `SECRET_KEY`
* Set `OPENHUMANS_CLIENT_ID` and `OPENHUMANS_CLIENT_SECRET` using your project
information in Open Humans.
  * Set up an OAuth2 project, if you haven't already!
  * To get project info, click on the project name in https://www.openhumans.org/direct-sharing/projects/manage/
* Set `OPENHUMANS_REDIRECT_URI` to `http://127.0.0.1:5000/complete`
  * Make sure this is an **exact match** to the redirect URL registered in Open Humans
* Make sure to activate your `Python` environment with `pipenv shell`
* Migrate your database using `heroku local:run python manage.py migrate`

Now you can run the webserver of your local heroku environment using `heroku local`.

This should give you a server up and running on `http://0.0.0.0:5000`.

## FAQ

**When I run `heroku local` or use the app it crashes/complains about missing packages.**

It seems that either new packages are required to run the latest version of `oh_app_demo` or that you're not in the `pipenv shell`. To check for both things run:

```
pipenv install
pipenv shell
heroku local
```
The app should start now.

**I get an error about tables/columns not found!**

You probably didn't migrate your database. Run `heroku local:run python manage.py migrate` to add the missing database tables/columns.
