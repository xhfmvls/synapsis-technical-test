# cryptographics-implementation

## Overview

This folder contains the solution for the **Cryptographics Implementation** Challenge.<br>
For this challenge, I created a REST API that supports user registration and authentication.<br>
Below is a brief explanation of the code, the explanation of the approach used to solve the challenge, documentation on how to build/run the code, and several notes regarding the solution.

## Code

### Techstack
- Node.js (with TypeScript)
- Express.js
- Prisma ORM
- MySQL
- Postman (for API Testing)

### Endpoints
1. POST/ login (user authentication)<br>
This endpoint allows users to authenticate by providing a valid username and password
- Request Body:
```
username (string, required)
password (string, required)
```
- Expected Response:
```
(200) Returns a success message along with a JSON Web Token (JWT) for authentication.
(400) Data can’t be stored into the database (doesn’t met the criteria) or authentication failure.
(500) Issue on generating the token.
```
- Flow:
```
'1. Validates that both username and password are provided.
'2. Search for the user data by the provided username.
'3. Verifies the inputed password by comparing it with the stored password hash.
'4. Generates a JWT token (authentication token) if the given credentials are correct.
'5. If the credentials are valid, return a success message along with the JWT token. if not, return a failure message.
```

2. POST/ register (user registration)<br>
This endpoint allows new users to register by providing a username and password.
- Request Body:
```
username (string, required)
password (string, required)
```
- Expected Response:
```
(200) Returns a success message when the user is successfully registered.
(400) Returns an error if the username is already taken, or if the username/password don't meet the validation criteria.
```
- Flow:
```
'1. Validates that both username and password are provided.
'2. Checks if the username length is between 1 and 15 characters.
'3. Checks if the password is at least 8 characters long, and consist of combination of letter, number, and symbol (using regex).
'4. Generate a salt with 10 rounds of processing.
'5. Hashes the password with the generated salt using bcrypt and stores the user in the database.
'6. If the username is already in use (or the credentials given is invalid), returns an error. Otherwise, the user is registered successfully and it would return a success message.
```
<br>

## Approach
### Problem 1
Required to create a program that mimics a user registration and authentication application.<br>
- Solution: <br>
Create a REST API application with **Express** Framework (using **TypeScript**) that have **register** endpoint for the user registration purposes and **login** endpoint for the user authentication. The framework used can return a message (success or fail) in form of API response. <br><br>
### Problem 2
Required to store and restore the user credentials data into/from the database. <br>
- Solution: <br>
Create a **MySQL** database with user table that consist of **username** and **password_hash** field. Use ""Prisma"" ORM to enable the API to interact with the database securily. <br><br>
### Problem 3
Required to use a salted hash to store the password into the database. <br>
- Solution: <br>
Use **bcrypt** hashing algorithm, which has built-in support for generating salts as part of its process.<br><br>

## Setup (Documentation)

### 1. Set an `.env` file with credentials
```sh
DATABASE_URL="mysql://[username]:[password]@localhost:3306/[db_name]?schema=public"

PORT=8000

JWT_SECRET="[jwt_secret]"
```

### 2. Setting up the project and database
```sh
npm install

npx prisma generate

npx prisma migrate dev
```

### 3. Build the application
```sh
npm run build
```

### 4. Run the application
```sh
npm start
```

### 5. Request Testing
```
Import to Postman: **Synapsis.postman_collection.json**
```