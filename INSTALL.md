# Installation & Local Deployment

- [Installation & Local Deployment](#installation--local-deployment)
    + [*Step 1: Install pipenv and needed packages*](#step-1-install-pipenv-and-needed-packages)
    + [*Step 2: Install Heroku Command Line Interface (CLI)*](#step-2-install-heroku-command-line-interface-cli)
    + [*Step 3: Set-up the local `.env` file*](#step-3-set-up-the-local-env-file)
  * [FAQ](#faq)

To install this demo app follow the steps below

### *Step 1: Install pipenv and needed packages*

This project [uses the recommended `pipenv` workflow for installing dependencies](http://pipenv.readthedocs.io/en/latest/).

If you already have a `Python 3.x` installation on your end do the following to get started with all required Python packages do the following from the main folder of this repository:

```
pip install pipenv # install pipenv
pipenv install --three # install dependencies
pipenv shell #start virtual environment
```

These steps first install `pipenv` on your system, then install all the dependencies that this specific application needs in a virtual environment and then loads this environment. After running it you should now be in a shell that is specifically set up with all the required Python packages. You can exit this shell any time by just writing `exit`.

**You can re-load your environment at any time by `cd`ing into the root folder of this repository and running `pipenv shell`**.

If new packages have been added to this repository any time, you can upgrade all the packages for it by typing `pipenv install` again and it will use the existing `Pipfile` and `Pipfile.lock` to install the appropriate modules.

### *Step 2: Install Heroku Command Line Interface (CLI)*

This application is designed to be deployed on Heroku. To reproduce their production environment locally you should install the Heroku CLI to run this app locally, as it will make sure that the webserver works similarly and that the necessary environment variables are loaded as needed.

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


### *Step 3: Set-up the local `.env` file*
Once this is done you can complete minimal setup by:
* Create an `.env` file from the example: `cp env.sample .env`
* Edit `.env` to set a random string for `SECRET_KEY`
* Set `OPENHUMANS_CLIENT_ID` and `OPENHUMANS_CLIENT_SECRET` using your project
information in Open Humans.
  * Set up an OAuth2 project, if you haven't already!
  * To get project info, click on the project name in https://www.openhumans.org/direct-sharing/projects/manage/
* Set `OPENHUMANS_APP_BASE_URL` to `http://127.0.0.1:5000`
  * Make sure this is an **exact match** to the redirect URL registered in Open Humans
* Make sure to activate your `Python` environment with `pipenv shell`
* Migrate your database using `heroku local:run python manage.py migrate`

Now you can run the webserver of your local heroku environment using `heroku local`.

This should give you a server up and running on `http://127.0.0.1:5000`.

## FAQ

**When I run `heroku local` or use the app it crashes/complains about missing packages.**

It seems that either new packages are required to run the latest version of this repository or that you're not in the `pipenv shell`. To check for both things run:

```
pipenv install
pipenv shell
heroku local
```
The app should start now.

**I get an error about tables/columns not found!**

You probably didn't migrate your database. Run `heroku local:run python manage.py migrate` to add the missing database tables/columns.
