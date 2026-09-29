"use client";

import { useState } from "react";
import { User } from "@/types/user";//importa o molde do objeto
import { ApiError, deleteUser } from "@/lib/api/users";

//cria um molde para a função
type DeleteUserModalProps = {
  user: User | null;
  onClose: () => void;
  onConfirm: (user: User) => void;
};

export function DeleteUserModal({ user, onClose, onConfirm }: DeleteUserModalProps) {
  const [erro, setErro] = useState<string | null>(null);
  const [excluindo, setExcluindo] = useState(false);

  if (!user) return null;

  const handleConfirm = async () => {
    setErro(null);
    setExcluindo(true);

    try {
      await deleteUser(user.id);
      onConfirm(user);
      onClose();
    } catch (err) {
      // Cobre os 400/409 do backend: auto-exclusao e usuario que
      // cadastrou livro (ON DELETE RESTRICT). Sem mostrar isso, o
      // admin so veria o modal fechar sem nada acontecer.
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel excluir o usuario.");
    } finally {
      setExcluindo(false);
    }
  };

  //retorna um html
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-sm text-center">
        <h2 className="text-lg font-semibold mb-2">Excluir usuário</h2>
        <p className="text-sm text-gray-500 mb-4">
          Tem certeza que deseja excluir <strong>{user.username}</strong>? Essa ação não pode ser
          desfeita.
        </p>

        {erro && <p className="text-red-600 text-sm mb-4">{erro}</p>}

        <div className="flex gap-3 justify-center">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-sm border text-gray-600 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            onClick={handleConfirm}
            disabled={excluindo}
            className="px-4 py-2 rounded-lg text-sm bg-red-600 text-white hover:bg-red-700 disabled:opacity-60"
          >
            {excluindo ? "Excluindo..." : "Excluir"}
          </button>
        </div>
      </div>
    </div>
  );
}
