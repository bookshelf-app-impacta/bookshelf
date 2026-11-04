"use client";

import { useEffect, useId, useState } from "react";
import type { Review } from "@/types/review";
import { createReview, updateReview } from "@/lib/api/reviews";
import { ApiError } from "@/lib/errors";

type FieldErrors = Record<string, string>;

type ReviewFormProps = {
  bookId: number;
  review?: Review | null;
  onSaved: (review: Review) => void;
  onCancel?: () => void;
};

export function ReviewForm({ bookId, review, onSaved, onCancel }: ReviewFormProps) {
  const editando = !!review;

  const campoId = useId();

  const [body, setBody] = useState(review?.body ?? "");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  // Repreenche quando outra review for aberta pra edicao 
  useEffect(() => {
    setBody(review?.body ?? "");
    setFieldErrors({});
    setErro(null);
  }, [review]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setFieldErrors({});

    // So espacos nao e comentario. O backend tambem valida, mas barrar
    // aqui poupa uma ida a API.
    const texto = body.trim();
    if (!texto) {
      setFieldErrors({ body: "Escreva um comentário." });
      return;
    }

    setSalvando(true);
    try {
      const salva = review
        ? await updateReview(review.id, { body: texto })
        : await createReview(bookId, { body: texto });
      onSaved(salva);
      // Criou: limpa pro proximo uso. Editou: o pai fecha o modo edicao.
      if (!review) setBody("");
    } catch (err) {
      if (err instanceof ApiError) {
        setFieldErrors(err.fields ?? {});
        setErro(err.fields ? null : err.message);
      } else {
        setErro("Não foi possível salvar o comentário.");
      }
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div>
        <label htmlFor={campoId} className="text-sm text-gray-700">
          {editando ? "Editar comentário" : "Seu comentário"}
        </label>
        <textarea
          id={campoId}
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={4}
          placeholder="O que você achou do livro?"
          className="w-full border rounded-lg px-3 py-2 text-sm mt-1"
        />
        {fieldErrors.body && <p className="text-red-600 text-xs mt-1">{fieldErrors.body}</p>}
      </div>

      {erro && <p className="text-red-600 text-sm">{erro}</p>}

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={salvando}
          className="bg-blue-800 text-white rounded-lg py-2 px-6 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
        >
          {salvando ? "Salvando..." : editando ? "Salvar alterações" : "Comentar"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 rounded-lg text-sm border text-gray-600 hover:bg-gray-50"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
