export type UserRole = "user" | "admin";

export type User = {
  id: number;
  username: string;
  email: string;
  displayName?: string;
  avatarUrl?: string;
  role: UserRole;
  isActive: boolean;
};