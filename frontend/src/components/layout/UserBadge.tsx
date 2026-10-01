import Image from "next/image";
import Link from "next/link";
import type { User } from "@/types/user";

type UserBadgeProps = {
  user: User;
  onLogout: () => void;
};

export function UserBadge({ user, onLogout }: UserBadgeProps) {
  const nome = user.displayName ?? user.username;
  const isAdmin = user.role === "admin";
  const cargo = user.role === "admin" ? "Admin" : "Usuário";

  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="font-semibold leading-tight">{nome}</p>
        {
          isAdmin ? (
            <Link
            href="/admin/usuarios"
            className="text-blue-600 text-sm leading-tight hover:underline"
          >
            {cargo}
          </Link>
        ) : (
          <p className="text-blue-600 text-sm leading-tight">{cargo}</p>
        )
        }
      </div>

      {user.avatarUrl ? (
        <Image
          src={user.avatarUrl}
          alt={nome}
          width={40}
          height={40}
          className="rounded-full object-cover"
        />
      ) : (
        <div className="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 text-sm font-semibold">
          {nome.charAt(0).toUpperCase()}
        </div>
      )}

      <button onClick={onLogout} className="text-xs text-gray-400 hover:text-gray-600 hover:underline">
        Sair
      </button>
    </div>
  );
}
