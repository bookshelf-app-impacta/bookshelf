"use client";

import { useState } from "react";
import type { Book } from "@/types/book";
import { ApiError, deleteBook } from "@/lib/api/books";

type DeleteBookModalProps = {
  book: Book | null;
  onClose: () => void;
  onDeleted: (book: Book) => void;
};

export function DeleteBookModal({ book, onClose, onDeleted }: DeleteBookModalProps) {
  const [erro, setErro] = useState<string | null>(null);
  const [excluindo, setExcluindo] = useState(false);

  if (!book) return null;

  const handleConfirm = async () => {
    setErro(null);
    setExcluindo(true);

    try {
      await deleteBook(book.id);
      onDeleted(book);
      onClose();
    } catch (err) {
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel excluir o livro.");
    } finally {
      setExcluindo(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-sm text-center">
        <h2 className="text-lg font-semibold mb-2">Excluir livro</h2>
        <p className="text-sm text-gray-500 mb-4">
          Tem certeza que deseja excluir <strong>{book.title}</strong>? Essa ação não pode ser
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
