"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/layout/Header";
import {
  FileText,
  FileDown,
  Target,
  Compass,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  ShieldCheck,
  FileSpreadsheet,
} from "lucide-react";
import { api } from "@/lib/api";

export default function ReportsPage() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAnalysisId, setSelectedAnalysisId] = useState<string>("");

  useEffect(() => {
    api
      .getGapHistory()
      .then((data) => {
        setHistory(data);
        if (data.length > 0) {
          setSelectedAnalysisId(data[0].id);
        }
      })
      .catch((err) => console.error("Failed to load gap history:", err))
      .finally(() => setLoading(false));

    // Also check localStorage for last ID
    if (typeof window !== "undefined") {
      const lastId = localStorage.getItem("skillsync_last_gap_id");
      if (lastId) setSelectedAnalysisId(lastId);
    }
  }, []);

  const selectedRun = history.find((h) => h.id === selectedAnalysisId) || history[0];

  return (
    <div>
      <Header
        title="Reports & Compliance Documentation"
        subtitle="Download professional PDF summaries and RFC 4180 CSV exports for talent acquisition and portfolio review"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-8">
        {/* Compliance / Standards Badge */}
        <div className="p-4 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-md bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-xs font-semibold text-[var(--foreground)]">
                Standardized Export Verification
              </h3>
              <p className="text-[11px] text-[var(--muted-text)]">
                All generated documents conform to RFC 4180 CSV specifications and PDF-1.4 vector standards with verifiable audit trails.
              </p>
            </div>
          </div>
          <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 shrink-0">
            Audit-Ready
          </span>
        </div>

        {/* Two-Column Report Showcase */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Section 1: Skill Gap & Compatibility Report */}
          <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-3">
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  <h3 className="text-sm font-semibold text-[var(--foreground)]">
                    Skill Gap & Compatibility Assessment
                  </h3>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 font-mono">
                  ReportLab Vector PDF
                </span>
              </div>

              <p className="text-xs text-[var(--muted-text)] leading-relaxed">
                Includes executive match score, multi-tier requirement coverage, transferable skill mappings, proof project milestones, and mandatory explainability disclaimers.
              </p>

              {history.length > 0 && (
                <div className="space-y-1.5">
                  <label className="text-xs text-[var(--muted-text)]">Select Assessment Snapshot:</label>
                  <select
                    value={selectedAnalysisId}
                    onChange={(e) => setSelectedAnalysisId(e.target.value)}
                    className="w-full px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
                  >
                    {history.map((run) => (
                      <option key={run.id} value={run.id}>
                        {run.candidate_name} &bull; {run.job_title} ({run.overall_score}%)
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {selectedRun && (
                <div className="p-4 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs space-y-2">
                  <div className="flex justify-between">
                    <span className="text-[var(--muted-text)]">Target Job Role:</span>
                    <span className="font-semibold text-[var(--foreground)]">{selectedRun.job_title}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--muted-text)]">Overall Match Index:</span>
                    <span className="font-mono font-bold text-blue-600 dark:text-blue-400">
                      {selectedRun.overall_score}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--muted-text)]">Mandatory Coverage:</span>
                    <span className="font-mono text-[var(--foreground)]">{selectedRun.mandatory_score}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-[var(--muted-text)]">Alignment Tier:</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                      {selectedRun.alignment_tier}
                    </span>
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center gap-3 pt-3 border-t border-[var(--surface-border)]">
              {selectedAnalysisId ? (
                <>
                  <a
                    href={api.getGapPdfUrl(selectedAnalysisId)}
                    className="flex-1 py-2 px-3 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric flex items-center justify-center gap-2 transition-colors"
                  >
                    <FileDown className="w-4 h-4" />
                    <span>Download PDF Document</span>
                  </a>
                  <a
                    href={api.getGapCsvUrl(selectedAnalysisId)}
                    className="py-2 px-3 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-semibold text-[var(--foreground)] flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <FileSpreadsheet className="w-4 h-4" />
                    <span>CSV</span>
                  </a>
                </>
              ) : (
                <div className="text-xs text-[var(--muted-text)] py-2">
                  Run a skill gap analysis first to generate downloadable reports.
                </div>
              )}
            </div>
          </div>

          {/* Section 2: Personalized Learning Roadmap Report */}
          <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-3">
                <div className="flex items-center gap-2">
                  <Compass className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                  <h3 className="text-sm font-semibold text-[var(--foreground)]">
                    Adaptive Learning Roadmap Curriculum
                  </h3>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-600 dark:text-purple-400 font-mono">
                  Weekly Plan Export
                </span>
              </div>

              <p className="text-xs text-[var(--muted-text)] leading-relaxed">
                Exports weekly milestone deliverables, hands-on proof projects, direct official documentation URLs, and progress task checklists for interview preparation.
              </p>

              <div className="p-4 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs space-y-2">
                <div className="flex justify-between">
                  <span className="text-[var(--muted-text)]">Curriculum Scope:</span>
                  <span className="font-semibold text-[var(--foreground)]">AI & Cloud Engineering</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[var(--muted-text)]">Timeline Duration:</span>
                  <span className="font-mono text-[var(--foreground)]">6 Weeks (Structured)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[var(--muted-text)]">Deliverables:</span>
                  <span className="font-mono text-[var(--foreground)]">6 Milestone Proof Projects</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[var(--muted-text)]">Format:</span>
                  <span className="text-purple-600 dark:text-purple-400 font-medium">
                    PDF Document & RFC 4180 Table
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3 pt-3 border-t border-[var(--surface-border)]">
              <a
                href={api.getRoadmapPdfUrl("default-roadmap")}
                className="flex-1 py-2 px-3 rounded-md bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <FileDown className="w-4 h-4" />
                <span>Download Roadmap PDF</span>
              </a>
              <a
                href={api.getRoadmapCsvUrl("default-roadmap")}
                className="py-2 px-3 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-semibold text-[var(--foreground)] flex items-center justify-center gap-1.5 transition-colors"
              >
                <FileSpreadsheet className="w-4 h-4" />
                <span>CSV</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
