# FMDB
IMDB like movie db using flask.

#### API

- `/listing`

  - Request type: `GET`
  - Accessible to all `signed-in` users
  - Queries Supported
    - `?name=Star` - Search by movie name
    - `?director=steven` - Search by director name
    - `?genre=Thriller` - Search by genre
    - `?p=1` - Page number for pagination
    - `?items=50` - Number of items to return per page

- `/admin`

  - Request type: `GET`
  - `ADMIN` group users only

- `/manage/delete/<int:id>`

  - Request type: `DELETE`
  - `ADMIN` group users only

- `/manage/add`

  - Request type: `POST`

  - `ADMIN` group users only

  - Request body

    - ```json
      {
        'movie_name': 'STR',
        'director': 'STR',
        'popularity': 'FLOAT',
        'chip_genres': 'STR',
        'imdb_score': 'FLOAT'
      }
      ```

- 

#### Search

Search works by filtering results within the `/listing` endpoint. 

Supported `GET` request parameters:

- Movie Title
  - `/listing?name=Star`
- Director
  - `/listing?director=steven`
- Genre
  - `/listing?genre=Thriller`

Search supports autocomplete when inside a page that requires authentication to access