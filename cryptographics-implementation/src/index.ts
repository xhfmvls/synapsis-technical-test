import express, { Express, Request, Response, Application } from 'express';
import dotenv from 'dotenv';
import bodyParser from 'body-parser';
import cors from 'cors';
import bcrypt from "bcrypt";
const { PrismaClient } = require('@prisma/client');
require('express-async-errors');

//For env File 
dotenv.config();

const app: Application = express();
const port = process.env.PORT || 8000;
const prisma = new PrismaClient();
app.use(cors());
app.use(bodyParser.json());

app.get('/', (req: Request, res: Response) => {
    res.send('Welcome to Express & TypeScript Server');
});

app.post('/register', async (req: Request, res: Response) => {
    const body = req.body;

    // Check if username and password are provided
    if (!body.username || !body.password) {
        res.status(400).send('Both username and password are required');
        return;
    }

    const username = body.username;
    const password = body.password;

    // check whether the username length is greater than 0 and less than 15
    if (username.length < 1 || username.length > 15) {
        res.status(400).send('Username should be between 1 and 15 characters');
        return;
    }

    // check whether the password length is greater than 8
    if (password.length < 8) {
        res.status(400).send('Password should be at least 8 characters');
        return;
    }

    // check whether the password consisting of combination of letter, number, and symbol
    if (!password.match(/^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])/)) {
        res.status(400).send('Password should consist of at least one letter, one number, and one symbol');
        return;
    }

    // generate salt (10 rounds)
    const salt = bcrypt.genSaltSync(10);

    // hash the password with the generated salt
    const hashedPassword = bcrypt.hashSync(password, salt);

    try {
        await prisma.User.create({
            data: {
                username: username,
                password_hash: hashedPassword
            }
        });
    }
    catch (error) {
        console.log(error);
        res.status(400).send('Username already exists');
        return;
    }

    res.status(200).send('User registered successfully');
    return;
});

app.listen(port, () => {
    console.log(`Server is ready at http://localhost:${port}`);
});