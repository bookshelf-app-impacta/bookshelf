import type { Book, BookInput } from "@/types/book";

const BASE_URL = `${process.env.NEXT_PUBLIC_API_URL}/api/books`;

export class ApiError extends Error {
  fields?: Record<string, string>;

  constructor(message: string, fields?: Record<string, string>) {
    super(message);
    this.fields = fields;
  }
}

function authHeaders(): HeadersInit {
  // window nao existe durante SSR; GET nao precisa de token mesmo,
  // so POST/PUT/DELETE (protegidos por @admin_required no backend).
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function throwApiError(response: Response): Promise<never> {
  const data = await response.json().catch(() => null);
  throw new ApiError(data?.error ?? "Nao foi possivel completar a operacao.", data?.fields);
}

export async function listBooks(): Promise<Book[]> {
  const response = await fetch(`${BASE_URL}/`, { cache: "no-store" });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function getBook(id: number): Promise<Book> {
  const response = await fetch(`${BASE_URL}/${id}`, { cache: "no-store" });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function createBook(payload: BookInput): Promise<Book> {
  const response = await fetch(`${BASE_URL}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function updateBook(id: number, payload: Partial<BookInput>): Promise<Book> {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}

export async function deleteBook(id: number): Promise<void> {
  const response = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!response.ok) await throwApiError(response);
}
