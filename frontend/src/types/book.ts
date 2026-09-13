export type BookAuthor = {
  id: number;
  name: string;
  slug: string;
};

export type BookGenre = {
  id: number;
  name: string;
  slug: string;
};

// Espelha o book_to_dict do backend (backend/app/schemas/book_schema.py) —
// por isso snake_case aqui, diferente do types/user.ts.
export type Book = {
  id: number;
  title: string;
  original_title: string | null;
  slug: string;
  release_year: number | null;
  synopsis: string | null;
  cover_url: string | null;
  isbn13: string | null;
  publisher: string | null;
  page_count: number | null;
  language: string | null;
  author: BookAuthor | null;
  genre: BookGenre | null;
};

// Campos aceitos por POST/PUT /api/books — ver validate_book_create no backend.
export type BookInput = {
  title: string;
  original_title?: string | null;
  release_year?: number | null;
  synopsis?: string | null;
  cover_url?: string | null;
  isbn13?: string | null;
  publisher?: string | null;
  page_count?: number | null;
  language?: string | null;
  author?: string | null;
  genre_id?: number | null;
};
