"use client";

import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from "recharts";

interface CategoryPieChartProps {
  data: Array<{
    category_id: string;
    name: string;
    count: number;
    percentage: number;
  }>;
}

const COLORS = [
  "#2563eb", // blue
  "#7c3aed", // violet
  "#06b6d4", // cyan
  "#10b981", // emerald
  "#f59e0b", // amber
  "#ec4899", // pink
  "#64748b", // slate
  "#8b5cf6", // purple
];

export function CategoryPieChart({ data }: CategoryPieChartProps) {
  return (
    <div className="w-full h-[260px] flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={85}
            paddingAngle={3}
            dataKey="count"
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="bg-[var(--surface)] border border-[var(--surface-border)] px-2.5 py-1.5 rounded shadow-elevation text-xs">
                    <div className="font-semibold text-[var(--foreground)]">{item.name}</div>
                    <div className="text-[var(--muted-text)] font-mono">
                      {item.count} skills ({item.percentage}%)
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
