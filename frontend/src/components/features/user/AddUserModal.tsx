"use client";

import { useState } from "react";// hook(permite que a função tenha memória própria e reagir a mudanças) do React pra guardar estado
import { X, User as UserIcon } from "lucide-react";//icones
import { User, UserRole } from "@/types/user";//importa o molde do objeto
import { ApiError, createUser } from "@/lib/api/users";

//cria um molde para a função
type AddUserModalProps = {
  open: boolean;//se vai abrir sim/não
  onClose: () => void;//quando fechado...
  onSave: (user: User) => void; // roda depois que a API confirma a criacao
};

export function AddUserModal({ open, onClose, onSave }: AddUserModalProps) {
  //cosntante e seus estados
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("user");
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);

  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  //se não esta aberto nada acontece
  if (!open) return null;

  //função caso o arquivo mude
  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    //percebe a mudança
    const file = e.target.files?.[0];// pega o primeiro arquivo escolhido no input
    if (!file) return; // se o usuário cancelou a seleção, não faz nada
    setAvatarFile(file);// guarda o arquivo em si (pra futuro envio ao backend)
    setAvatarPreview(URL.createObjectURL(file));// gera uma URL temporária só pra mostrar a prévia na tela
  }

  //caso envio
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();//sem recarregar a página toda depois de enviar
    setErro(null);
    setSalvando(true);

    try {
      // avatarUrl nao vai pro backend: a previa acima e so um blob:
      // local do navegador, nao existe upload de arquivo na API ainda.
      // Mandar isso pra frente so salvaria um link que nao abre.
      const novo = await createUser({
        username,
        email,
        password,
        displayName: displayName || undefined,
        role,
      });
      onSave(novo);
      resetForm();
      onClose();
    } catch (err) {
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel criar o usuario.");
    } finally {
      setSalvando(false);
    }
  }

  function handleClose() {
    resetForm();
    onClose();
  }

  //função pra limpar tudo
  function resetForm() {
    setUsername("");
    setDisplayName("");
    setEmail("");
    setPassword("");
    setRole("user");
    setAvatarFile(null);
    setAvatarPreview(null);
    setErro(null);
  }
  //retorna html
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Adicionar Usuário</h2>
          <button onClick={handleClose}>
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
              {avatarFile ? "Trocar foto" : "Adicionar foto (opcional)"}
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
            placeholder="Senha"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
            required
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
            {salvando ? "Salvando..." : "Salvar"}
          </button>
        </form>
      </div>
    </div>
  );
}
