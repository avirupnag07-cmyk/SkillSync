"use client";

import { useEffect, useState } from "react";
import { ThemeToggle } from "./ThemeToggle";
import { api } from "@/lib/api";
import { ProviderInfo } from "@/lib/types";
import { Cpu, Github, ExternalLink, CheckCircle2 } from "lucide-react";

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  const [provider, setProvider] = useState<ProviderInfo | null>(null);

  useEffect(() => {
    api
      .getHealth()
      .then((data) => setProvider(data.active_provider))
      .catch(() => {
        setProvider({
          provider: "deterministic",
          model_name: "Deterministic Engine",
          is_local: true,
          requires_api_key: false,
          status: "active",
          badge_label: "Deterministic Engine (No API Key Required)",
          description: "Rule-based NER and ontology matching active.",
        });
      });
  }, []);

  return (
    <header className="h-14 border-b border-[var(--surface-border)] bg-[var(--surface)] px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        <h1 className="text-sm font-semibold text-[var(--foreground)] tracking-tight">
          {title || "Dashboard Overview"}
        </h1>
        {subtitle && (
          <p className="text-[11px] text-[var(--muted-text)]">{subtitle}</p>
        )}
      </div>

      <div className="flex items-center gap-3">
        {/* Transparent AI Provider Badge */}
        {provider && (
          <div
            className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] border bg-[var(--surface-muted)] border-[var(--surface-border)] text-[var(--foreground)]"
            title={provider.description}
          >
            <Cpu className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
            <span className="font-medium text-xs tracking-tight">
              {provider.badge_label}
            </span>
          </div>
        )}

        {/* Theme Toggle */}
        <ThemeToggle />

        {/* Documentation / GitHub link */}
        <a
          href="https://github.com/avirupnag07-cmyk/c-practice"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs font-medium text-[var(--muted-text)] hover:text-[var(--foreground)] hover:bg-[var(--surface-muted)] border border-[var(--surface-border)] transition-colors"
        >
          <Github className="w-3.5 h-3.5" />
          <span>Open Source</span>
        </a>
      </div>
    </header>
  );
}
