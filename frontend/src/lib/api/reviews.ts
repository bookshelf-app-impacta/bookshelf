import type { Review, ReviewInput } from "@/types/review";
import { ApiError } from "@/lib/errors";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

function authHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}
 
async function throwApiError(response: Response): Promise<never> {
  const data = await response.json().catch(() => null);
  throw new ApiError(data?.error ?? "Nao foi possivel completar a operacao.", data?.fields);
}
 
export async function listReviews(bookId: number): Promise<Review[]> {
  const response = await fetch(`${API_URL}/api/books/${bookId}/reviews/`, { cache: "no-store" });
  if (!response.ok) await throwApiError(response);
  return response.json();
}
 
export async function createReview(bookId: number, payload: ReviewInput): Promise<Review> {
  const response = await fetch(`${API_URL}/api/books/${bookId}/reviews/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}
 
export async function updateReview(id: number, payload: ReviewInput): Promise<Review> {
  const response = await fetch(`${API_URL}/api/reviews/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await throwApiError(response);
  return response.json();
}
 
export async function deleteReview(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/api/reviews/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!response.ok) await throwApiError(response);
}