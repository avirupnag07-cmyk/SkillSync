import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "SkillSync - AI Skill Gap Intelligence Platform",
  description:
    "Production-grade AI skill gap intelligence platform comparing resumes against live job requirements with explainable scoring and adaptive roadmaps.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[var(--background)] text-[var(--foreground)] antialiased flex">
        {/* Main Navigation Sidebar */}
        <Sidebar />

        {/* Dynamic Main Workspace */}
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto h-screen">
          <main className="flex-1 pb-16">{children}</main>
        </div>
      </body>
    </html>
  );
}
