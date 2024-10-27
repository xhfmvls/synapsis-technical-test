import express, { Request, Response, Application } from 'express';
import dotenv from 'dotenv';
import bodyParser from 'body-parser';
import cors from 'cors';
import { login, register } from './controllers/auth.controller';
const { PrismaClient } = require('@prisma/client');
require('express-async-errors');

//For env File 
dotenv.config();

const app: Application = express();
const port = process.env.PORT || 8000;
app.use(cors());
app.use(bodyParser.json());

app.get('/', (req: Request, res: Response) => {
    res.send('Welcome to Express & TypeScript Server');
});

app.post('/login', login);

app.post('/register', register);

app.listen(port, () => {
    console.log(`Server is ready at http://localhost:${port}`);
});