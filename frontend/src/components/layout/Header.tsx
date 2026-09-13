"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { User } from "@/types/user";
import { clearSession, getCurrentUser } from "@/lib/auth";
import { Nav } from "./Nav";
import { UserBadge } from "./UserBadge";

export function Header() {
  const router = useRouter();
  // Comeca null de proposito (mesmo raciocinio do RequireAdmin): no
  // primeiro render nao ha localStorage ainda, e usar o valor real
  // aqui causaria hydration mismatch entre servidor e client.
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    setUser(getCurrentUser());
  }, []);

  function handleLogout() {
    clearSession();
    setUser(null);
    router.push("/login");
  }

  return (
    <header className="flex items-center justify-between px-8 py-4">
      <span className="font-black text-[56px]">Bookshelf</span>
      <Nav />
      {user ? (
        <UserBadge user={user} onLogout={handleLogout} />
      ) : (
        <Link href="/login" className="text-sm font-semibold text-blue-700 hover:underline">
          Entrar
        </Link>
      )}
    </header>
  );
}
