//tela com degradê via Tailwind(framework de css)
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-blue-700 via-blue-500 to-indigo-300">
      {children}
    </div>
  );
}