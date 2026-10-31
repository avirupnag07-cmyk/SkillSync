"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  UserCircle,
  Briefcase,
  Target,
  TrendingUp,
  Compass,
  GitCompare,
  FileText,
  Sparkles,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/profile", label: "Career Profile", icon: UserCircle },
  { href: "/jobs", label: "Job Intelligence", icon: Briefcase },
  { href: "/gap-analysis", label: "Skill Gap Analysis", icon: Target },
  { href: "/market", label: "Market Analytics", icon: TrendingUp },
  { href: "/roadmap", label: "Learning Roadmap", icon: Compass },
  { href: "/role-comparison", label: "Role Comparison", icon: GitCompare },
  { href: "/reports", label: "Reports & Exports", icon: FileText },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-[var(--surface-border)] bg-[var(--surface)] flex flex-col shrink-0 h-screen sticky top-0 select-none z-30">
      {/* Brand Header */}
      <div className="h-14 border-b border-[var(--surface-border)] flex items-center px-5 gap-3">
        <div className="w-7 h-7 rounded-md bg-blue-600 flex items-center justify-center text-white shadow-electric">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <span className="font-semibold text-sm tracking-tight text-[var(--foreground)]">
            SkillSync
          </span>
          <span className="ml-1.5 px-1.5 py-0.5 text-[10px] font-mono rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium">
            v1.0
          </span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[11px] font-semibold tracking-wider text-[var(--muted-text)] uppercase">
          Platform Modules
        </div>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition-colors",
                isActive
                  ? "bg-blue-500/10 text-blue-600 dark:text-blue-400 font-semibold"
                  : "text-[var(--muted-text)] hover:text-[var(--foreground)] hover:bg-[var(--surface-muted)]"
              )}
            >
              <div className="flex items-center gap-2.5">
                <Icon
                  className={cn(
                    "w-4 h-4 transition-colors",
                    isActive
                      ? "text-blue-600 dark:text-blue-400"
                      : "text-[var(--muted-text)] group-hover:text-[var(--foreground)]"
                  )}
                />
                <span>{item.label}</span>
              </div>
              {isActive && (
                <div className="w-1.5 h-1.5 rounded-full bg-blue-600 dark:bg-blue-400 shadow-electric" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* System Status Footnote */}
      <div className="p-3 border-t border-[var(--surface-border)]">
        <div className="p-2.5 rounded-md bg-[var(--surface-muted)] text-[11px] space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[var(--muted-text)]">Engine Status</span>
            <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Active
            </span>
          </div>
          <div className="text-[10px] text-[var(--muted-text)] truncate">
            Deterministic / LangGraph
          </div>
        </div>
      </div>
    </aside>
  );
}
