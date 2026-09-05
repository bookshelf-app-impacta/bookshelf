"use client";

import { useState } from "react";
import { UsersToolbar } from "@/components/features/user/UsersToolbar";
import { UserTable } from "@/components/features/user/UserTable";
import { AddUserModal } from "@/components/features/user/AddUserModal";
import { EditUserModal } from "@/components/features/user/EditUserModal";
import { DeleteUserModal } from "@/components/features/user/DeleteUserModal";
import { User } from "@/types/user";

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
  const [users, setUsers] = useState<User[]>(usuariosMock);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [userEditando, setUserEditando] = useState<User | null>(null);
  const [userExcluindo, setUserExcluindo] = useState<User | null>(null);

  function handleBuscar(termo: string) {
    console.log("buscando:", termo);
  }

  function handleAdd(dados: Omit<User, "id" | "isActive">) {
    const novo: User = { ...dados, id: Date.now(), isActive: true };
    setUsers((prev) => [...prev, novo]);
    // POST /users
  }

  function handleEditSave(userAtualizado: User) {
    setUsers((prev) => prev.map((u) => (u.id === userAtualizado.id ? userAtualizado : u)));
    // PUT/PATCH /users/:id
  }

  function handleDeleteConfirm(user: User) {
    setUsers((prev) => prev.filter((u) => u.id !== user.id));
    // DELETE /users/:id
  }

  return (
    <div className="px-8 py-6">
      <UsersToolbar onAdicionar={() => setAddModalOpen(true)} onBuscar={handleBuscar} />

      <UserTable
        users={users}
        onEdit={(user) => setUserEditando(user)}
        onDelete={(user) => setUserExcluindo(user)}
      />

      <AddUserModal open={addModalOpen} onClose={() => setAddModalOpen(false)} onSave={handleAdd} />
      <EditUserModal user={userEditando} onClose={() => setUserEditando(null)} onSave={handleEditSave} />
      <DeleteUserModal user={userExcluindo} onClose={() => setUserExcluindo(null)} onConfirm={handleDeleteConfirm} />
    </div>
  );
}