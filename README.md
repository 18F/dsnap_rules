# Eligibility Rules
[![CircleCI](https://circleci.com/gh/18F/new_rules.svg?style=svg)](https://circleci.com/gh/18F/new_rules)

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

### Running locally
Start the app using:
```
FLASK_APP=new_rules.app python -m flask run
```

The `examples` directory has examples for eligible, ineligible and invalid payloads.
Submit examples from the directory `examples`. E.g.,
```
curl -X POST -d @examples/eligible_request.json http://localhost:5000/
```
This assumes that the application is running on the default port of 5000. To change the port and other settings, see http://flask.pocoo.org/docs/1.0/cli/#run-the-development-server.
