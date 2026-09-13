import { redirect } from "next/navigation";

// O catalogo de livros agora e a Home ("/"). Mantemos essa rota so
// porque o Nav.tsx ja tem um link pra "/estante" — redireciona em vez
// de duplicar a mesma lista em dois lugares.
export default function EstantePage() {
  redirect("/");
}
