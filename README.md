# Real Estate

Real Estate is an open-source web application designed to provide a platform for buying, selling, and renting properties. The application allows users to browse available properties, view property details, and contact property owners or agents. The project utilizes Python Django and Django Rest Framework.

## Features

-   Property listing with search and filtering
-   Property detail view with images, description, location, and amenities
-   Property owner/agent contact form
-   User authentication and authorization
-   Property creation, update, and deletion (for authorized users only)
-   Dashboard for authorized users to view their listed properties, pending requests, and edit their profile

## Setup

To run the Real Estate application, you'll need to have the following installed on your machine:

-   Python 3.6 or later
-   pip (to install Python packages)
-   PostgreSQL (v10 or later)

After installing the required dependencies, run the following commands to set up the project:
```python
# Clone the repository
git clone https://github.com/skynette/real-estate.git

# Navigate to the project directory
cd real-estate

# Install the required packages
pip install -r requirements.txt

# Create a PostgreSQL database and update the settings in settings.py
# ...

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver

```
You should now be able to access the application at `http://localhost:8000`.


# Contributing to Real Estate

Thank you for your interest in contributing to the Real Estate project! We welcome all contributions, whether it's bug reports, feature requests, or code contributions.

## Getting Started

To get started with contributing to the project, please follow these steps:

1.  Fork the repository on GitHub
2.  Clone the forked repository to your local machine
3.  Install the required dependencies by running `pip install -r requirements.txt`
4.  Create a new branch for your changes (`git checkout -b my-new-feature`)
5.  Make your changes, commit them, and push to your forked repository
6.  Open a pull request to the main repository

Please make sure to include a detailed description of your changes in your pull request, including any relevant background information and screenshots (if applicable).

## Code Style

We follow the PEP 8 style guide for Python code, and the Django code style for Django code. Please make sure to follow these style guides when contributing to the project.

## Testing

We use the Django test framework to test our code. Please make sure to write tests for your changes and ensure that all existing tests pass before submitting a pull request.

To run the tests, use the following command:

    python manage.py test

## Issues

If you encounter a bug or have a feature request, please open an issue on the GitHub repository. Please make sure to include as much detail as possible, including steps to reproduce the issue (if applicable) and any relevant error messages.

## License

By contributing to the Real Estate project, you agree to license your contributions under the project's [MIT License](https://github.com/skynette/real-estate/blob/main/LICENSE).
