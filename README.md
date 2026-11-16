# Pokédex: Back-End Starter Projects

Starter code for the **Back-End** module of the Code Platoon curriculum. You build one project, **our own version of the PokeAPI** (Django, Django REST Framework, and PostgreSQL on Docker Compose), a lecture at a time.

Each branch holds the **starter code for one lecture**, which is the finished project from the lecture before it. If you fall behind, or want to compare your work, check out that lecture's branch.

| Branch | Starter for lecture | Project state when you start |
| ------ | ------------------- | ---------------------------- |
| `2.2-fields-methods-fixtures-admin` | Lesson 2, Lecture 2 | Django + PostgreSQL running on Docker Compose |
| `3.1-intro-validators-and-tests` | Lesson 3, Lecture 1 | `Pokemon` model, migrations, admin, fixture |
| `3.2-intro-model-serializers` | Lesson 3, Lecture 2 | Validators, `choices`, and 13 model tests |
| `4.1-intro-to-associations` | Lesson 4, Lecture 1 | `PokemonSerializer` and 27 tests (this lecture uses a separate practice project) |
| `4.2-implementing-relationships` | Lesson 4, Lecture 2 | Same code as `4.1` (lecture 4.1 doesn't change the Pokédex) |
| `5.1-api-views` | Lesson 5, Lecture 1 | `move_app`, `PokemonMove`, nested serializers, 27 tests |
| `5.2-endpoints-and-testing` | Lesson 5, Lecture 2 | `APIView` endpoints, app `urls.py`, 29 tests |
| `6.1-intro-to-crud` | Lesson 6, Lecture 1 | Single-record `GET` endpoints, 37 tests |
| `6.2-create-and-delete` | Lesson 6, Lecture 2 | `PUT` and `PATCH` endpoints, 40 tests |
| `7.1-create-login` | Lesson 7, Lecture 1 | Full CRUD API, 52 tests |
| `7.2-info-logout` | Lesson 7, Lecture 2 | `Trainer` user model, token app, `TrainerSerializer`, 52 tests |
| `main` | Finished project | Auth endpoints and `IsAuthenticatedOrReadOnly`, 66 tests |

Lecture 2.1 has no starter, because you create the project from scratch.

## Running a branch

```bash
git clone https://github.com/Code-Platoon-Assignments/pokedex.git
cd pokedex
git checkout 5.2-endpoints-and-testing   # any branch above
docker compose up -d --build
docker compose exec backend bash
```

Inside the container:

```bash
python manage.py migrate
python manage.py loaddata pokemon_data.json move_data.json pokemon_move_data.json   # from lecture 4.2 on
python manage.py test
```

The API is served at <http://localhost:8000/>. Stop everything with `docker compose down` (add `-v` to also delete the database volume).

> These branches are teaching snapshots. The database password and Django `SECRET_KEY` are development placeholders, so don't deploy this as it is.
