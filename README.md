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


uvicorn main:app --host 0.0.0.0 --port 8000
ngrok http 8000

{
  "email": "admin@unmsm.edu",
  "password": "1234",
  "full_name": "Administrador",
  "role": "admin"
}

{
  "email": "user@example.com",
  "password": "string",
  "full_name": "string",
  "role": "person"
}

{
  "email": "admin@unmsm.edu.pe",
  "password": "1234",
  "full_name": "Administrador",
  "role": "admin"
}