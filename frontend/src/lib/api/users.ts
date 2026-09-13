import type { User, UserRole } from "@/types/user";

const BASE_URL = `${process.env.NEXT_PUBLIC_API_URL}/api/users`;

export class ApiError extends Error {
  fields?: Record<string, string>;

  constructor(message: string, fields?: Record<string, string>) {
    super(message);
    this.fields = fields;
  }
}

function authHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function throwApiError(response: Response): Promise<never> {
  const data = await response.json().catch(() => null);
  throw new ApiError(data?.error ?? "Nao foi possivel completar a operacao.", data?.fields);
}

export type CreateUserInput = {
  username: string;
  email: string;
  password: string;
  displayName?: string;
  role?: UserRole;
};

export type UpdateUserInput = Partial<{
  username: string;
  email: string;
  password: string;
  displayName: string;
  role: UserRole;
  isActive: boolean;
}>;

// Lista tambem exige token: diferente de livros, nao ha rota publica
// de usuario (e-mail de outra pessoa e dado sensivel).
export async function listUsers(): Promise<User[]> {
  const response = await fetch(`${BASE_URL}/`, { headers: authHeaders(), cache: "no-store" });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function createUser(payload: CreateUserInput): Promise<User> {
  const response = await fetch(`${BASE_URL}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function updateUser(id: number, payload: UpdateUserInput): Promise<User> {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function deleteUser(id: number): Promise<void> {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!response.ok) await throwApiError(response);
}
