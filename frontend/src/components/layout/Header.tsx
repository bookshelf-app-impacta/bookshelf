import { Nav } from "./Nav";
import { UserBadge } from "./UserBadge";

export function Header() {
  return (
    <header className="flex items-center justify-between px-8 py-4">
      <span className="font-black text-[56px]">Bookshelf</span>
      <Nav />
      <UserBadge nome="Leticia Valença" cargo="Admin" avatarUrl="/avatarPlaceholder.png"/>
    </header>
  );
}