import Image from "next/image";

type UserBadgeProps = {
  nome: string;
  cargo: string;
  avatarUrl: string;
};

export function UserBadge({ nome, cargo, avatarUrl }: UserBadgeProps) {
  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="font-semibold leading-tight">{nome}</p>
        <p className="text-blue-600 text-sm leading-tight">{cargo}</p>
      </div>
      <Image
        src={avatarUrl}
        alt={nome}
        width={40}
        height={40}
        className="rounded-full object-cover"
      />
    </div>
  );
}