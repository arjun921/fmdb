# FMDB
IMDB like movie db using flask.

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

    - ```json
    {
      'movie_name': 'STR',
      'director': 'STR',
      'popularity': 'FLOAT',
      'chip_genres': 'STR',
      'imdb_score': 'FLOAT'
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

