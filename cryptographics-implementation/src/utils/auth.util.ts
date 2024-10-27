import { sign, SignOptions, verify } from 'jsonwebtoken';
import dotenv from 'dotenv';
dotenv.config();

export const generateToken = async (id: string) => {
  const payload = {
    id: id
  }

  const secretKey: string | undefined = process.env.JWT_SECRET;

  if (!secretKey) {
    return [false, null]
  }

  const opt: SignOptions = {
    // algorithm: 'RS256',
    expiresIn: '1h',
  }

  const token = sign(payload, secretKey, opt);
  return [true, token];
}

export const validateToken = async (token: string): Promise<any> => {
  const secretKey: string | undefined = process.env.JWT_SECRET;

  if (!secretKey) {
    return [false, null]
  }

  const decoded = verify(token, secretKey);
  return [true, decoded];
}