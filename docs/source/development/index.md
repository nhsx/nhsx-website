The `docker-compose.yml` file at the root of the project defines containers for PostgreSQL, Redis, Memcached and the web applications.

To bring up the development environment, you'll first need to ensure all of the required [environment variables](development/environment-variables.md) are exported into your shell session.

From there, you can just `docker-compose up -d`

For development, the docker container will just run a `sleep` command to keep the container running, you can then shell in to the container with `docker exec -it nhsx_web_1 fish` or `docker exec -it nhsx_web_1 zsh` depending on your preferred shell.

Once inside, you can...

* run the application with `runserver` which is an alias to `python manage.py runserver 0.0.0.0:5000`
* Get a python shell with all the application's models pre-imported with `sp` (an alias to `python manage.py shell_plus`)


