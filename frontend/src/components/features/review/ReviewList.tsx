"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Review } from "@/types/review";
import type { User } from "@/types/user";
import { getCurrentUser } from "@/lib/auth";
import { listReviews } from "@/lib/api/reviews";
import { ApiError } from "@/lib/errors";
import { ReviewForm } from "./ReviewForm";
import { ReviewItem } from "./ReviewItem";
import { DeleteReviewModal } from "./DeleteReviewModal";

type ReviewListProps = {
  bookId: number;
};

export function ReviewList({ bookId }: ReviewListProps) {
  const router = useRouter();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  // undefined = ainda nao olhei o localStorage; null = deslogado. Sem
  // essa diferenca, quem esta logado veria "Entre para avaliar" por um
  // instante antes do useEffect rodar (mesmo cuidado do Header).
  const [user, setUser] = useState<User | null | undefined>(undefined);
  const [editando, setEditando] = useState<Review | null>(null);
  const [excluindo, setExcluindo] = useState<Review | null>(null);

  useEffect(() => {
    setUser(getCurrentUser());
  }, []);

  useEffect(() => {
    listReviews(bookId)
      .then(setReviews)
      .catch((err) => {
        setErro(
          err instanceof ApiError ? err.message : "Não foi possível carregar as avaliações.",
        );
      })
      .finally(() => setCarregando(false));
  }, [bookId]);

  // O banco so aceita uma review por usuario por livro. Quem ja tem a
  // sua nao ve o formulario de criar — edita pela propria avaliacao.
  const minhaReview = user ? reviews.find((r) => r.user.id === user.id) : undefined;

  // Os modais/formularios ja chamaram a API — aqui so sincroniza a tela.
  // O refresh() refaz a parte do servidor da pagina, onde mora a media
  // do banner; o estado desta lista continua como esta.
  function handleCriada(nova: Review) {
    setReviews((prev) => [nova, ...prev]);
    router.refresh();
  }

  function handleEditada(atualizada: Review) {
    setReviews((prev) => prev.map((r) => (r.id === atualizada.id ? atualizada : r)));
    setEditando(null);
    router.refresh();
  }

  function handleExcluida(excluida: Review) {
    setReviews((prev) => prev.filter((r) => r.id !== excluida.id));
    router.refresh();
  }

  return (
    <div>
      {user === null && (
        <p className="mb-8 text-sm text-gray-500">
          <Link href="/login" className="font-semibold text-blue-700 hover:underline">
            Entre
          </Link>{" "}
          para avaliar este livro.
        </p>
      )}
      {user && !minhaReview && (
        <div className="mb-8">
          <ReviewForm bookId={bookId} onSaved={handleCriada} />
        </div>
      )}

      {carregando ? (
        <p className="text-sm text-gray-500">Carregando...</p>
      ) : erro ? (
        <p className="text-sm text-red-600">{erro}</p>
      ) : reviews.length === 0 ? (
        <p className="text-sm text-gray-400">Ainda não há avaliações neste livro.</p>
      ) : (
        <div className="divide-y">
          {reviews.map((review) =>
            editando?.id === review.id ? (
              <div key={review.id} className="py-5">
                <ReviewForm
                  bookId={bookId}
                  review={review}
                  onSaved={handleEditada}
                  onCancel={() => setEditando(null)}
                />
              </div>
            ) : (
              <ReviewItem
                key={review.id}
                review={review}
                isOwn={user?.id === review.user.id}
                onEdit={() => setEditando(review)}
                onDelete={() => setExcluindo(review)}
              />
            ),
          )}
        </div>
      )}

      <DeleteReviewModal
        review={excluindo}
        onClose={() => setExcluindo(null)}
        onDeleted={handleExcluida}
      />
    </div>
  );
}