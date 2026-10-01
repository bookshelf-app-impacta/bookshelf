import type { User } from "@/types/user";
import { ApiError } from "@/lib/errors";

type LoginPayload = {
  email: string;
  password: string;
};

type RegisterPayload = {
  username: string;
  email: string;
  password: string;
  displayName?: string; // o backend lê "displayName", não "nome"
};

type LoginResponse = {
  token: string;
  user: User;
};

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new Error(data?.error ?? "Credenciais inválidas");
  }

  return response.json();
}

export async function register(payload: RegisterPayload): Promise<LoginResponse> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new ApiError(data?.error ?? "Não foi possível criar a conta.", data?.fields);
  }
  return response.json();
}