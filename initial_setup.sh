#!/bin/bash

# Create Virtual Environment for Project
python3 -m venv env

# Activate environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for storing Environment variables. Get default values from .env.examples
cp .env.example .env

# Run migration for models
./manage.py makemigrations
./manage.py migrate

# Run unittests
./manage.py test

# Start service on default port 8000
./manage.py runserver
