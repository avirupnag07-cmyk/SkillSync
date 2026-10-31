"use client";

import { cn } from "@/lib/utils";

interface ScoreGaugeProps {
  score: number;
  mandatoryScore: number;
  preferredScore: number;
  experienceScore: number;
  tier: string;
}

export function ScoreGauge({
  score,
  mandatoryScore,
  preferredScore,
  experienceScore,
  tier,
}: ScoreGaugeProps) {
  // SVG stroke-dasharray calculation for 100-point circle (radius = 42, circumference = ~264)
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getTierColor = (s: number) => {
    if (s >= 85) return "text-emerald-600 dark:text-emerald-400 stroke-emerald-500";
    if (s >= 70) return "text-blue-600 dark:text-blue-400 stroke-blue-600";
    if (s >= 50) return "text-amber-600 dark:text-amber-400 stroke-amber-500";
    return "text-rose-600 dark:text-rose-400 stroke-rose-500";
  };

  const tierColor = getTierColor(score);

  return (
    <div className="flex flex-col items-center">
      {/* Circular Progress Gauge */}
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background Track */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            className="stroke-[var(--surface-muted)]"
            strokeWidth="9"
            fill="transparent"
          />
          {/* Value Arc */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            className={cn("transition-all duration-1000 ease-out", tierColor)}
            strokeWidth="9"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>

        {/* Center Score Display */}
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-bold tracking-tight text-[var(--foreground)] font-mono">
            {Math.round(score)}%
          </span>
          <span className="text-[10px] text-[var(--muted-text)] uppercase font-semibold tracking-wider">
            Match Index
          </span>
        </div>
      </div>

      {/* Alignment Tier Badge */}
      <div className="mt-3 text-center">
        <span
          className={cn(
            "inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold border",
            score >= 70
              ? "bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20"
              : score >= 50
              ? "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20"
              : "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20"
          )}
        >
          {tier}
        </span>
      </div>

      {/* Subcomponent Alignment Factors */}
      <div className="w-full mt-5 space-y-2.5 pt-4 border-t border-[var(--surface-border)]">
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-[var(--muted-text)]">Mandatory Requirements (60%)</span>
            <span className="font-mono font-medium">{Math.round(mandatoryScore)}%</span>
          </div>
          <div className="w-full h-1.5 rounded-full bg-[var(--surface-muted)] overflow-hidden">
            <div
              className="h-full bg-blue-600 rounded-full transition-all duration-700"
              style={{ width: `${mandatoryScore}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-[var(--muted-text)]">Preferred / Bonus (25%)</span>
            <span className="font-mono font-medium">{Math.round(preferredScore)}%</span>
          </div>
          <div className="w-full h-1.5 rounded-full bg-[var(--surface-muted)] overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full transition-all duration-700"
              style={{ width: `${preferredScore}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-[var(--muted-text)]">Experience Alignment (15%)</span>
            <span className="font-mono font-medium">{Math.round(experienceScore)}%</span>
          </div>
          <div className="w-full h-1.5 rounded-full bg-[var(--surface-muted)] overflow-hidden">
            <div
              className="h-full bg-purple-500 rounded-full transition-all duration-700"
              style={{ width: `${experienceScore}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
