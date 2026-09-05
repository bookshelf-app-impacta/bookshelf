"use client";

import { useState } from "react";
import { X, User as UserIcon } from "lucide-react";
import { User, UserRole } from "@/types/user";

type AddUserModalProps = {
  open: boolean;
  onClose: () => void;
  onSave: (dados: Omit<User, "id" | "isActive">) => void;
};

export function AddUserModal({ open, onClose, onSave }: AddUserModalProps) {
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<UserRole>("user");
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);

  if (!open) return null;

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setAvatarFile(file);
    setAvatarPreview(URL.createObjectURL(file));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSave({
      username,
      displayName: displayName || undefined,
      email,
      role,
      avatarUrl: avatarPreview ?? undefined,
    });
    resetForm();
    onClose();
  }

  function resetForm() {
    setUsername("");
    setDisplayName("");
    setEmail("");
    setRole("user");
    setAvatarFile(null);
    setAvatarPreview(null);
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Adicionar Usuário</h2>
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

          <select
            value={role}
            onChange={(e) => setRole(e.target.value as UserRole)}
            className="border rounded-lg px-3 py-2 text-sm"
          >
            <option value="user">Usuário</option>
            <option value="admin">Admin</option>
          </select>

          <button
            type="submit"
            className="bg-blue-700 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-800 mt-2"
          >
            Salvar
          </button>
        </form>
      </div>
    </div>
  );
}