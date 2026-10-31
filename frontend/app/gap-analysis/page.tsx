"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import {
  Target,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  ArrowRight,
  FileDown,
  Layers,
  Cpu,
  ShieldAlert,
  Compass,
} from "lucide-react";
import { api } from "@/lib/api";
import { GapAnalysisResult, JobPosting, CandidateProfile } from "@/lib/types";
import { SAMPLE_CANDIDATE_PROFILES } from "@/lib/sample-data";
import { ScoreGauge } from "@/components/charts/ScoreGauge";
import { SkillRadarChart } from "@/components/charts/SkillRadarChart";
import { getCategoryBadgeColor } from "@/lib/utils";

function GapAnalysisContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const jobIdParam = searchParams.get("job_id");

  const [profiles] = useState<CandidateProfile[]>(SAMPLE_CANDIDATE_PROFILES);
  const [selectedProfile, setSelectedProfile] = useState<CandidateProfile>(SAMPLE_CANDIDATE_PROFILES[0]);
  const [benchmarkJobs, setBenchmarkJobs] = useState<JobPosting[]>([]);
  const [selectedJob, setSelectedJob] = useState<JobPosting | null>(null);

  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load benchmark jobs on mount
  useEffect(() => {
    api
      .getBenchmarkJobs()
      .then((jobs) => {
        setBenchmarkJobs(jobs);
        if (jobIdParam) {
          const match = jobs.find((j) => j.id === jobIdParam);
          if (match) setSelectedJob(match);
        } else if (jobs.length > 0) {
          setSelectedJob(jobs[0]);
        }
      })
      .catch((err) => console.error("Error loading benchmark jobs:", err));

    // Check stored active profile
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("skillsync_active_profile");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          setSelectedProfile(parsed);
        } catch {}
      }
    }
  }, [jobIdParam]);

  const handleRunAnalysis = async () => {
    if (!selectedJob) return;

    setAnalyzing(true);
    setError(null);
    try {
      const data = await api.analyzeGap({
        candidate_skills: selectedProfile.skills,
        candidate_experience_years: selectedProfile.experience_years,
        required_experience_years: selectedJob.required_experience_years,
        raw_job_description: selectedJob.description,
        job_title: selectedJob.title,
        job_id: selectedJob.id,
      });
      setResult(data);
      if (typeof window !== "undefined" && data.id) {
        localStorage.setItem("skillsync_last_gap_id", data.id);
        localStorage.setItem("skillsync_last_gap_result", JSON.stringify(data));
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to calculate skill gap analysis.");
    } finally {
      setAnalyzing(false);
    }
  };

  // Run automatically if target job loaded and no result yet
  useEffect(() => {
    if (selectedJob && !result && !analyzing) {
      handleRunAnalysis();
    }
  }, [selectedJob]);

  const handleGenerateRoadmap = () => {
    if (result) {
      router.push(`/roadmap?target_role=${encodeURIComponent(selectedJob?.title || "Engineering Role")}`);
    }
  };

  return (
    <div>
      <Header
        title="Skill Gap Intelligence & Career Compatibility"
        subtitle="Explainable semantic matching, tier classification, and multi-factor competency mapping"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Selector Header Bar */}
        <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          <div>
            <label className="text-xs text-[var(--muted-text)] font-medium">Candidate Profile</label>
            <select
              value={selectedProfile.id}
              onChange={(e) => {
                const found = profiles.find((p) => p.id === e.target.value) || selectedProfile;
                setSelectedProfile(found);
                localStorage.setItem("skillsync_active_profile", JSON.stringify(found));
              }}
              className="w-full mt-1 px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
            >
              {profiles.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.skills.length} skills, {p.experience_years} yrs)
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs text-[var(--muted-text)] font-medium">Target Job Specification</label>
            <select
              value={selectedJob?.id || ""}
              onChange={(e) => {
                const match = benchmarkJobs.find((j) => j.id === e.target.value);
                if (match) setSelectedJob(match);
              }}
              className="w-full mt-1 px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
            >
              {benchmarkJobs.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.title} &bull; {j.company} ({j.required_experience_years} yrs exp)
                </option>
              ))}
            </select>
          </div>

          <div>
            <button
              onClick={handleRunAnalysis}
              disabled={analyzing}
              className="w-full py-2 px-4 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric flex items-center justify-center gap-2 transition-colors"
            >
              <Target className="w-4 h-4" />
              <span>{analyzing ? "Running LangGraph Agents..." : "Recalculate Gap Analysis"}</span>
            </button>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-xs text-red-600 dark:text-red-400">
            {error}
          </div>
        )}

        {/* Results Showcase */}
        {result && (
          <div className="space-y-6">
            {/* Top Analysis Metrics: Score Gauge + Radar + Executive Summary */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Score Gauge Card */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between">
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--muted-text)] mb-2">
                    Compatibility Index
                  </h3>
                  <ScoreGauge
                    score={result.overall_score}
                    mandatoryScore={result.mandatory_score}
                    preferredScore={result.preferred_score}
                    experienceScore={result.experience_score}
                    tier={result.alignment_tier}
                  />
                </div>
              </div>

              {/* Domain Radar Coverage */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between">
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-[var(--muted-text)] mb-1">
                    Domain Competency Balance
                  </h3>
                  <p className="text-[11px] text-[var(--muted-text)] mb-3">
                    Normalized requirement coverage across 8 technical dimensions:
                  </p>
                  <SkillRadarChart data={result.category_breakdown} />
                </div>
              </div>

              {/* Executive Summary & Quick Action Card */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-xs font-semibold text-[var(--foreground)]">
                    <Sparkles className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                    <span>Agent Executive Rationale</span>
                  </div>
                  <p className="text-xs text-[var(--foreground)] leading-relaxed bg-[var(--surface-muted)] p-3.5 rounded-md border border-[var(--surface-border)]">
                    {result.executive_summary}
                  </p>

                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="p-2.5 rounded bg-[var(--surface-muted)] border border-[var(--surface-border)]">
                      <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                        {result.matched_skills.length}
                      </div>
                      <div className="text-[10px] text-[var(--muted-text)]">Matched Directly</div>
                    </div>
                    <div className="p-2.5 rounded bg-[var(--surface-muted)] border border-[var(--surface-border)]">
                      <div className="text-lg font-bold text-blue-600 dark:text-blue-400 font-mono">
                        {result.partially_matched_skills.length}
                      </div>
                      <div className="text-[10px] text-[var(--muted-text)]">Transferable</div>
                    </div>
                    <div className="p-2.5 rounded bg-[var(--surface-muted)] border border-[var(--surface-border)]">
                      <div className="text-lg font-bold text-rose-600 dark:text-rose-400 font-mono">
                        {result.missing_mandatory_skills.length}
                      </div>
                      <div className="text-[10px] text-[var(--muted-text)]">Missing Mandatory</div>
                    </div>
                    <div className="p-2.5 rounded bg-[var(--surface-muted)] border border-[var(--surface-border)]">
                      <div className="text-lg font-bold text-amber-600 dark:text-amber-400 font-mono">
                        {result.missing_preferred_skills.length}
                      </div>
                      <div className="text-[10px] text-[var(--muted-text)]">Missing Preferred</div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2 pt-2 border-t border-[var(--surface-border)]">
                  <button
                    onClick={handleGenerateRoadmap}
                    className="w-full py-2 px-3 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <Compass className="w-4 h-4" />
                    <span>Generate Personalized Learning Roadmap</span>
                  </button>
                  <div className="flex gap-2">
                    {result.id && (
                      <>
                        <a
                          href={api.getGapPdfUrl(result.id)}
                          className="flex-1 py-1.5 px-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-center text-xs font-medium text-[var(--foreground)] flex items-center justify-center gap-1 transition-colors"
                        >
                          <FileDown className="w-3.5 h-3.5" /> PDF
                        </a>
                        <a
                          href={api.getGapCsvUrl(result.id)}
                          className="flex-1 py-1.5 px-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-center text-xs font-medium text-[var(--foreground)] flex items-center justify-center gap-1 transition-colors"
                        >
                          <FileDown className="w-3.5 h-3.5" /> CSV
                        </a>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Categorized Gap Analysis Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Missing Mandatory Skills (High Impact Gaps) */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
                <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-2.5">
                  <div className="flex items-center gap-2">
                    <XCircle className="w-4 h-4 text-rose-500" />
                    <h3 className="text-sm font-semibold text-[var(--foreground)]">
                      Missing Mandatory Skills ({result.missing_mandatory_skills.length})
                    </h3>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-rose-500/10 text-rose-600 dark:text-rose-400 font-medium">
                    Highest Priority
                  </span>
                </div>

                {result.missing_mandatory_skills.length === 0 ? (
                  <div className="p-4 text-center text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                    All mandatory job specifications are satisfied!
                  </div>
                ) : (
                  <div className="space-y-2.5">
                    {result.missing_mandatory_skills.map((skill) => (
                      <div
                        key={skill.id}
                        className="p-3 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-muted)] space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-[var(--foreground)]">{skill.name}</span>
                          <span className={`text-[10px] px-2 py-0.5 rounded border ${getCategoryBadgeColor(skill.category)}`}>
                            {skill.category_name || skill.category}
                          </span>
                        </div>
                        {skill.project_idea && (
                          <p className="text-[11px] text-[var(--muted-text)]">
                            <span className="font-medium text-[var(--foreground)]">Proof Project:</span> {skill.project_idea}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Partially Matched / Transferable Competencies */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
                <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-2.5">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-blue-500" />
                    <h3 className="text-sm font-semibold text-[var(--foreground)]">
                      Transferable Skills ({result.partially_matched_skills.length})
                    </h3>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium">
                    Semantic Transfer
                  </span>
                </div>

                {result.partially_matched_skills.length === 0 ? (
                  <div className="p-4 text-center text-xs text-[var(--muted-text)]">
                    No related transferable substitutions identified.
                  </div>
                ) : (
                  <div className="space-y-2.5">
                    {result.partially_matched_skills.map((skill) => (
                      <div
                        key={skill.id}
                        className="p-3 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-muted)] space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-[var(--foreground)]">{skill.name}</span>
                          <span className="text-[10px] text-blue-600 dark:text-blue-400 font-mono font-medium">
                            {Math.round((skill.similarity || 0.7) * 100)}% Transferable
                          </span>
                        </div>
                        <p className="text-[11px] text-[var(--muted-text)]">
                          Bridged via candidate's demonstrated capability in{" "}
                          <span className="font-semibold text-[var(--foreground)]">{skill.transferable_skill}</span>.
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Matched Direct Skills */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
                <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-2.5">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    <h3 className="text-sm font-semibold text-[var(--foreground)]">
                      Matched Qualifications ({result.matched_skills.length})
                    </h3>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-medium">
                    Verified Fit
                  </span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {result.matched_skills.map((skill) => (
                    <span
                      key={skill.id}
                      className="px-2.5 py-1 rounded text-xs font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20"
                    >
                      {skill.name}
                    </span>
                  ))}
                </div>
              </div>

              {/* Missing Preferred Skills (Bonus) */}
              <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
                <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-2.5">
                  <div className="flex items-center gap-2">
                    <HelpCircle className="w-4 h-4 text-amber-500" />
                    <h3 className="text-sm font-semibold text-[var(--foreground)]">
                      Missing Preferred / Bonus ({result.missing_preferred_skills.length})
                    </h3>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400 font-medium">
                    Secondary Priority
                  </span>
                </div>

                <div className="flex flex-wrap gap-2">
                  {result.missing_preferred_skills.map((skill) => (
                    <span
                      key={skill.id}
                      className="px-2.5 py-1 rounded text-xs font-medium bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/20"
                    >
                      {skill.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Mandatory Disclaimer */}
            <div className="p-4 rounded-lg border border-[var(--surface-border)] bg-[var(--surface-muted)] flex items-start gap-3">
              <ShieldAlert className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
              <div className="text-xs text-[var(--muted-text)] leading-relaxed">
                <span className="font-semibold text-[var(--foreground)]">Career Advisory Notice: </span>
                {result.disclaimer}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GapAnalysisPage() {
  return (
    <Suspense fallback={<div className="p-8 text-xs text-[var(--muted-text)]">Loading Gap Analysis Workspace...</div>}>
      <GapAnalysisContent />
    </Suspense>
  );
}
