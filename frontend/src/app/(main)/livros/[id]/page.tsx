import Link from "next/link";
import { notFound } from "next/navigation";
import { BookOpen, ChevronLeft } from "lucide-react";
import { getBook } from "@/lib/api/books";
import type { Book } from "@/types/book";

type LivroPageProps = {
  // No Next 15+ os params chegam como Promise — por isso o await abaixo.
  params: Promise<{ id: string }>;
};

// Server Component (igual a Home): o livro e publico, entao da pra
// buscar no servidor. Os comentarios vao ser client components, porque
// precisam do token e do usuario que vivem no localStorage.
export default async function LivroPage({ params }: LivroPageProps) {
  const { id: idParam } = await params;
  const id = Number(idParam);

  // "/livros/abc" ou "/livros/0" nem chegam a ir pra API.
  if (!Number.isInteger(id) || id <= 0) notFound();

  let book: Book;
  try {
    book = await getBook(id);
  } catch {
    // Hoje qualquer falha vira 404, inclusive API fora do ar: o ApiError
    // do books.ts nao carrega o status HTTP pra distinguir os casos.
    notFound();
  }

  // Genero e ano viram "etiquetas" na faixa do topo; o resto vai pra
  // ficha de detalhes. So aparece o que o livro realmente tem.
  const etiquetas = [book.genre?.name, book.release_year].filter(
    (valor): valor is string | number => valor != null,
  );
  const ficha = [
    { rotulo: "Editora", valor: book.publisher },
    { rotulo: "Páginas", valor: book.page_count },
    { rotulo: "Idioma", valor: book.language },
    { rotulo: "ISBN-13", valor: book.isbn13 },
  ].filter((item) => item.valor);

  return (
    <div className="mx-auto max-w-5xl px-8 py-6">
      {/* Faixa do topo: mesmo degradê azul da tela de login, so que mais
          escuro pra o texto branco ter contraste. A capa e o destaque. */}
      <header className="rounded-2xl bg-gradient-to-br from-blue-800 via-blue-700 to-indigo-600 p-6 text-white sm:p-10">
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-sm text-blue-100 hover:text-white"
        >
          <ChevronLeft className="h-4 w-4" aria-hidden />
          Estante
        </Link>

        <div className="mt-6 flex flex-col gap-6 sm:flex-row sm:items-end sm:gap-10">
          <div className="flex aspect-[2/3] w-40 shrink-0 items-center justify-center overflow-hidden rounded-lg bg-blue-900/40 shadow-2xl ring-1 ring-white/20 sm:w-52">
            {book.cover_url ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={book.cover_url} alt={book.title} className="h-full w-full object-cover" />
            ) : (
              <div className="flex flex-col items-center gap-2 text-xs text-blue-100/70">
                <BookOpen className="h-8 w-8" aria-hidden />
                Sem capa
              </div>
            )}
          </div>

          <div className="flex min-w-0 flex-col gap-3">
            <h1 className="text-balance text-3xl font-black tracking-tight sm:text-5xl">
              {book.title}
            </h1>
            {book.original_title && <p className="italic text-blue-100">{book.original_title}</p>}
            <p className="text-lg font-semibold">{book.author?.name ?? "Autor desconhecido"}</p>
            {etiquetas.length > 0 && (
              <ul className="flex flex-wrap gap-2">
                {etiquetas.map((etiqueta) => (
                  <li
                    key={etiqueta}
                    className="rounded-full bg-white/15 px-3 py-1 text-xs font-medium"
                  >
                    {etiqueta}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </header>

      {/* Abaixo da faixa: sinopse e comentarios na coluna larga, ficha de
          detalhes ao lado. No celular tudo empilha: sinopse, detalhes,
          comentarios. */}
      <div className="mt-10 grid gap-x-12 gap-y-10 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <section className="lg:col-start-1">
          <h2 className="mb-3 text-lg font-bold">Sinopse</h2>
          {book.synopsis ? (
            <p className="max-w-prose whitespace-pre-line leading-relaxed text-gray-700">
              {book.synopsis}
            </p>
          ) : (
            <p className="text-sm text-gray-400">Este livro ainda não tem sinopse.</p>
          )}
        </section>

        {ficha.length > 0 && (
          <aside className="self-start rounded-2xl bg-white p-6 shadow lg:col-start-2 lg:row-span-2 lg:row-start-1">
            <h2 className="mb-2 text-lg font-bold">Detalhes</h2>
            <dl className="divide-y">
              {ficha.map((item) => (
                <div key={item.rotulo} className="flex justify-between gap-4 py-3 text-sm">
                  <dt className="text-gray-500">{item.rotulo}</dt>
                  <dd className="text-right font-medium text-gray-900">{item.valor}</dd>
                </div>
              ))}
            </dl>
          </aside>
        )}

        <section className="lg:col-start-1">
          <h2 className="mb-3 text-lg font-bold">Comentários</h2>
          {/* Proximo passo: lista de comentarios + ReviewForm no lugar deste aviso. */}
          <div className="rounded-xl border border-dashed border-gray-300 p-6 text-sm text-gray-400">
            Os comentários vão aparecer aqui.
          </div>
        </section>
      </div>
    </div>
  );
}
