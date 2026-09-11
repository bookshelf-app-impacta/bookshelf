"use client";

import { useState } from "react";
import Link from "next/link";
import { login } from "@/lib/api/auth";
import { useRouter } from "next/navigation";

export function LoginForm() {
  const router = useRouter();
  //constantes e seus estados. 
  //retorna um array com 2 posições: [valorAtual, funçãoQueAtualiza]
  //[variável sempre lida, única forma permitida para alterar o valor da primeira variável]
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);

  //função assincrona = não vai parar o projeto esperando uma resposta
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setCarregando(true);

    try {
      const { token, user } = await login({ email, password: senha });
      localStorage.setItem("token", token);
      router.push("/"); // rota da home
    } catch (err) {
      setErro(err instanceof Error ? err.message : "E-mail ou senha inválidos.");
    } finally {
      setCarregando(false);
    }
  }
  //html do formulário
  return (
    <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-8">
      <div className="flex items-center gap-2 mb-1">
        <span className="w-1 h-6 bg-blue-700 rounded" />
        <h1 className="text-2xl font-black">Bookshelf</h1>
      </div>
      <p className="text-center font-semibold text-sm mb-1">SIGN IN</p>
      <p className="text-center text-gray-400 text-xs mb-6">
        Enter your credentials to access your account
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label className="text-sm text-gray-700">Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            required
          />
        </div>

        <div>
          <label className="text-sm text-gray-700">Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
            required
          />
        </div>

        <div className="text-right text-xs text-gray-500">
          Forgot your password?{" "}
          <Link href="/reset-password" className="text-blue-700 font-semibold underline">
            Reset Password
          </Link>
        </div>

        {erro && <p className="text-red-600 text-sm">{erro}</p>}

        <button
          type="submit"
          disabled={carregando}
          className="bg-blue-800 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
        >
          {carregando ? "Entrando..." : "SIGN IN"}
        </button>
      </form>
    </div>
  );
}