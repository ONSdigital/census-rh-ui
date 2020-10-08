[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f86365f13b044491b9047a549589109f)](https://www.codacy.com/app/philwhiles/census-rh-ui?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/census-rh-ui&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/ONSdigital/census-rh-ui.svg?branch=master)](https://travis-ci.org/ONSdigital/census-rh-ui)
[![codecov](https://codecov.io/gh/ONSdigital/census-rh-ui/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/census-rh-ui)

# Respondent Home Python Web Application
Respondent Home is part of ONS's Census Survey Data Collection platform. It allows users to validate their Internet Access Code (IAC) and forwards
them to the [ONS eQ Survey Runner](https://github.com/ONSdigital/eq-survey-runner) upon successful validation.


![The ONS Survey Data Collection platform](/images/sdc_platform.png?raw=true)

This repository contains the Python [AIOHTTP](http://docs.aiohttp.org/en/stable/) application that is the user interface for the Respondent Home product.

## Payload

The fields required to launch an eQ survey are documented in the [ons-schema-definitions](http://ons-schema-definitions.readthedocs.io/en/latest/respondent_management_to_electronic_questionnaire.html#required-fields).


## Installation
Install the required Python packages for running and testing Respondent Home within a virtual environment:

  `make install`

Requires a version of Python 3.8 to be available.

## Running
First, run scripts/load_templates.sh to pull the current/correct version of the ONS Design Patterns.

Then to run this application in development use:

  `make run`

and access using [http://localhost:9092](http://localhost:9092).

## Tests
To run the unit tests for Respondent Home:

  `make test`
  
To run the unit tests and generate a coverage report for Respondent Home:

  `make coverage`

To bring up all the RAS/RM & eQ Runner services and run the integration tests against them and Respondent Home:

  `make local_test`

NB: Waiting for the services to be ready will likely take up to ten minutes.


## Docker
Respondent Home is one part of the RAS/RM docker containers:

  [https://github.com/ONSdigital/ras-rm-docker-dev](https://github.com/ONSdigital/ras-rm-docker-dev)


## Environment Variables
The environment variables below must be provided:

```
JSON_SECRET_KEYS
SECRET_KEY
```

## Translations
The site uses babel for translations.

Text to translate is marked up in html and py templates and files, then a messages.pot is build via pybabel, which collates all the text to translate into a single file.

To build/re-build the translation messages.pot use:

```
pipenv run pybabel extract -F babel.cfg -o app/translations/messages.pot .
```
    
To create a new language messages file, run the following, changing the 2 character language code at the end to the required language code. Only generate a individual language file once.

Note that this implementation includes an English translation. This is needed due to an issue with implementing pybabel with aiohttp.

```
pipenv run pybabel init -i app/translations/messages.pot -d app/translations -l cy
```

Once created, you can update the existing language messages.po files to include changes in the messages.pot by running the following. This will update ALL language files.

```
pipenv run pybabel update -i app/translations/messages.pot -d app/translations
```
    
To compile updates to the messages.po files into messages.mo (the file actually used by the site) use:

```
pipenv run pybabel compile -d app/translations
```
