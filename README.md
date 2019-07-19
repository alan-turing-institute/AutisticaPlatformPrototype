# Autistica Filemanagement Demo

This application is intended as a very simple demonstration of how user-shared *Experiences* can be shared through a website and deposited into Open Humans.

## Content
- [Autistica Filemanagement Demo](#autistica-filemanagement-demo)
  * [Feature set](#feature-set)
  * [Data Storage](#data-storage)
    + [General Storage](#general-storage)
    + [Public Storage](#public-storage)
  * [Limitations](#limitations)
  * [Documentation on using Open Humans](#documentation-on-using-open-humans)
  * [Local Deployment and Development](#local-deployment-and-development)
  * [Contributing](#contributing)

## Feature set

The initial feature set includes:
- logging in into the application through Open Humans
- writing new experiences
- Consent management
  - whether to allow research use of the experience
  - whether to make this experience publicly available
- Users can toggle the research use and public status of each individual experience at any point.
- Each *Experience* is stored as an individual JSON file in Open Humans, annotated with additional metadata (whether the experience is designated to be made public & whether research use of it is allowed)
  - When toggling the sharing/usage permission status those files will be updated to reflect the change
- Public *Experiences* are additionally stored in this web application's database for easier & faster display
- *Experiences* that are made public enter a moderation queue and need to be approved before joining a public list of experiences.

## Data Storage


### General Storage

All experiences are stored on Open Humans as a simple *JSON* file, at this point just containing the timestamp of posting the experience and the experience text.

```
{
    "text": "add another test",
    "timestamp": "2019-07-18 10:43:56.549079"
}
```

Furthermore the application deposits additional metadata in Open Humans when uploading a file:

```
{
    "id": 1234,
    "basename": "testfile.json",
    "created": "2019-07-18T10:43:59.709964Z",
    "download_url": "https://www.openhumans.org/data-management/datafile-download/XXXXXX/?key=access_key",
    "metadata":
    {
        "tags":
        [
            "viewable",
            "non-research"
        ],
        "uuid": "f1790562-a948-11e9-8161-8c859069dbc5",
        "description": "this is a test file"
    },
    "source": "direct-sharing-267"
}
```

The `uuid` is used to correctly link publicly shared experiences to the files on Open Humans. The `tags` describe whether a file is marked as publicly shared or not and whether research use of the data is permitted.


### Public Storage
When a user flags an experience as publicly availble a copy of it will be deposited in this applications own database. The `Django` model to store those is found in `main/models.py`. In addition to linking it to the user, it also stores the `uuid`, linking it to the deposited data in Open Humans.

## Limitations

In this very simplistic demo app there is no proper handling of ownership of *Experiences* or of moderator roles, e.g. everyone can approve/moderate experiences in the queue.

## Documentation on using Open Humans
Logging into this app and storing data is handled through the Open Humans ecosystem. In order to use this application an associated project on Open Humans must be created. The following links provide further documentation on creating these projects & how to use the API.

- A [general overview on OAuth2-based projects on Open Humans](https://www.openhumans.org/direct-sharing/oauth2-features/).
- [How-to create a new project](https://www.openhumans.org/direct-sharing/oauth2-setup/) on Open Humans.
- This application [uses the `django-open-humans` Python library](https://django-open-humans.readthedocs.io/en/latest/) which provides a *Django* app that includes user management, the full OAuth2 workflow as well as additional functions to interact with the Open Humans API.
- The `django-open-humans` library is [based on a more generic `open-humans-api` Python library](https://open-humans-api.readthedocs.io/en/latest/index.html), which can be used in non-Django based Python applications.

## Local Deployment and Development
This app is written in *Python 3.6+*, uses the *Django 2.x* framework and is designed to be ultimately deployed to *Heroku*. You will need some additional modules and packages to locally experiment with this uploader template or to develop it further. A full step-by-step guide that should work for Mac OS (and with minor differences for Linux) [can be found in the INSTALL.md](https://github.com/gedankenstuecke/autistica-filemanagement-demo/blob/master/INSTALL.md).


## Contributing
We'd love to get your contribution to this project, thanks so much for your interest in this! Please [read our `CONTRIBUTING.md`](https://github.com/gedankenstuecke/autistica-filemanagement-demo/blob/master/CONTRIBUTING.md) to see how you can help and become part of our team! 🎉
