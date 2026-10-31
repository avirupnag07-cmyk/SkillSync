"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import {
  TrendingUp,
  BarChart3,
  PieChart as PieIcon,
  Sparkles,
  ArrowRight,
  GitCompare,
  Layers,
  Flame,
  Award,
} from "lucide-react";
import { api } from "@/lib/api";
import { MarketOverview } from "@/lib/types";
import { DemandBarChart } from "@/components/charts/DemandBarChart";
import { CategoryPieChart } from "@/components/charts/CategoryPieChart";
import { getCategoryBadgeColor } from "@/lib/utils";

export default function MarketAnalyticsPage() {
  const [market, setMarket] = useState<MarketOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [categoryFilter, setCategoryFilter] = useState("all");

  useEffect(() => {
    api
      .getMarketOverview()
      .then((data) => setMarket(data))
      .catch((err) => console.error("Failed to load market intelligence:", err))
      .finally(() => setLoading(false));
  }, []);

  const filteredSkills = market?.top_skills.filter((s) => {
    if (categoryFilter === "all") return true;
    return s.category === categoryFilter;
  }) || [];

  return (
    <div>
      <Header
        title="Market Intelligence & Technology Demand Index"
        subtitle="Cross-industry frequency distributions, salary correlations, and category shares"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Top Summary Banner */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)]">
            <div className="text-xs text-[var(--muted-text)]">Analyzed Job Postings</div>
            <div className="text-2xl font-bold font-mono text-[var(--foreground)] mt-1">
              {market?.total_jobs_analyzed || 0}
            </div>
            <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-1 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Live & Curated Feeds
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)]">
            <div className="text-xs text-[var(--muted-text)]">Unique Skills Tracked</div>
            <div className="text-2xl font-bold font-mono text-[var(--foreground)] mt-1">
              {market?.unique_skills_tracked || 0}
            </div>
            <div className="text-[11px] text-[var(--muted-text)] mt-1">
              Mapped into 8 tech categories
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)]">
            <div className="text-xs text-[var(--muted-text)]">#1 Most Requested Skill</div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1 truncate">
              {market?.top_skills[0]?.name || "Python"}
            </div>
            <div className="text-[11px] text-[var(--muted-text)] mt-1">
              {market?.top_skills[0]?.demand_percentage || 75}% market prevalence
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)]">
            <div className="text-xs text-[var(--muted-text)]">Fastest Growing Framework</div>
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">
              LangGraph
            </div>
            <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-1">
              +185% YoY requirement increase
            </div>
          </div>
        </div>

        {/* Charts Row: Bar Chart + Category Donut */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold text-[var(--foreground)]">
                  Top 10 Technical Competencies in Industry Demand
                </h3>
                <p className="text-xs text-[var(--muted-text)]">
                  Percentage of reviewed job postings requiring or preferring each skill
                </p>
              </div>
              <BarChart3 className="w-4 h-4 text-[var(--muted-text)]" />
            </div>
            {market?.top_skills ? (
              <DemandBarChart data={market.top_skills} />
            ) : (
              <div className="h-[320px] flex items-center justify-center text-xs text-[var(--muted-text)]">
                Loading charts...
              </div>
            )}
          </div>

          <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-semibold text-[var(--foreground)]">
                    Domain Distribution
                  </h3>
                  <p className="text-xs text-[var(--muted-text)]">
                    Share of skills by architectural layer
                  </p>
                </div>
                <PieIcon className="w-4 h-4 text-[var(--muted-text)]" />
              </div>
              {market?.category_distribution ? (
                <CategoryPieChart data={market.category_distribution} />
              ) : (
                <div className="h-[260px] flex items-center justify-center text-xs text-[var(--muted-text)]">
                  Loading domain shares...
                </div>
              )}
            </div>

            <Link
              href="/role-comparison"
              className="p-3 rounded-md bg-blue-500/10 hover:bg-blue-500/15 border border-blue-500/20 text-blue-600 dark:text-blue-400 text-xs font-semibold flex items-center justify-between transition-colors"
            >
              <div className="flex items-center gap-2">
                <GitCompare className="w-4 h-4" />
                <span>Compare Engineering Roles</span>
              </div>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Detailed Leaderboard Table */}
        <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-[var(--surface-border)] pb-3">
            <div>
              <h3 className="text-sm font-semibold text-[var(--foreground)]">
                Skills Demand Leaderboard
              </h3>
              <p className="text-xs text-[var(--muted-text)]">
                Ranked breakdown of technical requirements with mandatory-to-preferred ratios
              </p>
            </div>

            {/* Category Filter */}
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
            >
              <option value="all">All Domains</option>
              <option value="languages">Languages</option>
              <option value="frameworks_libraries">Frameworks</option>
              <option value="ai_ml">AI & ML</option>
              <option value="cloud_devops">Cloud & DevOps</option>
              <option value="databases_data">Databases & Data</option>
              <option value="developer_tools">Developer Tools</option>
            </select>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead>
                <tr className="border-b border-[var(--surface-border)] text-[var(--muted-text)]">
                  <th className="py-2.5 px-3 font-medium">Rank</th>
                  <th className="py-2.5 px-3 font-medium">Technology / Competency</th>
                  <th className="py-2.5 px-3 font-medium">Domain</th>
                  <th className="py-2.5 px-3 font-medium text-right">Prevalence</th>
                  <th className="py-2.5 px-3 font-medium text-right">Mandatory %</th>
                  <th className="py-2.5 px-3 font-medium text-right">Weight Factor</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--surface-border)]">
                {filteredSkills.map((skill, index) => (
                  <tr key={skill.id} className="hover:bg-[var(--surface-muted)] transition-colors">
                    <td className="py-3 px-3 font-mono text-[var(--muted-text)]">
                      #{index + 1}
                    </td>
                    <td className="py-3 px-3 font-semibold text-[var(--foreground)] flex items-center gap-2">
                      {index < 3 && <Flame className="w-3.5 h-3.5 text-amber-500" />}
                      <span>{skill.name}</span>
                    </td>
                    <td className="py-3 px-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] border ${getCategoryBadgeColor(skill.category)}`}>
                        {skill.category_name}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right font-mono font-medium text-blue-600 dark:text-blue-400">
                      {skill.demand_percentage}%
                    </td>
                    <td className="py-3 px-3 text-right font-mono text-[var(--muted-text)]">
                      {skill.mandatory_ratio}%
                    </td>
                    <td className="py-3 px-3 text-right font-mono text-[var(--muted-text)]">
                      {skill.weight.toFixed(1)}x
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
