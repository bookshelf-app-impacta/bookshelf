"use client";
import { useEffect, useState } from "react";// hook(permite que a função tenha memória própria e reagir a mudanças) do React pra guardar estado
// componentes da feature de usuário
import { UsersToolbar } from "@/components/features/user/UsersToolbar";
import { UserTable } from "@/components/features/user/UserTable";
import { AddUserModal } from "@/components/features/user/AddUserModal";
import { EditUserModal } from "@/components/features/user/EditUserModal";
import { DeleteUserModal } from "@/components/features/user/DeleteUserModal";
import { RequireAdmin } from "@/components/auth/RequireAdmin";
import { ApiError, listUsers, updateUser } from "@/lib/api/users";

import { User } from "@/types/user"; // tipo (formato) que descreve os dados de um usuário

export default function UsuariosPage() {
  //constantes e seus estados
  const [users, setUsers] = useState<User[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [busca, setBusca] = useState("");
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [userEditando, setUserEditando] = useState<User | null>(null);
  const [userExcluindo, setUserExcluindo] = useState<User | null>(null);

  // Busca a lista real na API quando a pagina monta — nao da pra
  // buscar no servidor (Server Component) porque o token vive no
  // localStorage, que so existe no navegador.
  useEffect(() => {
    listUsers()
      .then(setUsers)
      .catch((err) => {
        setErro(
          err instanceof ApiError ? err.message : "Nao foi possivel carregar os usuarios."
        );
      })
      .finally(() => setCarregando(false));
  }, []);

  //filtro na tabela, agora filtrando de verdade (antes so ia pro console)
  function handleBuscar(termo: string) {
    setBusca(termo);
  }

  const usuariosFiltrados = busca
    ? users.filter((u) =>
        `${u.username} ${u.displayName ?? ""} ${u.email}`
          .toLowerCase()
          .includes(busca.toLowerCase())
      )
    : users;

  //o proprio modal ja chamou a API — aqui so atualiza a lista local
  function handleAdd(novo: User) {
    setUsers((prev) => [...prev, novo]);
  }

  // alterna is_active (ativo/inativo) sem abrir modal
  async function handleToggleActive(user: User) {
    try {
      const atualizado = await updateUser(user.id, { isActive: !user.isActive });
      setUsers((prev) => prev.map((u) => (u.id === atualizado.id ? atualizado : u)));
    } catch (err) {
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel atualizar o status.");
    }
  }

  //edita o usuário — o modal ja chamou a API, so sincroniza a lista
  function handleEditSave(userAtualizado: User) {
    setUsers((prev) => prev.map((u) => (u.id === userAtualizado.id ? userAtualizado : u)));
  }

  function handleDeleteConfirm(user: User) {
    setUsers((prev) => prev.filter((u) => u.id !== user.id));
  }
  //retorna html
  return (
    <RequireAdmin>
      <div className="px-8 py-6">
        {erro && <p className="text-red-600 text-sm mb-4">{erro}</p>}

        {/* chama a função de busca */}
        <UsersToolbar onAdicionar={() => setAddModalOpen(true)} onBuscar={handleBuscar} />

        {carregando ? (
          <p className="text-gray-500 text-sm">Carregando...</p>
        ) : (
          // chama a tabela
          <UserTable
            users={usuariosFiltrados}
            onEdit={(user) => setUserEditando(user)}
            onDelete={(user) => setUserExcluindo(user)}
            onToggleActive={handleToggleActive}
          />
        )}

        {/* chama as interações da tabela */}
        <AddUserModal open={addModalOpen} onClose={() => setAddModalOpen(false)} onSave={handleAdd} />
        <EditUserModal user={userEditando} onClose={() => setUserEditando(null)} onSave={handleEditSave} />
        <DeleteUserModal user={userExcluindo} onClose={() => setUserExcluindo(null)} onConfirm={handleDeleteConfirm} />
      </div>
    </RequireAdmin>
  );
}
