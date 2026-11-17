import type { Review } from "@/types/review";

// So conta quem deu nota: review so com texto tem rating null e nao
// entra na media (o backend trata igual, COUNT(rating) e nao COUNT(id)).
export function calcularMedia(reviews: Review[]): { media: number | null; total: number } {
  const notas = reviews
    .map((r) => r.rating)
    .filter((nota): nota is number => nota !== null);

  if (notas.length === 0) return { media: null, total: 0 };

  const soma = notas.reduce((acc, nota) => acc + nota, 0);
  return { media: soma / notas.length, total: notas.length };
}

// 4.5 -> "4,5". Uma casa decimal, com virgula, como no resto da tela.
export function formatarNota(nota: number): string {
  return nota.toFixed(1).replace(".", ",");
}