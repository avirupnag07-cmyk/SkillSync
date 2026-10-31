"use client";

import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Tooltip,
} from "recharts";
import { CategoryBreakdown } from "@/lib/types";

interface SkillRadarChartProps {
  data: CategoryBreakdown[];
}

export function SkillRadarChart({ data }: SkillRadarChartProps) {
  const chartData = data.map((item) => ({
    subject: item.category_name.split("&")[0].trim(),
    score: item.score,
    fullMark: 100,
  }));

  return (
    <div className="w-full h-[280px]">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
          <PolarGrid stroke="#71717a" strokeOpacity={0.2} />
          <PolarAngleAxis
            dataKey="subject"
            tick={{ fill: "currentColor", fontSize: 10 }}
            className="text-[var(--muted-text)]"
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{ fill: "currentColor", fontSize: 9 }}
            className="text-[var(--muted-text)]"
          />
          <Radar
            name="Skill Coverage"
            dataKey="score"
            stroke="#2563eb"
            fill="#3b82f6"
            fillOpacity={0.35}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0];
                return (
                  <div className="bg-[var(--surface)] border border-[var(--surface-border)] px-2.5 py-1.5 rounded shadow-elevation text-xs">
                    <div className="font-semibold text-[var(--foreground)]">{item.payload.subject}</div>
                    <div className="text-blue-600 dark:text-blue-400 font-mono">
                      Alignment: {item.value}%
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
