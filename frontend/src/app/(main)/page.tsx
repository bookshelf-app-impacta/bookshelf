import { listBooks } from "@/lib/api/books";
import { BookGrid } from "@/components/features/book/BookGrid";

// Home — antes disso aqui era so o boilerplate padrao do create-next-app
// (logo do Next, links pra documentacao). Movido pra dentro de (main)
// pra ganhar o Header; nao da pra ter um app/page.tsx (fora de grupo)
// e um app/(main)/page.tsx ao mesmo tempo, os dois resolvem pra "/".
export default async function HomePage() {
  const books = await listBooks();

  return (
    <div className="px-8 py-6">
      <BookGrid initialBooks={books} />
    </div>
  );
}
