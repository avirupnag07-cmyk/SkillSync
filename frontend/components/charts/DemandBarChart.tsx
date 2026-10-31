"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from "recharts";
import { RankedSkill } from "@/lib/types";

interface DemandBarChartProps {
  data: RankedSkill[];
}

export function DemandBarChart({ data }: DemandBarChartProps) {
  const chartData = data.slice(0, 10).map((s) => ({
    name: s.name,
    demand: s.demand_percentage,
    category: s.category,
    frequency: s.frequency,
  }));

  return (
    <div className="w-full h-[320px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
        >
          <XAxis
            type="number"
            domain={[0, 100]}
            unit="%"
            tick={{ fill: "currentColor", fontSize: 11 }}
            className="text-[var(--muted-text)]"
            axisLine={{ stroke: "#71717a", strokeOpacity: 0.2 }}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={{ fill: "currentColor", fontSize: 11 }}
            className="text-[var(--foreground)]"
            width={110}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            cursor={{ fill: "rgba(100, 100, 100, 0.08)" }}
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="bg-[var(--surface)] border border-[var(--surface-border)] px-3 py-2 rounded shadow-elevation text-xs">
                    <div className="font-semibold text-[var(--foreground)]">{item.name}</div>
                    <div className="text-blue-600 dark:text-blue-400 font-mono mt-0.5">
                      Demand Prevalence: {item.demand}%
                    </div>
                    <div className="text-[10px] text-[var(--muted-text)]">
                      Appears in {item.frequency} active postings
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="demand" radius={[0, 4, 4, 0]}>
            {chartData.map((_, index) => (
              <Cell
                key={`cell-${index}`}
                fill={index === 0 ? "#2563eb" : index < 3 ? "#3b82f6" : "#60a5fa"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
