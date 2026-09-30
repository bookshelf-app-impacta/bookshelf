"use client";

import { useState } from "react";

export function RegisterForm() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [nome, setNome] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
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
        </div>

        <button
          type="submit"
          className="bg-blue-800 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-900"
        >
          CADASTRAR
        </button>
      </form>
    </div>
  );
}
