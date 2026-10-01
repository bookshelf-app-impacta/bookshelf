"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { register } from "@/lib/api/auth";
import { saveSession } from "@/lib/auth";
import { ApiError } from "@/lib/errors";

type FieldErrors = Record<string, string>;

export function RegisterForm() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [nome, setNome] = useState("");

  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [erro, setErro] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setFieldErrors({});
    setCarregando(true);
    try {
      const { token, user } = await register({
        username,
        email,
        password: senha,
        displayName: nome || undefined,
      });
      saveSession(token, user);
      router.push("/");
    } catch (err) {
      if (err instanceof ApiError) {
        setFieldErrors(err.fields ?? {});
        setErro(err.fields ? null : err.message);
      } else {
        setErro("Não foi possível criar a conta.");
      }
    } finally {
      setCarregando(false);
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-8">
      <div className="flex items-center gap-2 mb-1">
        <span className="w-1 h-6 bg-blue-700 rounded" />
        <h1 className="text-2xl font-black">Bookshelf</h1>
      </div>
      <p className="text-center font-semibold text-sm mb-1">CADASTRO</p>
      <p className="text-center text-gray-400 text-xs mb-6">
        Preencha os dados para criar sua conta
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label htmlFor="username" className="text-sm text-gray-700">Usuário</label>
          <input
            id="username"
            placeholder="Digite seu nome de usuário"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            minLength={3}
            maxLength={30}
            required
          />
          {fieldErrors.username && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.username}</p>
          )}
        </div>

        <div>
          <label htmlFor="email" className="text-sm text-gray-700">E-mail</label>
          <input
            id="email"
            type="email"
            placeholder="Digite seu e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            maxLength={255}
            required
          />
          {fieldErrors.email && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.email}</p>
          )}
        </div>

        <div>
          <label htmlFor="senha" className="text-sm text-gray-700">Senha</label>
          <input
            id="senha"
            type="password"
            placeholder="Mínimo de 8 caracteres"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            minLength={8}
            required
          />
          {fieldErrors.password && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.password}</p>
          )}
        </div>

        <div>
          <label htmlFor="nome" className="text-sm text-gray-700">Nome (opcional)</label>
          <input
            id="nome"
            placeholder="Como você quer ser chamado"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            maxLength={80}
          />
          {fieldErrors.displayName && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.displayName}</p>
          )}
        </div>

        {erro && <p className="text-red-600 text-sm">{erro}</p>}

        <button
          type="submit"
          disabled={carregando}
          className="bg-blue-800 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
        >
          {carregando ? "Cadastrando..." : "CADASTRAR"}
        </button>

        <p className="text-center text-xs text-gray-500">
          Já tem conta?{" "}
          <Link href="/login" className="text-blue-700 font-semibold underline">
            Entrar
          </Link>
        </p>
      </form>
    </div>
  );
}
