"use client";

import { UsersToolbar } from "@/components/features/user/UsersToolbar";

export default function UsuariosPage() {
  function handleAdicionar() {
    // abre modal ou navega pra tela de novo usuário
    console.log("adicionar usuário");
  }

  function handleBuscar(termo: string) {
    console.log("buscando:", termo);
  }

  return (
    <div className="px-8 py-6">
      <UsersToolbar onAdicionar={handleAdicionar} onBuscar={handleBuscar} />
      {/* tabela vem aqui embaixo */}
    </div>
  );
}