import Image from "next/image";
import { Pencil, Trash2 } from "lucide-react";//icones
import { Table, TableHead, TableBody, TableRow, TableHeaderCell, TableCell } from "@/components/ui/Table";//ui ta tabela
import { User } from "@/types/user";//importa o molde do objeto

//cria um molde para a função
type UserTableProps = {
  users: User[];
  onEdit: (user: User) => void;
  onDelete: (user: User) => void;
  onToggleActive: (user: User) => void; 
};

//retorna um html
export function UserTable({ users, onEdit, onDelete, onToggleActive}: UserTableProps) {
  return (
    <Table>
      <TableHead>
        <tr>
          <TableHeaderCell></TableHeaderCell>
          <TableHeaderCell>Nome</TableHeaderCell>
          <TableHeaderCell>Username</TableHeaderCell>
          <TableHeaderCell>E-mail</TableHeaderCell>
          <TableHeaderCell>Tipo de Conta</TableHeaderCell>
          <TableHeaderCell>Status</TableHeaderCell>
          <TableHeaderCell></TableHeaderCell>
        </tr>
      </TableHead>
      <TableBody>
        {users.map((user) => (
          <TableRow key={user.id}>
            <TableCell>
              {user.avatarUrl ? (
                <Image
                  src={user.avatarUrl}
                  alt={user.displayName ?? user.username}
                  width={32}
                  height={32}
                  className="rounded-full object-cover"
                />
              ) : (
                <div className="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 text-xs">
                  {(user.displayName ?? user.username).charAt(0).toUpperCase()}
                </div>
              )}
            </TableCell>
            <TableCell>{user.displayName ?? "—"}</TableCell>
            <TableCell>@{user.username}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <span
                className={`text-xs font-semibold px-2 py-1 rounded-full ${
                  user.role === "admin" ? "bg-blue-100 text-blue-700" : "bg-gray-100 text-gray-600"
                }`}
              >
                {user.role === "admin" ? "Admin" : "Usuário"}
              </span>
            </TableCell>
            <TableCell>
              <button
                onClick={() => onToggleActive(user)}
                className={`text-xs font-semibold px-2 py-1 rounded-full ${
                  user.isActive
                    ? "bg-green-100 text-green-700"
                    : "bg-gray-100 text-gray-500"
                }`}
              >
                {user.isActive ? "Ativo" : "Inativo"}
              </button>
            </TableCell>
            <TableCell>
              <div className="flex gap-3">
                <button onClick={() => onEdit(user)} className="text-blue-600">
                  <Pencil className="h-4 w-4" />
                </button>
                <button onClick={() => onDelete(user)} className="text-blue-600">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}