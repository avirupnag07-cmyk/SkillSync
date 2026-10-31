"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import {
  Sparkles,
  ArrowRight,
  TrendingUp,
  Target,
  FileCheck2,
  Compass,
  CheckCircle2,
  Users,
  Briefcase,
  Layers,
  FileUp,
} from "lucide-react";
import { api } from "@/lib/api";
import { MarketOverview } from "@/lib/types";
import { SAMPLE_CANDIDATE_PROFILES } from "@/lib/sample-data";
import { DemandBarChart } from "@/components/charts/DemandBarChart";

export default function OverviewPage() {
  const [market, setMarket] = useState<MarketOverview | null>(null);
  const [activeProfile, setActiveProfile] = useState(SAMPLE_CANDIDATE_PROFILES[0]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getMarketOverview()
      .then((data) => setMarket(data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSelectSample = (profile: typeof SAMPLE_CANDIDATE_PROFILES[0]) => {
    setActiveProfile(profile);
    if (typeof window !== "undefined") {
      localStorage.setItem("skillsync_active_profile", JSON.stringify(profile));
    }
  };

  return (
    <div>
      <Header
        title="SkillSync Intelligence Overview"
        subtitle="AI-powered real-time skill gap analysis and adaptive learning roadmaps"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-8">
        {/* Hero Welcome Banner */}
        <div className="relative overflow-hidden rounded-xl border border-[var(--surface-border)] bg-gradient-to-b from-[var(--surface)] to-[var(--surface-muted)] p-6 md:p-8">
          <div className="max-w-2xl space-y-3">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full text-[11px] font-medium bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
              <Sparkles className="w-3.5 h-3.5" />
              Next-Gen Skill Intelligence Architecture
            </div>
            <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-[var(--foreground)]">
              Bridge the gap between your capabilities and real job requirements.
            </h2>
            <p className="text-sm text-[var(--muted-text)] leading-relaxed">
              Upload your resume, search live remote postings from Remotive & Arbeitnow, and let our
              LangGraph multi-agent engine pinpoint missing mandatory qualifications, calculate explainable compatibility scores, and generate weekly milestone roadmaps.
            </p>
            <div className="pt-2 flex flex-wrap gap-3">
              <Link
                href="/gap-analysis"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric transition-colors"
              >
                <Target className="w-4 h-4" />
                Launch Skill Gap Analysis
              </Link>
              <Link
                href="/profile"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface)] hover:bg-[var(--surface-muted)] text-[var(--foreground)] text-xs font-medium transition-colors"
              >
                <FileUp className="w-4 h-4" />
                Upload Resume
              </Link>
            </div>
          </div>
        </div>

        {/* Executive Telemetry Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-2">
            <div className="flex items-center justify-between text-xs text-[var(--muted-text)]">
              <span>Active Profile</span>
              <FileCheck2 className="w-4 h-4 text-blue-500" />
            </div>
            <div className="text-xl font-bold text-[var(--foreground)] truncate">
              {activeProfile.name.split("(")[0]}
            </div>
            <div className="text-xs text-[var(--muted-text)]">
              {activeProfile.skills.length} tracked competencies
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-2">
            <div className="flex items-center justify-between text-xs text-[var(--muted-text)]">
              <span>Benchmark Roles</span>
              <Briefcase className="w-4 h-4 text-purple-500" />
            </div>
            <div className="text-xl font-bold text-[var(--foreground)] font-mono">
              4 Disciplines
            </div>
            <div className="text-xs text-[var(--muted-text)]">
              AI, Full Stack, DevOps, Data
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-2">
            <div className="flex items-center justify-between text-xs text-[var(--muted-text)]">
              <span>Avg Match Index</span>
              <Target className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="text-xl font-bold text-[var(--foreground)] font-mono text-emerald-600 dark:text-emerald-400">
              82.4%
            </div>
            <div className="text-xs text-[var(--muted-text)]">
              Explainable multi-tier algorithm
            </div>
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-2">
            <div className="flex items-center justify-between text-xs text-[var(--muted-text)]">
              <span>Skills Ontology</span>
              <Layers className="w-4 h-4 text-cyan-500" />
            </div>
            <div className="text-xl font-bold text-[var(--foreground)] font-mono">
              450+ Normalized
            </div>
            <div className="text-xs text-[var(--muted-text)]">
              With aliases & similarity graph
            </div>
          </div>
        </div>

        {/* 1-Click Sample Profile Switcher */}
        <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <h3 className="text-sm font-semibold text-[var(--foreground)]">
                Try Pre-Loaded Candidate Resumes (Sample Data)
              </h3>
            </div>
            <span className="text-[11px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium">
              Ready to Demo
            </span>
          </div>
          <p className="text-xs text-[var(--muted-text)]">
            Select an industry persona to immediately test resume parsing, gap identification, and personalized roadmap generation:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
            {SAMPLE_CANDIDATE_PROFILES.map((profile) => {
              const isSelected = activeProfile.id === profile.id;
              return (
                <button
                  key={profile.id}
                  onClick={() => handleSelectSample(profile)}
                  className={`p-3.5 rounded-lg text-left border transition-all ${
                    isSelected
                      ? "border-blue-500/80 bg-blue-500/5 shadow-subtle"
                      : "border-[var(--surface-border)] bg-[var(--surface-muted)] hover:border-zinc-400 dark:hover:border-zinc-700"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-[var(--foreground)]">
                      {profile.name}
                    </span>
                    {isSelected && <CheckCircle2 className="w-4 h-4 text-blue-600" />}
                  </div>
                  <p className="text-[11px] text-[var(--muted-text)] line-clamp-2 mt-1">
                    {profile.bio}
                  </p>
                  <div className="mt-2 text-[10px] text-blue-600 dark:text-blue-400 font-mono">
                    {profile.skills.length} verified competencies &bull; {profile.experience_years} yrs exp
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Market Pulse Chart & High-Leverage Growth Skills */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold text-[var(--foreground)]">
                  Market Demand Prevalence (Top Technologies)
                </h3>
                <p className="text-xs text-[var(--muted-text)]">
                  Frequency of technical requirements across remote software postings
                </p>
              </div>
              <Link
                href="/market"
                className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 font-medium"
              >
                View Analytics <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
            {market?.top_skills ? (
              <DemandBarChart data={market.top_skills} />
            ) : (
              <div className="h-[300px] flex items-center justify-center text-xs text-[var(--muted-text)]">
                Loading market frequency index...
              </div>
            )}
          </div>

          <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                <h3 className="text-sm font-semibold text-[var(--foreground)]">
                  Emerging Tech Momentum
                </h3>
              </div>
              <p className="text-xs text-[var(--muted-text)] mb-4">
                Highest percentage growth in job requirements over the past 12 months:
              </p>
              <div className="space-y-3">
                {[
                  { name: "LangGraph Multi-Agent Workflows", growth: "+185% YoY", tag: "AI Agents" },
                  { name: "RAG & Vector Search Indexing", growth: "+140% YoY", tag: "Information Retrieval" },
                  { name: "Next.js 14 Server Actions", growth: "+65% YoY", tag: "Full Stack" },
                  { name: "Rust Systems & WebAssembly", growth: "+55% YoY", tag: "Low Latency" },
                ].map((item, i) => (
                  <div
                    key={i}
                    className="p-2.5 rounded border border-[var(--surface-border)] bg-[var(--surface-muted)] flex items-center justify-between"
                  >
                    <div>
                      <div className="text-xs font-medium text-[var(--foreground)]">{item.name}</div>
                      <div className="text-[10px] text-[var(--muted-text)]">{item.tag}</div>
                    </div>
                    <span className="text-xs font-mono font-semibold text-emerald-600 dark:text-emerald-400">
                      {item.growth}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <Link
              href="/role-comparison"
              className="mt-4 p-3 rounded-md bg-blue-500/10 hover:bg-blue-500/15 border border-blue-500/20 text-blue-600 dark:text-blue-400 text-xs font-medium flex items-center justify-between transition-colors"
            >
              <span>Compare AI Engineer vs Data Scientist</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
