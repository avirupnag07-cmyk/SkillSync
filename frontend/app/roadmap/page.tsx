"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { Header } from "@/components/layout/Header";
import {
  Compass,
  CheckCircle2,
  Circle,
  ExternalLink,
  BookOpen,
  Code2,
  Calendar,
  FileDown,
  Sparkles,
  Trophy,
} from "lucide-react";
import { api } from "@/lib/api";
import { LearningRoadmap, WeekPlan } from "@/lib/types";
import { getCategoryBadgeColor } from "@/lib/utils";

function RoadmapContent() {
  const searchParams = useSearchParams();
  const targetRoleParam = searchParams.get("target_role") || "Senior AI Systems Engineer";

  const [roadmap, setRoadmap] = useState<LearningRoadmap | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDuration, setSelectedDuration] = useState(6);

  const fetchRoadmap = async (duration: number) => {
    setLoading(true);
    try {
      // Check if last gap result exists in localStorage
      let missingSkills: any[] = [];
      if (typeof window !== "undefined") {
        const lastResult = localStorage.getItem("skillsync_last_gap_result");
        if (lastResult) {
          try {
            const parsed = JSON.parse(lastResult);
            missingSkills = [
              ...parsed.missing_mandatory_skills,
              ...parsed.missing_preferred_skills,
              ...parsed.partially_matched_skills,
            ];
          } catch {}
        }
      }

      // If no missing skills stored, provide default high-impact roadmap skills
      if (missingSkills.length === 0) {
        missingSkills = [
          { id: "langgraph", name: "LangGraph", category: "ai_ml", is_mandatory: true, weight: 2.2 },
          { id: "rag", name: "RAG Architectures", category: "ai_ml", is_mandatory: true, weight: 2.2 },
          { id: "vector_databases", name: "Vector Databases", category: "ai_ml", is_mandatory: true, weight: 2.0 },
          { id: "kubernetes", name: "Kubernetes (K8s)", category: "cloud_devops", is_mandatory: true, weight: 2.2 },
          { id: "terraform", name: "Terraform IaC", category: "cloud_devops", is_mandatory: false, weight: 2.0 },
          { id: "mlops", name: "MLOps & MLflow", category: "ai_ml", is_mandatory: false, weight: 2.0 },
        ];
      }

      const data = await api.generateRoadmap({
        target_role: targetRoleParam,
        duration_weeks: duration,
        missing_skills: missingSkills,
      });
      setRoadmap(data);
    } catch (err) {
      console.error("Failed to generate learning roadmap:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap(selectedDuration);
  }, [selectedDuration, targetRoleParam]);

  const handleToggleTask = async (weekNumber: number, taskId: string, currentStatus: boolean) => {
    if (!roadmap) return;

    // Optimistic UI update
    const updatedWeeks = roadmap.weeks.map((week) => {
      if (week.week_number === weekNumber) {
        return {
          ...week,
          tasks: week.tasks.map((task) =>
            task.id === taskId ? { ...task, completed: !currentStatus } : task
          ),
        };
      }
      return week;
    });

    setRoadmap({ ...roadmap, weeks: updatedWeeks });

    if (roadmap.id) {
      try {
        await api.toggleRoadmapTask(roadmap.id, weekNumber, taskId, !currentStatus);
      } catch (err) {
        console.error("Failed to update task state on backend:", err);
      }
    }
  };

  // Compute total task completion percentage
  const allTasks = roadmap?.weeks.flatMap((w) => w.tasks) || [];
  const completedTasks = allTasks.filter((t) => t.completed);
  const progressPercent = allTasks.length > 0 ? Math.round((completedTasks.length / allTasks.length) * 100) : 0;

  return (
    <div>
      <Header
        title="Personalized Learning Roadmap"
        subtitle={`Adaptive weekly upskilling curriculum targeting ${roadmap?.target_role || targetRoleParam}`}
      />

      <div className="p-8 max-w-7xl mx-auto space-y-6">
        {/* Top Progress & Configuration Bar */}
        <div className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Compass className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <h2 className="text-base font-semibold text-[var(--foreground)]">
                {roadmap?.title || "Targeted Skill Bridge Plan"}
              </h2>
            </div>
            <p className="text-xs text-[var(--muted-text)]">
              Sequenced from foundations to capstone proof-of-work project milestones.
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* Duration Selector */}
            <div className="flex items-center gap-1.5 text-xs text-[var(--muted-text)]">
              <Calendar className="w-3.5 h-3.5" />
              <span>Timeline:</span>
              <select
                value={selectedDuration}
                onChange={(e) => setSelectedDuration(parseInt(e.target.value, 10))}
                className="px-2.5 py-1 rounded border border-[var(--surface-border)] bg-[var(--surface-muted)] text-xs text-[var(--foreground)] font-medium"
              >
                <option value={4}>4 Weeks (Accelerated)</option>
                <option value={6}>6 Weeks (Standard)</option>
                <option value={8}>8 Weeks (Comprehensive)</option>
                <option value={12}>12 Weeks (Full Mastery)</option>
              </select>
            </div>

            {/* Export Actions */}
            {roadmap?.id && (
              <div className="flex items-center gap-2">
                <a
                  href={api.getRoadmapPdfUrl(roadmap.id)}
                  className="px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-medium text-[var(--foreground)] flex items-center gap-1.5 transition-colors"
                >
                  <FileDown className="w-3.5 h-3.5" /> PDF
                </a>
                <a
                  href={api.getRoadmapCsvUrl(roadmap.id)}
                  className="px-3 py-1.5 rounded-md border border-[var(--surface-border)] bg-[var(--surface-muted)] hover:bg-[var(--surface-border)] text-xs font-medium text-[var(--foreground)] flex items-center gap-1.5 transition-colors"
                >
                  <FileDown className="w-3.5 h-3.5" /> CSV
                </a>
              </div>
            )}
          </div>
        </div>

        {/* Progress Metric Card */}
        <div className="p-4 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-2">
          <div className="flex justify-between items-center text-xs">
            <span className="font-medium text-[var(--foreground)] flex items-center gap-1.5">
              <Trophy className="w-4 h-4 text-amber-500" />
              Roadmap Milestone Progress
            </span>
            <span className="font-mono text-blue-600 dark:text-blue-400 font-semibold">
              {completedTasks.length} of {allTasks.length} tasks completed ({progressPercent}%)
            </span>
          </div>
          <div className="w-full h-2 rounded-full bg-[var(--surface-muted)] overflow-hidden">
            <div
              className="h-full bg-blue-600 rounded-full transition-all duration-500"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Weekly Modules */}
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] animate-pulse space-y-3">
                <div className="h-5 bg-[var(--surface-muted)] rounded w-1/3" />
                <div className="h-4 bg-[var(--surface-muted)] rounded w-2/3" />
                <div className="h-12 bg-[var(--surface-muted)] rounded w-full" />
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {roadmap?.weeks.map((week) => (
              <div
                key={week.week_number}
                className="p-6 rounded-lg border border-[var(--surface-border)] bg-[var(--surface)] space-y-4"
              >
                {/* Week Header */}
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-[var(--surface-border)] pb-3">
                  <div className="flex items-center gap-3">
                    <span className="w-8 h-8 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center text-xs font-bold font-mono border border-blue-500/20">
                      W{week.week_number}
                    </span>
                    <div>
                      <h3 className="text-sm font-semibold text-[var(--foreground)]">
                        {week.title}
                      </h3>
                      <p className="text-xs text-[var(--muted-text)] mt-0.5">{week.goal}</p>
                    </div>
                  </div>

                  {/* Skills Badges for the week */}
                  <div className="flex flex-wrap gap-1.5">
                    {week.skills.map((s, idx) => (
                      <span
                        key={idx}
                        className={`text-[10px] px-2 py-0.5 rounded border ${getCategoryBadgeColor(s.category)}`}
                      >
                        {s.name}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Practical Milestone Project Deliverable */}
                <div className="p-3.5 rounded-lg border border-blue-500/20 bg-blue-500/5 space-y-1">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400">
                    <Code2 className="w-4 h-4" />
                    <span>Hands-On Milestone Deliverable</span>
                  </div>
                  <p className="text-xs text-[var(--foreground)] leading-relaxed font-mono">
                    {week.project_milestone}
                  </p>
                </div>

                {/* Resources & Docs */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  {week.documentation_links.length > 0 && (
                    <div className="space-y-1.5">
                      <span className="text-[11px] font-semibold text-[var(--muted-text)] flex items-center gap-1">
                        <BookOpen className="w-3.5 h-3.5 text-blue-500" /> Official Documentation
                      </span>
                      <div className="flex flex-wrap gap-2">
                        {week.documentation_links.map((link, i) => (
                          <a
                            key={i}
                            href={link}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-[11px] text-blue-600 dark:text-blue-400 hover:underline bg-[var(--surface-muted)] px-2 py-1 rounded border border-[var(--surface-border)]"
                          >
                            <span>{link.replace(/^https?:\/\//, "").split("/")[0]}</span>
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  {week.free_resources.length > 0 && (
                    <div className="space-y-1.5">
                      <span className="text-[11px] font-semibold text-[var(--muted-text)] flex items-center gap-1">
                        <Sparkles className="w-3.5 h-3.5 text-purple-500" /> Curated Free Courses & Guides
                      </span>
                      <ul className="space-y-1 text-[11px] text-[var(--foreground)]">
                        {week.free_resources.map((res, i) => (
                          <li key={i} className="flex items-center gap-1.5">
                            <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
                            <span>{res}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Action Tasks Checklist */}
                <div className="pt-2 border-t border-[var(--surface-border)] space-y-2">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-[var(--muted-text)]">
                    Progress Checklist
                  </span>
                  <div className="space-y-1.5">
                    {week.tasks.map((task) => (
                      <button
                        key={task.id}
                        onClick={() => handleToggleTask(week.week_number, task.id, task.completed)}
                        className={`w-full text-left p-2.5 rounded-md text-xs flex items-center gap-2.5 transition-colors border ${
                          task.completed
                            ? "bg-emerald-500/5 text-emerald-700 dark:text-emerald-400 border-emerald-500/20 line-through opacity-80"
                            : "bg-[var(--surface-muted)] text-[var(--foreground)] border-[var(--surface-border)] hover:border-blue-500/50"
                        }`}
                      >
                        {task.completed ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                        ) : (
                          <Circle className="w-4 h-4 text-[var(--muted-text)] shrink-0" />
                        )}
                        <span>{task.description}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function RoadmapPage() {
  return (
    <Suspense fallback={<div className="p-8 text-xs text-[var(--muted-text)]">Loading Roadmap Curriculum...</div>}>
      <RoadmapContent />
    </Suspense>
  );
}
