The `docker-compose.yml` file at the root of the project defines containers for PostgreSQL, Redis, Memcached and the web applications.

To bring up the development environment, you'll first need to ensure all of the required [environment variables](environment-variables.md) are exported into your shell session. The easiest way to do this is to copy the `docker-compose.env.example`
file to create a `docker-compose.env` file, and replace the empty variables with your
own.

From there, you can just `docker-compose up -d`

For development, the docker container will just run a `sleep` command to keep the container running, you can then shell in to the container with `docker exec -it nhsx_web_1 fish` or `docker exec -it nhsx_web_1 zsh` depending on your preferred shell.

Once inside, you can...

* run the application with `runserver` which is an alias to `python manage.py runserver 0.0.0.0:5000`
* Get a python shell with all the application's models pre-imported with `sp` (an alias to `python manage.py shell_plus`)
* There's also a handy alias `manpy` which is just short for `python manage.py`


## First Run

You'll have no database tables set up in the DB when you first bring up the containers, so the first thing you'll need to do is run migrations...

```
manpy migrate
```

You also then need a superuser account so that you can log in to the wagtail admin interface.

```
manpy createsuperuser
```

We have overridden the User model to allow login with email / password as usernames are not useful here. The `createsuperuser` command will still ask you for a username here, but you should give it an email address.

We also need to add a sane hostname to our hosts file. Open /etc/hosts and add...

```
0.0.0.0    nhsx.test
```

Finally, open http://nhsx.test:5000 in your browser, or http://nhsx.test:5000/admin to go straight to the Wagtail admin interface.

