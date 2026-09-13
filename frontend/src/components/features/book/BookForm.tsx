"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ApiError, createBook } from "@/lib/api/books";

type FieldErrors = Record<string, string>;

export function BookForm() {
  const router = useRouter();

  const [title, setTitle] = useState("");
  const [originalTitle, setOriginalTitle] = useState("");
  const [releaseYear, setReleaseYear] = useState("");
  const [synopsis, setSynopsis] = useState("");
  const [isbn13, setIsbn13] = useState("");
  const [publisher, setPublisher] = useState("");
  const [pageCount, setPageCount] = useState("");
  const [language, setLanguage] = useState("");
  const [coverUrl, setCoverUrl] = useState("");

  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setFieldErrors({});
    setSalvando(true);

    try {
      await createBook({
        title,
        original_title: originalTitle || undefined,
        release_year: releaseYear ? Number(releaseYear) : undefined,
        synopsis: synopsis || undefined,
        isbn13: isbn13 || undefined,
        publisher: publisher || undefined,
        page_count: pageCount ? Number(pageCount) : undefined,
        language: language || undefined,
        cover_url: coverUrl || undefined,
      });
      router.push("/");
    } catch (err) {
      if (err instanceof ApiError) {
        setFieldErrors(err.fields ?? {});
        setErro(err.message);
      } else {
        setErro("Nao foi possivel cadastrar o livro.");
      }
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl shadow-xl w-full max-w-2xl p-8 flex flex-col gap-4"
    >
      <div>
        <label className="text-sm text-gray-700">Título *</label>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          required
        />
        {fieldErrors.title && <p className="text-red-600 text-xs mt-1">{fieldErrors.title}</p>}
      </div>

      <div>
        <label className="text-sm text-gray-700">Título original</label>
        <input
          value={originalTitle}
          onChange={(e) => setOriginalTitle(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
        />
        {fieldErrors.original_title && (
          <p className="text-red-600 text-xs mt-1">{fieldErrors.original_title}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm text-gray-700">Ano de lançamento</label>
          <input
            type="number"
            value={releaseYear}
            onChange={(e) => setReleaseYear(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.release_year && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.release_year}</p>
          )}
        </div>

        <div>
          <label className="text-sm text-gray-700">Número de páginas</label>
          <input
            type="number"
            value={pageCount}
            onChange={(e) => setPageCount(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.page_count && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.page_count}</p>
          )}
        </div>
      </div>

      <div>
        <label className="text-sm text-gray-700">Sinopse</label>
        <textarea
          value={synopsis}
          onChange={(e) => setSynopsis(e.target.value)}
          rows={4}
          className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm text-gray-700">ISBN-13</label>
          <input
            value={isbn13}
            onChange={(e) => setIsbn13(e.target.value)}
            placeholder="9780000000000"
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.isbn13 && <p className="text-red-600 text-xs mt-1">{fieldErrors.isbn13}</p>}
        </div>

        <div>
          <label className="text-sm text-gray-700">Editora</label>
          <input
            value={publisher}
            onChange={(e) => setPublisher(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.publisher && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.publisher}</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm text-gray-700">Idioma</label>
          <input
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            placeholder="Português"
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.language && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.language}</p>
          )}
        </div>

        <div>
          <label className="text-sm text-gray-700">URL da capa</label>
          <input
            value={coverUrl}
            onChange={(e) => setCoverUrl(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
          />
          {fieldErrors.cover_url && (
            <p className="text-red-600 text-xs mt-1">{fieldErrors.cover_url}</p>
          )}
        </div>
      </div>

      {erro && <p className="text-red-600 text-sm">{erro}</p>}

      <button
        type="submit"
        disabled={salvando}
        className="bg-blue-800 text-white rounded-lg py-2 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60 self-start px-6 mt-2"
      >
        {salvando ? "Salvando..." : "Cadastrar livro"}
      </button>
    </form>
  );
}
