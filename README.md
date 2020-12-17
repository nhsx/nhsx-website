# NHSX Wagtail

A Wagtail implementation of the NHSX website.

## Development

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Getting started

Clone the repository:

```bash
git clone https://github.com/nhsx/nhsx-website.git
```

Run the setup script:

```bash
script/setup
```

This will create a docker-compose.env file, initialize the
containers, run the migrations, and set up a superuser with the
username `admin@example.com` and the password `admin`.

You can then run the site with the following command:

```bash
script/server
```

The site will then be available at "http://localhost:5000".

You may also want to give the site a sensible hostname. Open `/etc/
hosts` and add the following to make the site available at
"http://nhsx.test:5000".

```text
0.0.0.0    nhsx.test
```

### Running the tests

The following script runs the tests:

```bash
script/test
```

For more on the approach to testing, see [docs/testing.md](https://github.com/nhsx/nhsx-website/blob/dev/docs/testing.md)

### Other useful commands

To run the Wagtail console:

```bash
script/console
```

To generate migrations:

```bash
script/manpy makemigrations
```

To run migrations:

```bash
script/manpy migrate
```

You can also run a number of other `manage.py` scripts with
the following command:

```bash
script/manpy COMMAND
```

## License

Released under the MIT license.
