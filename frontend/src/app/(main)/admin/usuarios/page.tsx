"use client";
import { useState } from "react";// hook(permite que a função tenha memória própria e reagir a mudanças) do React pra guardar estado
// componentes da feature de usuário
import { UsersToolbar } from "@/components/features/user/UsersToolbar";
import { UserTable } from "@/components/features/user/UserTable";
import { AddUserModal } from "@/components/features/user/AddUserModal";
import { EditUserModal } from "@/components/features/user/EditUserModal";
import { DeleteUserModal } from "@/components/features/user/DeleteUserModal";

import { User } from "@/types/user"; // tipo (formato) que descreve os dados de um usuário

//usuário fake
const usuariosMock: User[] = [
  {
    id: 1,
    username: "karthi",
    displayName: "Karthi",
    email: "karthi@gmail.com",
    avatarUrl: "https://i.pravatar.cc/80",
    role: "admin",
    isActive: true,
  },
];

export default function UsuariosPage() {
  //constantes e seus estados
  const [users, setUsers] = useState<User[]>(usuariosMock);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [userEditando, setUserEditando] = useState<User | null>(null);
  const [userExcluindo, setUserExcluindo] = useState<User | null>(null);

  //filtro na tabela, por enquanto apenas pegando o termo e jogando no console...
  function handleBuscar(termo: string) {
    console.log("buscando:", termo);
  }

  //adicionar um novo usuário, ainda falta integração
  function handleAdd(dados: Omit<User, "id" | "isActive">) {
    //cria um usuário com algumas infos da classe
    const novo: User = { ...dados, id: Date.now(), isActive: true };
    setUsers((prev) => [...prev, novo]);
    // POST /users
  }

  // alterna is_active (ativo/inativo) sem abrir modal
  function handleToggleActive(user: User) {
  //transforma cada item, mas mantém a mesma quantidade no array  
  setUsers((prev) =>
    prev.map((u) => (u.id === user.id ? { ...u, isActive: !u.isActive } : u))
  );
  // depois: PATCH /users/:id/status (ou rota equivalente, a combinar com o backend)
}

  //edita o usuário
  function handleEditSave(userAtualizado: User) {
    //faz um filtro do usuário
    setUsers((prev) => prev.map((u) => (u.id === userAtualizado.id ? userAtualizado : u)));
    // PUT/PATCH /users/:id
  }

  function handleDeleteConfirm(user: User) {
    //remove itens, devolvendo só os que passam numa condição
    setUsers((prev) => prev.filter((u) => u.id !== user.id));
    // DELETE /users/:id
  }
  //retorna html
  return (
    <div className="px-8 py-6">
      {/* chama a função de busca */}
      <UsersToolbar onAdicionar={() => setAddModalOpen(true)} onBuscar={handleBuscar} />
      {/* chama a tabela */}
      <UserTable
        users={users}
        onEdit={(user) => setUserEditando(user)}
        onDelete={(user) => setUserExcluindo(user)}
        onToggleActive={handleToggleActive}
      />
      {/* chama as interações da tabela */}
      <AddUserModal open={addModalOpen} onClose={() => setAddModalOpen(false)} onSave={handleAdd} />
      <EditUserModal user={userEditando} onClose={() => setUserEditando(null)} onSave={handleEditSave} />
      <DeleteUserModal user={userExcluindo} onClose={() => setUserExcluindo(null)} onConfirm={handleDeleteConfirm} />
    </div>
  );
}