import { HTMLAttributes, TdHTMLAttributes, ThHTMLAttributes } from "react";

export function Table({ children, ...props }: HTMLAttributes<HTMLTableElement>) {
  return (
    <div className="overflow-x-auto rounded-lg border">
      <table className="w-full text-sm text-left" {...props}>
        {children}
      </table>
    </div>
  );
}

export function TableHead({ children }: { children: React.ReactNode }) {
  return <thead className="bg-gray-50 text-gray-500">{children}</thead>;
}

export function TableBody({ children }: { children: React.ReactNode }) {
  return <tbody className="divide-y">{children}</tbody>;
}

export function TableRow({ children, ...props }: HTMLAttributes<HTMLTableRowElement>) {
  return (
    <tr className="hover:bg-gray-50" {...props}>
      {children}
    </tr>
  );
}

export function TableHeaderCell({ children, ...props }: ThHTMLAttributes<HTMLTableCellElement>) {
  return (
    <th className="px-4 py-3 font-medium" {...props}>
      {children}
    </th>
  );
}

export function TableCell({ children, ...props }: TdHTMLAttributes<HTMLTableCellElement>) {
  return (
    <td className="px-4 py-3" {...props}>
      {children}
    </td>
  );
}