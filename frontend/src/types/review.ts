//uma versao ENXUTA do User (types/user.ts)
export type ReviewAuthor = {
  id: number;
  username: string;
  displayName: string | null;
  avatarUrl: string | null;
};

// Contrato PROPOSTO para a API de reviews
export type Review = {
  id: number;
  bookId: number;
  body: string | null;
  rating: number | null;
  createdAt: string;
  updatedAt: string;
  user: ReviewAuthor;
};

// Corpo de POST/PUT
export type ReviewInput = {
  body: string;
};