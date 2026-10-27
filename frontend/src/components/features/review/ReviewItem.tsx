import type { Review } from "@/types/review";

type ReviewItemProps = {
  review: Review;
  // Dono do comentario: so ele ve Editar/Excluir. Esconder o botao e so
  // conforto — quem barra de verdade e o backend (403 se nao for o autor).
  isOwn: boolean;
  onEdit: () => void;
  onDelete: () => void;
};

export function ReviewItem({ review, isOwn, onEdit, onDelete }: ReviewItemProps) {
  const { user } = review;
  const nome = user.displayName ?? user.username;
  const data = new Date(review.createdAt).toLocaleDateString("pt-BR");

  return (
    <article className="flex gap-4 py-5">
      {user.avatarUrl ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={user.avatarUrl}
          alt={nome}
          className="h-10 w-10 shrink-0 rounded-full object-cover"
        />
      ) : (
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-100 text-sm font-semibold text-gray-500">
          {nome.charAt(0).toUpperCase()}
        </div>
      )}

      <div className="min-w-0 flex-1">
        <div className="flex items-baseline justify-between gap-3">
          <p className="truncate text-sm font-semibold">
            {nome} <span className="font-normal text-gray-400">@{user.username}</span>
          </p>
          <time dateTime={review.createdAt} className="shrink-0 text-xs text-gray-400">
            {data}
          </time>
        </div>

        <p className="mt-1 whitespace-pre-line text-sm leading-relaxed text-gray-700">
          {review.body}
        </p>

        {isOwn && (
          <div className="mt-2 flex gap-4 text-xs font-semibold">
            <button onClick={onEdit} className="text-blue-700 hover:underline">
              Editar
            </button>
            <button onClick={onDelete} className="text-red-600 hover:underline">
              Excluir
            </button>
          </div>
        )}
      </div>
    </article>
  );
}
