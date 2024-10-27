import express, { Express, Request, Response, Application } from 'express';
import bcrypt from "bcrypt";
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

export const login = async (req: Request, res: Response) => {
    const body = req.body;

    // Check if username and password are provided
    if (!body.username || !body.password) {
        res.status(400).send('Both username and password are required');
        return;
    }

    const username = body.username;
    const password = body.password;

    // get the user data with the provided username
    const user = await prisma.User.findUnique({
        where: {
            username: username
        }
    });

    // check if the user exists
    if (!user) {
        res.status(400).send('Invalid username or password');
        return;
    }

    // get the stored password hash and compare the password with the stored password hash
    const storedPasswordHash = user.password_hash;
    const isPasswordMatch = bcrypt.compareSync(password, storedPasswordHash);

    // if the password does not match, return an error
    if (!isPasswordMatch) {
        res.status(400).send('Invalid username or password');
        return;
    }

    res.status(200).send('User logged in successfully');
    return;
}

export const register = async (req: Request, res: Response) => {
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
        // create a new user with the provided username and hashed password
        await prisma.User.create({
            data: {
                username: username,
                password_hash: hashedPassword
            }
        });
    }
    catch (error) {
        // if the username already exists, return an error
        res.status(400).send('Username already exists');
        return;
    }

    res.status(200).send('User registered successfully');
    return;
}