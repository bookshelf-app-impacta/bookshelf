"use client";

import { useEffect, useState } from "react";// hook(permite que a função tenha memória própria e reagir a mudanças) do React pra guardar estado
import { X, User as UserIcon } from "lucide-react";//icone
import { User, UserRole } from "@/types/user";//importa o molde do objeto
import { ApiError, updateUser } from "@/lib/api/users";

//cria um molde para a função
type EditUserModalProps = {
  user: User | null;
  onClose: () => void;
  onSave: (user: User) => void;
};

export function EditUserModal({ user, onClose, onSave }: EditUserModalProps) {
  //cosntante e seus estados
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<UserRole>("user");
  const [novaSenha, setNovaSenha] = useState("");
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);

  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  //se tem o usuário, pode setar tudo com as funções de setar
  useEffect(() => {
    if (user) {
      setUsername(user.username);
      setDisplayName(user.displayName ?? "");
      setEmail(user.email);
      setRole(user.role);
      setAvatarPreview(user.avatarUrl ?? null);
      setNovaSenha("");
      setErro(null);
    }
  }, [user]);

  //caso não tenha usuário, não faça nada
  if (!user) return null;

  //caso a uma troca de imagem
  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];//pega a primeira imagem
    if (!file) return;// se o usuário cancelou a seleção, não faz nada
    setAvatarPreview(URL.createObjectURL(file));// gera uma URL temporária só pra mostrar a prévia na tela
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro(null);
    setSalvando(true);

    try {
      const atualizado = await updateUser(user.id, {
        username,
        email,
        role,
        displayName: displayName || undefined,
        // senha vazia = nao alterar (o backend trata assim em edicao,
        // diferente da criacao onde e obrigatoria).
        password: novaSenha || undefined,
      });
      onSave(atualizado);
      onClose();
    } catch (err) {
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel salvar as alterações.");
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Editar Usuário</h2>
          <button onClick={onClose}>
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <div className="flex flex-col items-center gap-2 mb-2">
            <div className="h-16 w-16 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
              {avatarPreview ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={avatarPreview} alt="Prévia" className="h-full w-full object-cover" />
              ) : (
                <UserIcon className="h-6 w-6 text-gray-400" />
              )}
            </div>
            <label className="text-sm text-blue-600 cursor-pointer">
              Trocar foto
              <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
            </label>
          </div>

          <input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
            required
          />
          <input
            placeholder="Nome de exibição (opcional)"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />
          <input
            placeholder="E-mail"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
            required
          />
          <input
            placeholder="Nova senha (deixe em branco para manter)"
            type="password"
            value={novaSenha}
            onChange={(e) => setNovaSenha(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />

          <select
            value={role}
            onChange={(e) => setRole(e.target.value as UserRole)}
            className="border rounded-lg px-3 py-2 text-sm"
          >
            <option value="user">Usuário</option>
            <option value="admin">Admin</option>
          </select>

          {erro && <p className="text-red-600 text-sm">{erro}</p>}

          <button
            type="submit"
            disabled={salvando}
            className="bg-blue-700 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-800 disabled:opacity-60 mt-2"
          >
            {salvando ? "Salvando..." : "Salvar alterações"}
          </button>
        </form>
      </div>
    </div>
  );
}
