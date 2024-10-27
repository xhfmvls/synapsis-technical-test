# cryptographics-implementation

## Overview

This folder contains the solution for the **Cryptographics Implementation**.<br>
For this challenge, I created a REST API that supports user registration and authentication.<br>
Below is a brief explanation of the code, the explanation of the approach used to solve the challenge, instructions on how to run the code, and several notes regarding the solution.

## Code

### Techstack
- Node.js (Typescript)
- Express.js
- Prisma ORM
- MySQL

### Endpoints
1. POST/ login (user authentication)
This endpoint allows users to authenticate by providing a valid username and password
- Request Body:
username (string, required)
password (string, required)
- Expected Response:
(200) Returns a success message along with a JSON Web Token (JWT) for authentication.
(400) Data can’t be stored into the database (doesn’t met the criteria) or authentication failure.
(500) Issue on generating the token.
- Flow:
'1. Validates that both username and password are provided.
'2. Search for the user data by the provided username.
'3. Verifies the inputed password by comparing it with the stored password hash.
'4. Generates a JWT token (authentication token) if the given credentials are correct.
'5. If the credentials are valid, return a success message along with the JWT token. if not, return a failure message.

2. POST/ register (user registration)
This endpoint allows new users to register by providing a username and password.
- Request Body:
username (string, required)
password (string, required)
- Expected Response:
(200) Returns a success message when the user is successfully registered.
(400) Returns an error if the username is already taken, or if the username/password don't meet the validation criteria.
- Flow:
'1. Validates that both username and password are provided.
'2. Checks if the username length is between 1 and 15 characters.
'3. Checks if the password is at least 8 characters long, and consist of combination of letter, number, and symbol (using regex).
'4. Generate a salt with 10 rounds of processing.
'5. Hashes the password with the generated salt using bcrypt and stores the user in the database.
'6. If the username is already in use (or the credentials given is invalid), returns an error. Otherwise, the user is registered successfully and it would return a success message.