"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Pencil, Trash2 } from "lucide-react";
import type { Book } from "@/types/book";
import { getCurrentUser } from "@/lib/auth";
import { EditBookModal } from "./EditBookModal";
import { DeleteBookModal } from "./DeleteBookModal";

type BookGridProps = {
  initialBooks: Book[];
};

export function BookGrid({ initialBooks }: BookGridProps) {
  const [books, setBooks] = useState<Book[]>(initialBooks);
  const [bookEditando, setBookEditando] = useState<Book | null>(null);
  const [bookExcluindo, setBookExcluindo] = useState<Book | null>(null);
  // Comeca false de proposito: no primeiro render (SSR) nao ha
  // localStorage, e usar o valor real aqui causaria um hydration
  // mismatch entre o HTML do servidor e o do client.
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    setIsAdmin(getCurrentUser()?.role === "admin");
  }, []);

  function handleSave(atualizado: Book) {
    setBooks((prev) => prev.map((b) => (b.id === atualizado.id ? atualizado : b)));
  }

  function handleDeleted(excluido: Book) {
    setBooks((prev) => prev.filter((b) => b.id !== excluido.id));
  }

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-black">Estante</h1>
        {isAdmin && (
          <Link
            href="/livros/novo"
            className="bg-blue-800 text-white rounded-lg px-4 py-2 text-sm font-semibold hover:bg-blue-900"
          >
            + Adicionar livro
          </Link>
        )}
      </div>

      {books.length === 0 ? (
        <p className="text-gray-500 text-sm">Nenhum livro cadastrado ainda.</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {books.map((book) => (
            <div
              key={book.id}
              className="bg-white rounded-xl shadow p-4 flex flex-col gap-1 relative"
            >
              {isAdmin && (
                <div className="absolute top-2 right-2 flex gap-1">
                  <button
                    onClick={() => setBookEditando(book)}
                    className="bg-white/90 rounded-full p-1.5 shadow hover:bg-gray-100"
                    aria-label="Editar livro"
                  >
                    <Pencil className="h-3.5 w-3.5 text-gray-600" />
                  </button>
                  <button
                    onClick={() => setBookExcluindo(book)}
                    className="bg-white/90 rounded-full p-1.5 shadow hover:bg-gray-100"
                    aria-label="Excluir livro"
                  >
                    <Trash2 className="h-3.5 w-3.5 text-red-600" />
                  </button>
                </div>
              )}

              <div className="h-40 w-full bg-gray-100 rounded-lg mb-2 overflow-hidden flex items-center justify-center text-gray-400 text-xs">
                {book.cover_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={book.cover_url}
                    alt={book.title}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  "Sem capa"
                )}
              </div>
              <p className="font-semibold text-sm truncate">{book.title}</p>
              <p className="text-xs text-gray-500">{book.author?.name ?? "Autor desconhecido"}</p>
              {book.release_year && <p className="text-xs text-gray-400">{book.release_year}</p>}
            </div>
          ))}
        </div>
      )}

      <EditBookModal book={bookEditando} onClose={() => setBookEditando(null)} onSave={handleSave} />
      <DeleteBookModal
        book={bookExcluindo}
        onClose={() => setBookExcluindo(null)}
        onDeleted={handleDeleted}
      />
    </>
  );
}
