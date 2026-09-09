type LoginPayload = {
  email: string;
  senha: string;
};

export async function login(payload: LoginPayload) {
  // HOLD,esperando backend
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Credenciais inválidas");
  }

  return response.json();
}