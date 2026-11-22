"use client";

import { useEffect, useId, useState } from "react";
import type { Review } from "@/types/review";
import { createReview, updateReview } from "@/lib/api/reviews";
import { ApiError } from "@/lib/errors";
import { formatarNota } from "@/lib/rating";
import { StarRating } from "./StarRating";

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

  const [nota, setNota] = useState<number | null>(review?.rating ?? null);
  const [body, setBody] = useState(review?.body ?? "");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [erro, setErro] = useState<string | null>(null);
  const [salvando, setSalvando] = useState(false);

  // Repreenche quando outra review for aberta pra edicao
  useEffect(() => {
    setNota(review?.rating ?? null);
    setBody(review?.body ?? "");
    setFieldErrors({});
    setErro(null);
  }, [review]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    setFieldErrors({});

    // Mesma regra do backend (ck_reviews_nota_ou_texto): precisa de nota,
    // de texto, ou dos dois. Barrar aqui poupa uma ida a API.
    const texto = body.trim();
    if (nota === null && !texto) {
      setFieldErrors({ _geral: "Dê uma nota ou escreva um comentário." });
      return;
    }

    // Manda sempre os dois campos: o PUT do backend substitui tudo, entao
    // editar so o texto sem reenviar a nota apagaria a nota.
    const payload = { rating: nota, body: texto || null };

    setSalvando(true);
    try {
      const salva = review
        ? await updateReview(review.id, payload)
        : await createReview(bookId, payload);
      onSaved(salva);
      // Criou: limpa pro proximo uso. Editou: o pai fecha o modo edicao.
      if (!review) {
        setNota(null);
        setBody("");
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setFieldErrors(err.fields ?? {});
        setErro(err.fields ? null : err.message);
      } else {
        setErro("Não foi possível salvar a avaliação.");
      }
    } finally {
      setSalvando(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div>
        <p className="text-sm text-gray-700">{editando ? "Editar nota" : "Sua nota"}</p>
        <div className="mt-1 flex items-center gap-3">
          <StarRating value={nota} onChange={setNota} size={28} />
          {nota !== null && (
            <>
              <span className="text-sm font-semibold">{formatarNota(nota)}</span>
              <button
                type="button"
                onClick={() => setNota(null)}
                className="text-xs text-gray-500 hover:underline"
              >
                Limpar
              </button>
            </>
          )}
        </div>
        {fieldErrors.rating && <p className="text-red-600 text-xs mt-1">{fieldErrors.rating}</p>}
      </div>

      <div>
        <label htmlFor={campoId} className="text-sm text-gray-700">
          Comentário (opcional)
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

      {fieldErrors._geral && <p className="text-red-600 text-sm">{fieldErrors._geral}</p>}
      {erro && <p className="text-red-600 text-sm">{erro}</p>}

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={salvando}
          className="bg-blue-800 text-white rounded-lg py-2 px-6 text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
        >
          {salvando ? "Salvando..." : editando ? "Salvar alterações" : "Publicar"}
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