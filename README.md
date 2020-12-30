# django_librest

My first RESTful application made on Django REST Framework for portfolio.

Go to [my site](https://librest.fra1t.me/api/v1/books/) to see API of books for example.

> Don't worry if browser does not allow you to visit this subdomain
> because my security certificate protects only the main domain name.

## All in one

   1. [Install Docker Compose](https://docs.docker.com/compose/install/).
   2. Clone this repository.
   3. Configure [.env](.env) and [uwsgi.ini](config/uwsgi.ini) files as you wish.
   4. Run all containers with `docker-compose up -d`  to launch **django_librest**.
   5. Go to [swagger][1] or [redoc][2] to see all abilities REST API.

## License
[MIT](LICENSE)

[1]:https://librest.fra1t.me/swagger/
[2]:https://librest.fra1t.me/redoc/
