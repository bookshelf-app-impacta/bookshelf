import type { User } from "@/types/user";

// Le o usuario salvo pelo LoginForm (ver components/features/auth/LoginForm.tsx).
// So funciona no client — chamar isso durante SSR sempre devolve null.
export function getCurrentUser(): User | null {
  if (typeof window === "undefined") return null;

  const raw = localStorage.getItem("user");
  if (!raw) return null;

  try {
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

// Usado no "Sair" do Header. So limpa o client — nao existe sessao no
// servidor pra invalidar, o token so perde validade quando expira.
export function clearSession(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}
