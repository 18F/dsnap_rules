# D-SNAP Rules
[![CircleCI](https://circleci.com/gh/18F/dsnap_rules.svg?style=svg)](https://circleci.com/gh/18F/dsnap_rules)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for additional information.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.

## Development

### Installation

Install project dependencies using:
```
pipenv install
```

### Testing

Run tests using:
```
pytest
```

#### Testing the deployed application
The application has been deployed in cloud.gov and is available at https://dsnap-rules.app.cloud.gov.

The `examples` directory has examples for eligible, ineligible and invalid payloads.

Submit examples from the directory `examples`. E.g.,
```
curl -X POST -d @examples/eligible_request.json https://dsnap-rules.app.cloud.gov
```

In addition, there is a quick-and-dirty [form](https://dsnap-rules.app.cloud.gov) that can be used to test the application.

### Running locally
Create a local PostgreSQL database. Set the environment variable DATABASE_URL to point to this database, e.g.:
```
export DATABASE_URL=postgresql:///dsnap
```

Migrate the database, if necessary, using:
```
python manage.py migrate
```

Start the app using:
```
python manage.py runserver
```

This will make the application available at `http://localhost:8000`, by default. To change the port and other settings, see https://docs.djangoproject.com/en/2.1/ref/django-admin/#runserver.
