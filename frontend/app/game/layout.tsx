import { TopNav } from "@/components/nav/top-nav";

export default function GameLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="h-full bg-cover bg-map">
      <TopNav />
      {children}
    </main>
  );
}
