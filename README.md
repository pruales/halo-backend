# Halo Coding Challenge Python Microservice

React front-end can be found [here](https://github.com/pruales/halo-react). Its deployed through netlify here: https://laughing-hoover-481394.netlify.com/

This is a python microservice for halo's full-stack coding challenge. It uses JWT authenticationa and has a key-value store backed in a sqlite database. 
Its deployed on Digital Ocean and the base url for the api is  `https://17caf9f8.ngrok.io/`. The service is backed by a SQLite database 

**JWT required** endpoints need a bearer token in their header:
```
{
  headers: {
    'Authorization' : Bearer Token
  }
}
 ```
## Authentication
This microservice uses JWT based authentication. For simplicity, the access token expires in 30 days but I've included endpoints for refresh tokens that could be used in a real application.
The password is hashed using `bcrypt`. Users are stored in a users table with their username, hashed password and id. There is also a revoked token table that stores revoked tokens such as when a user logs out.
JWTs are managed by [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/).

#### API
Failed authentication attemps result in 401. Internal errors are 500.
##### POST `/register`
**Body (required)**: 
```
{
  username: String
  password: String
}
```
##### POST `/login`
**Body (required)**: 
```
{
  username: String
  password: String
}
```
**200 Response**:
```
{
  message: String
  access_token: String
}
```
##### POST `/logout/access`
**JWT required**

## Key-Value Store
Collection items are stored with their key, value, user id, and id. Users only have acces to their own items and they have the ability to add items
via the front-end. 

#### API

##### POST `/set`
**JWT required**
**Body (required)**: 
```
{
  key: String
  value: String
}
```

#### GET `/getAll`
**JWT required**

**200 Response**:
```
[
  {
    id: int,
    key: string,
    user_id: int
    value: string
  }...
]
```

