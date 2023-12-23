# Habr Parser

## Overview

This project is designed to scrape information from a selected site on [habr.com](https://habr.com). It features automated fetching of articles, parsing their content, and storing the information in a PostgreSQL database. The project is encapsulated within Docker containers for easy deployment.

## Project Features

- **Automated Parsing:** The parser runs every 10 minutes, fetching the main page of the chosen hub and extracting links to articles.

- **Duplicate Prevention:** Before saving articles, the parser analyze for duplicates, ensuring each article is unique in the database.

- **Database Storage:** Parsed articles are stored in a PostgreSQL database using two models (`Author` and `Article`) with a relational connection.

- **Django Admin Interface:** The project includes a Django admin interface for easy management and interaction with the collected articles.

## Running the Project

#### Clone the Repository
Clone the repository from GitHub:

```bash
git clone https://github.com/purechromas/habr_project
```

#### Create Environment Variables
Create a `.env` file based on the provided `.env.example` with your configurations.

#### Ensure Docker is Installed
Make sure Docker is installed on your machine.

#### Run the Project by Docker
Open a terminal and run the following command:

```
docker-compose -f docker-compose.yml up
```

## Additional Commands

#### Create Admin User
To work with Django admin and manage articles, create an admin user with the following command:

```
docker-compose -f docker-compose.yml run django poetry run python manage.py createadminuser
```

#### Run Habr Parser Manually
Initiate the Habr parser manually using the command:

```
docker-compose -f docker-compose.yml run django poetry run python manage.py run_habr_parser
```