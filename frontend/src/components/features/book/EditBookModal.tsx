"use client";

import { useEffect, useState } from "react";
import { X } from "lucide-react";
import type { Book } from "@/types/book";
import { ApiError, updateBook } from "@/lib/api/books";

type EditBookModalProps = {
  book: Book | null;
  onClose: () => void;
  onSave: (book: Book) => void;
};

export function EditBookModal({ book, onClose, onSave }: EditBookModalProps) {
  const [title, setTitle] = useState("");
  const [originalTitle, setOriginalTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [releaseYear, setReleaseYear] = useState("");
  const [synopsis, setSynopsis] = useState("");
  const [isbn13, setIsbn13] = useState("");
  const [publisher, setPublisher] = useState("");
  const [pageCount, setPageCount] = useState("");
  const [language, setLanguage] = useState("");
  const [coverUrl, setCoverUrl] = useState("");

  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  // Repreenche o formulario sempre que um livro diferente for aberto
  // pra edicao — sem isso sobraria o valor do livro anterior na tela.
  useEffect(() => {
    if (!book) return;
    setTitle(book.title);
    setOriginalTitle(book.original_title ?? "");
    setAuthor(book.author?.name ?? "");
    setReleaseYear(book.release_year?.toString() ?? "");
    setSynopsis(book.synopsis ?? "");
    setIsbn13(book.isbn13 ?? "");
    setPublisher(book.publisher ?? "");
    setPageCount(book.page_count?.toString() ?? "");
    setLanguage(book.language ?? "");
    setCoverUrl(book.cover_url ?? "");
    setErro(null);
  }, [book]);

  if (!book) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErro(null);
    setSalvando(true);

    try {
      const atualizado = await updateBook(book.id, {
        title,
        original_title: originalTitle || null,
        author: author || null,
        release_year: releaseYear ? Number(releaseYear) : null,
        synopsis: synopsis || null,
        isbn13: isbn13 || null,
        publisher: publisher || null,
        page_count: pageCount ? Number(pageCount) : null,
        language: language || null,
        cover_url: coverUrl || null,
      });
      onSave(atualizado);
      onClose();
    } catch (err) {
      setErro(err instanceof ApiError ? err.message : "Nao foi possivel salvar as alteracoes.");
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Editar livro</h2>
          <button onClick={onClose}>
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            placeholder="Título"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
            required
          />
          <input
            placeholder="Título original"
            value={originalTitle}
            onChange={(e) => setOriginalTitle(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />
          <input
            placeholder="Autor"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />

          <div className="grid grid-cols-2 gap-3">
            <input
              type="number"
              placeholder="Ano"
              value={releaseYear}
              onChange={(e) => setReleaseYear(e.target.value)}
              className="border rounded-lg px-3 py-2 text-sm"
            />
            <input
              type="number"
              placeholder="Páginas"
              value={pageCount}
              onChange={(e) => setPageCount(e.target.value)}
              className="border rounded-lg px-3 py-2 text-sm"
            />
          </div>

          <textarea
            placeholder="Sinopse"
            value={synopsis}
            onChange={(e) => setSynopsis(e.target.value)}
            rows={3}
            className="border rounded-lg px-3 py-2 text-sm"
          />

          <input
            placeholder="ISBN-13"
            value={isbn13}
            onChange={(e) => setIsbn13(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />
          <input
            placeholder="Editora"
            value={publisher}
            onChange={(e) => setPublisher(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm"
          />

          <div className="grid grid-cols-2 gap-3">
            <input
              placeholder="Idioma"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border rounded-lg px-3 py-2 text-sm"
            />
            <input
              placeholder="URL da capa"
              value={coverUrl}
              onChange={(e) => setCoverUrl(e.target.value)}
              className="border rounded-lg px-3 py-2 text-sm"
            />
          </div>

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
