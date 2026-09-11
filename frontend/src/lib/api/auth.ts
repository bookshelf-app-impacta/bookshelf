import type { User } from "@/types/user";

type LoginPayload = {
  email: string;
  password: string;
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