"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "@/lib/auth";

type RequireAdminProps = {
  children: React.ReactNode;
};

/**
 * Bloqueia o conteudo da pagina pra quem nao e admin — cobre o caso de
 * alguem digitar a URL direto na barra (ex.: /livros/novo), que nao
 * passa pelos links/botoes que ja ficam escondidos (ver BookGrid).
 *
 * So funciona como guarda no client, porque login aqui e so token no
 * localStorage, sem cookie de sessao — nao tem como o middleware do
 * Next (que roda no servidor) ler isso. Por comecar em "checking" e so
 * liberar o conteudo depois do useEffect, o HTML inicial do servidor e
 * o primeiro render do client sao iguais (null) — sem hydration
 * mismatch e sem a tela protegida aparecer um instante antes do
 * redirecionamento.
 */
export function RequireAdmin({ children }: RequireAdminProps) {
  const router = useRouter();
  const [status, setStatus] = useState<"checking" | "allowed">("checking");

  useEffect(() => {
    const user = getCurrentUser();

    if (!user) {
      router.replace("/login");
      return;
    }
    if (user.role !== "admin") {
      router.replace("/");
      return;
    }
    setStatus("allowed");
  }, [router]);

  if (status !== "allowed") {
    return null;
  }

  return <>{children}</>;
}
