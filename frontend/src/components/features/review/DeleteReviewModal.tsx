"use client";

import { useState } from "react";
import type { Review } from "@/types/review";
import { deleteReview } from "@/lib/api/reviews";
import { ApiError } from "@/lib/errors";

type DeleteReviewModalProps = {
  review: Review | null;
  onClose: () => void;
  onDeleted: (review: Review) => void;
};

export function DeleteReviewModal({ review, onClose, onDeleted }: DeleteReviewModalProps) {
  const [erro, setErro] = useState<string | null>(null);
  const [excluindo, setExcluindo] = useState(false);

  if (!review) return null;

  const handleConfirm = async () => {
    setErro(null);
    setExcluindo(true);

    try {
      await deleteReview(review.id);
      onDeleted(review);
      onClose();
    } catch (err) {
      // Mostra o erro na propria janela (403 se nao for o autor, 401 se
      // a sessao expirou) em vez de fechar sem nada acontecer.
      setErro(err instanceof ApiError ? err.message : "Não foi possível excluir o comentário.");
    } finally {
      setExcluindo(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-sm rounded-lg bg-white p-6 text-center">
        <h2 className="mb-2 text-lg font-semibold">Excluir comentário</h2>
        <p className="mb-4 text-sm text-gray-500">
          Tem certeza que deseja excluir seu comentário? Essa ação não pode ser desfeita.
        </p>

        {erro && <p className="mb-4 text-sm text-red-600">{erro}</p>}

        <div className="flex justify-center gap-3">
          <button
            onClick={onClose}
            className="rounded-lg border px-4 py-2 text-sm text-gray-600 hover:bg-gray-50"
          >
            Cancelar
          </button>
          <button
            onClick={handleConfirm}
            disabled={excluindo}
            className="rounded-lg bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700 disabled:opacity-60"
          >
            {excluindo ? "Excluindo..." : "Excluir"}
          </button>
        </div>
      </div>
    </div>
  );
}
