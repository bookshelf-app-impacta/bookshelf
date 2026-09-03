import { Search } from "lucide-react";

type UsersToolbarProps = {
  onAdicionar: () => void;
  onBuscar: (termo: string) => void;
};

export function UsersToolbar({ onAdicionar, onBuscar }: UsersToolbarProps) {
  return (
    <div className="flex items-center justify-end gap-4 py-4">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search..."
          onChange={(e) => onBuscar(e.target.value)}
          className="border rounded-lg pl-9 pr-4 py-2 w-64 text-sm outline-none focus:ring-2 focus:ring-blue-600"
        />
      </div>

      <button
        onClick={onAdicionar}
        className="bg-blue-700 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-blue-800"
      >
        Adicionar Usuário
      </button>
    </div>
  );
}