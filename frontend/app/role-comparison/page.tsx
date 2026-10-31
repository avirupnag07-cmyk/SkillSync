"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/Header";
import {
  GitCompare,
  ArrowRight,
  TrendingUp,
  DollarSign,
  Sparkles,
  Layers,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import { api } from "@/lib/api";
import { RoleComparison } from "@/lib/types";
import { getCategoryBadgeColor } from "@/lib/utils";

const ROLE_OPTIONS = [
  { key: "ai_engineer", label: "AI / Machine Learning Engineer" },
  { key: "data_scientist", label: "Data Scientist" },
  { key: "data_engineer", label: "Data Engineer" },
  { key: "fullstack_engineer", label: "Full Stack Engineer" },
  { key: "devops_cloud", label: "DevOps & Cloud Engineer" },
];

export default function RoleComparisonPage() {
  const [roleA, setRoleA] = useState("ai_engineer");
  const [roleB, setRoleB] = useState("data_scientist");
  const [comparison, setComparison] = useState<RoleComparison | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchComparison = async () => {
    setLoading(true);
    try {
      const data = await api.compareRoles(roleA, roleB);
      setComparison(data);
    } catch (err) {
      console.error("Failed to compare roles:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComparison();
  }, [roleA, roleB]);

  return (
    <div>
      <Header
        title="Cross-Role Career Transition Intelligence"
        subtitle="Analyze technical overlap, unique competencies, and transition feasibility between roles"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Selector Bar */}
        <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex-1 w-full">
            <label className="text-xs text-[var(--muted-text)] font-medium">Role A (Current Track)</label>
            <select
              value={roleA}
              onChange={(e) => setRoleA(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
            >
              {ROLE_OPTIONS.map((opt) => (
                <option key={opt.key} value={opt.key}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className="p-2 rounded-full bg-[var(--surface-muted)] text-[var(--muted-text)] shrink-0 hidden md:block">
            <GitCompare className="w-5 h-5" />
          </div>

          <div className="flex-1 w-full">
            <label className="text-xs text-[var(--muted-text)] font-medium">Role B (Target Track)</label>
            <select
              value={roleB}
              onChange={(e) => setRoleB(e.target.value)}
              className="w-full mt-1 px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
            >
              {ROLE_OPTIONS.map((opt) => (
                <option key={opt.key} value={opt.key}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Comparison Telemetry Card */}
        {comparison && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-1">
              <span className="text-xs text-[var(--muted-text)]">Competency Overlap</span>
              <div className="text-2xl font-bold font-mono text-blue-600 dark:text-blue-400">
                {comparison.overlap_percentage}%
              </div>
              <p className="text-[11px] text-[var(--muted-text)]">
                {comparison.shared_skills.length} shared architectural skills
              </p>
            </div>

            <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-1">
              <span className="text-xs text-[var(--muted-text)]">Transition Delta Index</span>
              <div className="text-2xl font-bold font-mono text-purple-600 dark:text-purple-400">
                {comparison.transition_difficulty_score}%
              </div>
              <p className="text-[11px] text-[var(--muted-text)]">
                {comparison.role_b.unique_skills.length} new specialization domains to bridge
              </p>
            </div>

            <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-1">
              <span className="text-xs text-[var(--muted-text)]">Market Demand Premium</span>
              <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                {comparison.role_b.average_salary}
              </div>
              <p className="text-[11px] text-[var(--muted-text)]">
                {comparison.role_b.demand_trend} average industry growth
              </p>
            </div>
          </div>
        )}

        {/* AI Transition Recommendation */}
        {comparison && (
          <div className="p-4 rounded-lg border border-blue-500/20 bg-blue-500/5 flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
            <div className="text-xs text-[var(--foreground)] leading-relaxed">
              <span className="font-semibold">Strategic Transition Guidance: </span>
              {comparison.recommendation}
            </div>
          </div>
        )}

        {/* Venn Tri-Column Layout */}
        {comparison && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Column 1: Unique to Role A */}
            <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
              <div className="border-b border-[var(--surface-border)] pb-2.5">
                <span className="text-[10px] uppercase font-mono text-[var(--muted-text)] tracking-wider">
                  Origin Track Unique
                </span>
                <h3 className="text-sm font-semibold text-[var(--foreground)] mt-0.5">
                  Exclusive to {comparison.role_a.title} ({comparison.role_a.unique_skills.length})
                </h3>
              </div>
              <div className="space-y-2">
                {comparison.role_a.unique_skills.map((s) => (
                  <div
                    key={s.id}
                    className="p-2.5 rounded border border-[var(--surface-border)] bg-[var(--surface-muted)] flex items-center justify-between"
                  >
                    <span className="text-xs font-medium text-[var(--foreground)]">{s.name}</span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded border ${getCategoryBadgeColor(s.category)}`}>
                      {s.category_name}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Column 2: Shared Common Core Foundations */}
            <div className="p-6 rounded-lg border border-blue-500/30 bg-[var(--surface)] space-y-3 shadow-electric">
              <div className="border-b border-[var(--surface-border)] pb-2.5">
                <span className="text-[10px] uppercase font-mono text-blue-600 dark:text-blue-400 font-semibold tracking-wider">
                  Transferable Core
                </span>
                <h3 className="text-sm font-semibold text-[var(--foreground)] mt-0.5">
                  Shared Technical Foundations ({comparison.shared_skills.length})
                </h3>
              </div>
              <div className="space-y-2">
                {comparison.shared_skills.map((s) => (
                  <div
                    key={s.id}
                    className="p-2.5 rounded border border-blue-500/20 bg-blue-500/5 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                      <span className="text-xs font-semibold text-[var(--foreground)]">{s.name}</span>
                    </div>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded border ${getCategoryBadgeColor(s.category)}`}>
                      {s.category_name}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Column 3: Unique to Role B (Target Track) */}
            <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
              <div className="border-b border-[var(--surface-border)] pb-2.5">
                <span className="text-[10px] uppercase font-mono text-purple-600 dark:text-purple-400 font-semibold tracking-wider">
                  Target Specialization
                </span>
                <h3 className="text-sm font-semibold text-[var(--foreground)] mt-0.5">
                  Exclusive to {comparison.role_b.title} ({comparison.role_b.unique_skills.length})
                </h3>
              </div>
              <div className="space-y-2">
                {comparison.role_b.unique_skills.map((s) => (
                  <div
                    key={s.id}
                    className="p-2.5 rounded border border-purple-500/20 bg-purple-500/5 flex items-center justify-between"
                  >
                    <span className="text-xs font-medium text-[var(--foreground)]">{s.name}</span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded border ${getCategoryBadgeColor(s.category)}`}>
                      {s.category_name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
