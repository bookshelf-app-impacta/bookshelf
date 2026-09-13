import { BookForm } from "@/components/features/book/BookForm";
import { RequireAdmin } from "@/components/auth/RequireAdmin";

export default function NovoLivroPage() {
  return (
    <RequireAdmin>
      <div className="px-8 py-6 flex flex-col items-start">
        <h1 className="text-2xl font-black mb-6">Cadastrar livro</h1>
        <BookForm />
      </div>
    </RequireAdmin>
  );
}
