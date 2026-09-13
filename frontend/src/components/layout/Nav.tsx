import Link from "next/link";

export function Nav() {
  return (
    <nav className="flex gap-6">
      <Link href="/estante">Estante</Link>
      <Link href="/">Início</Link>
      <Link href="/minha-estante">Minha Estante</Link>
      <Link href="/comunidade">Comunidade</Link>
    </nav>
  );
}