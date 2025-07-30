# Dispatch Task Project
Create and manage tasks and track progress

**Link to project:** 


**Tech used:**  Python 3.13, Mongodb

Visit http://127.0.0.1:8000/docs for the interactive Swagger UI

## How to run the application:

If you do not have a local mongodb setup, run the following commands.
- Download homebrew if you do not already have it installed
- `brew tap mongodb/brew`
- `brew install mongodb-community`
- `brew services start mongodb-community`

### Running the App
Add the api-key from the env file as Api-Key for the Authorization in Postman
or as
`curl -H "X-Auth-Token: 2d87043c-8d2e-42e2-a77e-eabc12345678" http://localhost:8000/secure`
```bash
uvicorn app.main:app --reload
```

### Query the db
```bash
mongosh
show dbs
use taskdatabase
show tables
db.tasks.find()

```