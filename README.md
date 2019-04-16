# FMDB
IMDB like movie db using flask.

Heroku hosted endpoint: [https://fimdb.herokuapp.com](https://fimdb.herokuapp.com/)

### Features
- Movie listing with Material Design
- Locale based page Translations (not thoroughly tested)
- Search by movie Title, Director, Genres (supports auto-complete)

### Built using
- python3
- flask
- sqlite3


## API

### General Users

- `/listing`
  - Request type: `GET`
  - Accessible to all `signed-in` users
  - Queries Supported
    - `?name=Star` - Search by movie name
    - `?director=steven` - Search by director name
    - `?genre=Thriller` - Search by genre
    - `?p=1` - Page number for pagination
    - `?items=50` - Number of items to return per page

### Admin only

- `/admin`
  - Request type: `GET`
  - Shows listing all movies list for management(edit/delete)

- `/manage/delete/<int:id>`

  - Request type: `DELETE`
  - Delete movie by `id`

- `/manage/add`

  - Request type: `POST`

  - Request body
  
    ```json
    {
        "movie_name": "STR",
        "director": "STR",
        "popularity": "FLOAT",
        "chip_genres": "STR",
        "imdb_score": "FLOAT"
    }
    ```

- `/manage/update`

  - Request type: `POST`

  - Request body

      ```json
      {
          "id": "INT",
          "movie_name": "STR",
          "director": "STR",
          "popularity": "FLOAT",
          "chip_genres": "STR",
          "imdb_score": "FLOAT"
      }
      ```


## Search

Search works by filtering in `/listing` endpoint. 

Search via `GET` request parameters:

- Movie Title
  - `/listing?name=Star`
- Director
  - `/listing?director=steven`
- Genre
  - `/listing?genre=Thriller`

Search supports **autocomplete** as long as user is inside a page *accessible after authentication*. This isn't a bug, it is a feature. Autocomplete can be added to all pages without authentication.

## Scaling

If lets say, some day this application becomes too famous and we get a lot of visitors on a daily basis; here are the following steps I would take to handle the traffic.

### Scaling each service

#### Database

The first step would be switching from `Sqlite` to a higher performance DB. Currently the implementation is using `sqlite` for test purposes.  

One of the possible DB options to switch to would be AWS Aurora

- Reasons for choosing:
  - Fully Managed
  - Auto-scaling
  - Compatible with MySQL applications without any modifications
  - 5x higher throughput compared to standard MySQL db
  - Optional serverless for completely automatic vertical/horizontal scaling

#### Web Server

One of the biggest bottlenecks in performance would be the `web-server` that serves the app. To ensure it can handle the large volume of requests, we need to switch to a faster, asynchronous framework.

Candidates for a faster async web framework include:

- **Sanic**
- **Vibora**

> ##### Vibora seems like the perfect candidate judging the [benchmarks](https://vibora.io/#benchmarks). 

Benchmarks show **Vibora** to be **significantly faster** than Sanic so, I would pick Vibora as a replacement for flask. 

*Why didn't you build it using Vibora in the first place?*

Large part of this project was developed during a 9 hour journey by train. Spotty internet connection and time constrains made me stick to the skills I already knew.

> Currently, the flask app has been deployed using Gunicorn WSGI server with GEVENT workers to support async requests.

*Horizontal scaling* is possible with the current(flask-based) architecture without jumping ship to Sanic or Vibora by using `NGINX` as a load balancer and running multiple Gunicorn servers. 

### Scaling the whole stack

Apart from improving service level performance, another way to handle more load is by scaling out all microservices as and when the load comes in. 

**Kubernetes** can be used to orchestrate **docker** containers for our application to spin up `db` and `web-server` containers depending on the load. 

Using kubernetes helps reduce a lot of the sys-ops overhead as it takes care of the scaling out all `microservices` as well as `load balancing` while ensuring the most optimal use for our infrastructure.
