"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/Header";
import {
  Search,
  MapPin,
  Briefcase,
  ExternalLink,
  Target,
  Sparkles,
  ClipboardPaste,
  Filter,
  CheckCircle2,
  DollarSign,
  Clock,
  Layers,
} from "lucide-react";
import { api } from "@/lib/api";
import { JobPosting } from "@/lib/types";
import { getCategoryBadgeColor } from "@/lib/utils";

export default function JobIntelligencePage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("");
  const [sourceFilter, setSourceFilter] = useState("all");

  // Manual paste form state
  const [showPasteModal, setShowPasteModal] = useState(false);
  const [pasteTitle, setPasteTitle] = useState("");
  const [pasteCompany, setPasteCompany] = useState("");
  const [pasteLocation, setPasteLocation] = useState("Remote");
  const [pasteDescription, setPasteDescription] = useState("");
  const [pasting, setPasting] = useState(false);

  // Selected job for detail modal
  const [selectedJob, setSelectedJob] = useState<JobPosting | null>(null);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await api.searchJobs(query, location, sourceFilter);
      setJobs(data);
    } catch (err) {
      console.error("Failed to fetch jobs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [sourceFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchJobs();
  };

  const handlePasteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pasteTitle || !pasteDescription) return;

    setPasting(true);
    try {
      const newJob = await api.pasteJob({
        title: pasteTitle,
        company: pasteCompany || "Custom Company",
        location: pasteLocation,
        description: pasteDescription,
      });
      setJobs([newJob, ...jobs]);
      setShowPasteModal(false);
      setPasteTitle("");
      setPasteDescription("");
      // Navigate to gap analysis with this new job
      router.push(`/gap-analysis?job_id=${newJob.id}`);
    } catch (err) {
      console.error("Failed to paste job:", err);
    } finally {
      setPasting(false);
    }
  };

  const handleAnalyzeJob = (job: JobPosting) => {
    if (typeof window !== "undefined") {
      localStorage.setItem("skillsync_selected_job", JSON.stringify(job));
    }
    router.push(`/gap-analysis?job_id=${job.id}`);
  };

  return (
    <div>
      <Header
        title="Job Intelligence & Requirements Engine"
        subtitle="Search live remote job postings or analyze custom job specifications"
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Search & Actions Bar */}
        <div className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4">
          <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-[var(--muted-text)] absolute left-3 top-3" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search job title, skills (e.g. AI Systems, Python, React, Kubernetes)..."
                className="w-full pl-9 pr-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <div className="relative md:w-56">
              <MapPin className="w-4 h-4 text-[var(--muted-text)] absolute left-3 top-3" />
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="Location (e.g. Remote, US)..."
                className="w-full pl-9 pr-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
              />
            </div>
            <button
              type="submit"
              className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric transition-colors"
            >
              Search Jobs
            </button>
            <button
              type="button"
              onClick={() => setShowPasteModal(true)}
              className="px-4 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-semibold text-[var(--foreground)] flex items-center justify-center gap-1.5 transition-colors"
            >
              <ClipboardPaste className="w-4 h-4" />
              <span>Paste Description</span>
            </button>
          </form>

          {/* Source Tabs */}
          <div className="flex items-center gap-2 pt-2 border-t border-[var(--surface-border)] overflow-x-auto text-xs">
            <span className="text-[var(--muted-text)] text-[11px] font-semibold uppercase tracking-wider mr-2">
              Source Feeds:
            </span>
            {[
              { id: "all", label: "All Opportunities" },
              { id: "curated", label: "Curated Benchmark Roles" },
              { id: "remotive", label: "Remotive Remote API" },
              { id: "arbeitnow", label: "Arbeitnow Job API" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSourceFilter(tab.id)}
                className={`px-3 py-1 rounded-md transition-colors ${
                  sourceFilter === tab.id
                    ? "bg-blue-500/10 text-blue-600 dark:text-blue-400 font-semibold border border-blue-500/20"
                    : "text-[var(--muted-text)] hover:text-[var(--foreground)]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Job Listings Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] animate-pulse space-y-3">
                <div className="h-4 bg-[var(--surface-muted)] rounded w-3/4" />
                <div className="h-3 bg-[var(--surface-muted)] rounded w-1/2" />
                <div className="h-16 bg-[var(--surface-muted)] rounded w-full" />
              </div>
            ))}
          </div>
        ) : jobs.length === 0 ? (
          <div className="p-12 text-center rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-3">
            <Briefcase className="w-8 h-8 text-[var(--muted-text)] mx-auto" />
            <h3 className="text-sm font-semibold text-[var(--foreground)]">No job descriptions matched your filters</h3>
            <p className="text-xs text-[var(--muted-text)]">
              Try adjusting your search query, or use "Paste Description" to analyze any specific job posting.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="p-5 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col justify-between hover:border-blue-500/60 transition-all space-y-4"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <h3 className="text-sm font-semibold text-[var(--foreground)] leading-snug">
                        {job.title}
                      </h3>
                      <div className="text-xs text-[var(--muted-text)] flex items-center gap-2 mt-0.5">
                        <span>{job.company}</span>
                        <span>&bull;</span>
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" /> {job.location}
                        </span>
                      </div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-[var(--surface-muted)] text-[var(--muted-text)] border border-[var(--surface-border)] shrink-0">
                      {job.source}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-[var(--muted-text)] pt-1">
                    {job.salary_range && (
                      <span className="flex items-center gap-1 font-mono">
                        <DollarSign className="w-3.5 h-3.5 text-emerald-500" />
                        {job.salary_range}
                      </span>
                    )}
                    <span className="flex items-center gap-1 font-mono">
                      <Clock className="w-3.5 h-3.5 text-purple-500" />
                      {job.required_experience_years}+ yrs exp
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Layers className="w-3.5 h-3.5 text-blue-500" />
                      {job.extracted_skills.length} skills parsed
                    </span>
                  </div>

                  {/* Top Extracted Skills Preview */}
                  <div className="flex flex-wrap gap-1.5 pt-2">
                    {job.extracted_skills.slice(0, 6).map((skill) => (
                      <span
                        key={skill.id}
                        className={`text-[10px] px-2 py-0.5 rounded border ${getCategoryBadgeColor(
                          skill.category
                        )}`}
                      >
                        {skill.name}
                        {skill.is_mandatory && " *"}
                      </span>
                    ))}
                    {job.extracted_skills.length > 6 && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-[var(--surface-muted)] text-[var(--muted-text)]">
                        +{job.extracted_skills.length - 6} more
                      </span>
                    )}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="pt-3 border-t border-[var(--surface-border)] flex items-center justify-between gap-3">
                  <button
                    onClick={() => setSelectedJob(job)}
                    className="text-xs text-[var(--muted-text)] hover:text-[var(--foreground)] underline font-medium"
                  >
                    View Specs
                  </button>
                  <button
                    onClick={() => handleAnalyzeJob(job)}
                    className="px-3.5 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-electric transition-colors"
                  >
                    <Target className="w-3.5 h-3.5" />
                    <span>Run Gap Analysis</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Modal: Paste Custom Job Description */}
        {showPasteModal && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[var(--surface)] border border-[var(--surface-border)] rounded-xl max-w-xl w-full p-6 space-y-4 shadow-elevation">
              <div className="flex items-center justify-between border-b border-[var(--surface-border)] pb-3">
                <div className="flex items-center gap-2">
                  <ClipboardPaste className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  <h3 className="text-sm font-semibold text-[var(--foreground)]">
                    Paste Raw Job Specification
                  </h3>
                </div>
                <button
                  onClick={() => setShowPasteModal(false)}
                  className="text-lg leading-none text-[var(--muted-text)] hover:text-[var(--foreground)]"
                >
                  &times;
                </button>
              </div>

              <form onSubmit={handlePasteSubmit} className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-[var(--muted-text)]">Target Job Title *</label>
                    <input
                      type="text"
                      required
                      value={pasteTitle}
                      onChange={(e) => setPasteTitle(e.target.value)}
                      placeholder="e.g. Lead AI Systems Engineer"
                      className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-[var(--muted-text)]">Company Name</label>
                    <input
                      type="text"
                      value={pasteCompany}
                      onChange={(e) => setPasteCompany(e.target.value)}
                      placeholder="e.g. DeepTech Labs"
                      className="w-full mt-1 px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[var(--muted-text)]">Job Description & Qualifications *</label>
                  <textarea
                    rows={8}
                    required
                    value={pasteDescription}
                    onChange={(e) => setPasteDescription(e.target.value)}
                    placeholder="Paste the complete job posting text here. Our Skill Extraction Agent will automatically classify mandatory vs preferred requirements..."
                    className="w-full mt-1 px-3 py-2 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)]"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-2 border-t border-[var(--surface-border)]">
                  <button
                    type="button"
                    onClick={() => setShowPasteModal(false)}
                    className="px-3.5 py-1.5 rounded-md text-xs text-[var(--muted-text)] hover:bg-[var(--surface-muted)]"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={pasting}
                    className="px-4 py-1.5 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric"
                  >
                    {pasting ? "Parsing..." : "Extract Skills & Analyze"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal: Job Detail View */}
        {selectedJob && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[var(--surface)] border border-[var(--surface-border)] rounded-xl max-w-2xl w-full p-6 space-y-4 shadow-elevation max-h-[85vh] overflow-y-auto">
              <div className="flex items-start justify-between border-b border-[var(--surface-border)] pb-3">
                <div>
                  <h3 className="text-base font-semibold text-[var(--foreground)]">
                    {selectedJob.title}
                  </h3>
                  <div className="text-xs text-[var(--muted-text)] mt-0.5">
                    {selectedJob.company} &bull; {selectedJob.location}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="text-xl leading-none text-[var(--muted-text)] hover:text-[var(--foreground)]"
                >
                  &times;
                </button>
              </div>

              <div className="space-y-3">
                <div>
                  <h4 className="text-xs font-semibold text-[var(--foreground)] mb-2">
                    Extracted Technical Requirements ({selectedJob.extracted_skills.length})
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedJob.extracted_skills.map((s) => (
                      <span
                        key={s.id}
                        className={`text-xs px-2.5 py-1 rounded-md border ${getCategoryBadgeColor(s.category)}`}
                      >
                        {s.name}
                        {s.is_mandatory ? " (Mandatory)" : " (Preferred)"}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-semibold text-[var(--foreground)] mb-1">Raw Description</h4>
                  <div className="p-3.5 rounded-md bg-[var(--surface-muted)] text-xs text-[var(--foreground)] whitespace-pre-line max-h-60 overflow-y-auto font-mono">
                    {selectedJob.description}
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-[var(--surface-border)] flex items-center justify-between">
                <button
                  onClick={() => setSelectedJob(null)}
                  className="px-3.5 py-1.5 rounded-md text-xs text-[var(--muted-text)] hover:bg-[var(--surface-muted)]"
                >
                  Close
                </button>
                <button
                  onClick={() => {
                    const j = selectedJob;
                    setSelectedJob(null);
                    handleAnalyzeJob(j);
                  }}
                  className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-electric"
                >
                  Run Gap Analysis With This Job
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
