# Post Scoring Project

```bash
python3 -m venv env
pip install -r requirements.txt
cd post_scoring_project
python3 manage.py migrate
python3 manage.py test
python3 manage.py createsuperuser
python3 manage.py runserver
```

Head over to the `localhost:8000/admin` in order to log in.
After that you'll be able to add posts and scores via:
- `localhost:8000/api/posts`
- `localhost:8000/api/scores`

