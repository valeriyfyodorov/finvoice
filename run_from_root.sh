#!/usr/bin/env bash
# make sure you are in root folder of the PROJECT

PR_NAME='website'
mv Python.gitignore .gitignore
pip install django
django-admin startproject $PR_NAME .
mkdir requirements/
touch requirements/local.txt requirements/production.txt requirements/test.txt requirements/base.txt
echo "-r base.txt" >> requirements/local.txt
echo "-r base.txt" >> requirements/production.txt
echo "-r base.txt" >> requirements/test.txt
pip install django-environ
mkdir $PR_NAME/settings/
mv $PR_NAME/settings.py $PR_NAME/settings/base.py
touch $PR_NAME/settings/local.py $PR_NAME/settings/production.py $PR_NAME/settings/test.py
echo "from .base import *" >> $PR_NAME/settings/local.py
echo "from .base import *" >> $PR_NAME/settings/production.py
echo "from .base import *" >> $PR_NAME/settings/test.py

echo "DEBUG = env.bool('DJANGO_DEBUG', default=True)" >> $PR_NAME/settings/local.py
touch .env


# from now on follow https://medium.com/@djstein/modern-django-part-1-project-refactor-and-meeting-the-django-settings-api-d2784efb606f
