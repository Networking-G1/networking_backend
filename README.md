- api
    * auth.py
    * groups.py
    * jobs.py
    * users.py
- core
    * config.py
    * security.py
    * utils.py
- models
    * jobs.py
    * user.py
- services
    * matching.py
    * notifications.py
    * validator.py
- tests
app.py


uvicorn main:app --reload --port 8000