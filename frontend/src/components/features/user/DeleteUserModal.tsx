"use client";

import { User } from "@/types/user";//importa o molde do objeto

//cria um molde para a função
// função que recebe o usuário a excluir e não devolve nada, só executa a ação
type DeleteUserModalProps = {
  user: User | null;
  onClose: () => void;
  onConfirm: (user: User) => void;
};

export function DeleteUserModal({ user, onClose, onConfirm }: DeleteUserModalProps) {
  if (!user) return null;
//retorna um html
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-sm text-center">
        <h2 className="text-lg font-semibold mb-2">Excluir usuário</h2>
        <p className="text-sm text-gray-500 mb-6">
          Tem certeza que deseja excluir <strong>{user.username}</strong>? Essa ação não pode ser desfeita.
        </p>

        <div className="flex gap-3 justify-center">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-sm border text-gray-600 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            onClick={() => {
              onConfirm(user);
              onClose();
            }}
            className="px-4 py-2 rounded-lg text-sm bg-red-600 text-white hover:bg-red-700"
          >
            Excluir
          </button>
        </div>
      </div>
    </div>
  );
}