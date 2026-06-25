"use client";

import type { QualityReport } from "@/types/api";
import { motion } from "framer-motion";
import { PaperCard } from "./paper-card";
import { SignalCard } from "./signal-card";
import { Sparkles } from "lucide-react";

interface ReportViewProps {
  report: QualityReport;
}

export function ReportView({ report }: ReportViewProps) {
  const concerns = report.signals.filter((s) => s.severity === "concern").length;
  const warnings = report.signals.filter((s) => s.severity === "warning").length;
  const infos = report.signals.filter((s) => s.severity === "info").length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="mt-12 grid gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.1fr)]"
    >
      <PaperCard paper={report.paper} />

      <div className="min-w-0">
        <div className="glass mb-6 rounded-2xl p-6">
          <div className="mb-3 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-[var(--gold-bright)]" />
            <h3 className="font-serif text-xl font-medium text-[var(--snow)]">Quality report</h3>
          </div>
          <p className="text-sm leading-relaxed text-[var(--mist)]">{report.summary}</p>
          <div className="mt-5 flex flex-wrap gap-2">
            {report.pdf_analyzed ? (
              <span className="rounded-full border border-[color-mix(in_srgb,var(--teal)_40%,var(--ink-border))] bg-[color-mix(in_srgb,var(--teal)_10%,var(--ink))] px-3 py-1 text-xs text-[var(--teal)]">
                PDF analyzed
              </span>
            ) : null}
            <StatPill label="Signals" value={report.signals.length} />
            {concerns > 0 ? <StatPill label="Concerns" value={concerns} tone="rose" /> : null}
            {warnings > 0 ? <StatPill label="Warnings" value={warnings} tone="amber" /> : null}
            {infos > 0 ? <StatPill label="Info" value={infos} tone="teal" /> : null}
          </div>
        </div>

        <div className="space-y-4">
          {report.signals.map((signal, index) => (
            <motion.div
              key={signal.id}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 + index * 0.06, duration: 0.4 }}
            >
              <SignalCard {...signal} index={index} />
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function StatPill({
  label,
  value,
  tone = "gold",
}: {
  label: string;
  value: number;
  tone?: "gold" | "teal" | "amber" | "rose";
}) {
  const colors = {
    gold: "text-[var(--gold-bright)] border-[var(--gold-dim)]",
    teal: "text-[var(--teal)] border-[color-mix(in_srgb,var(--teal)_40%,var(--ink-border))]",
    amber: "text-[var(--amber)] border-[color-mix(in_srgb,var(--amber)_40%,var(--ink-border))]",
    rose: "text-[var(--rose)] border-[color-mix(in_srgb,var(--rose)_40%,var(--ink-border))]",
  };

  return (
    <div
      className={`rounded-full border bg-[var(--ink)] px-4 py-1.5 text-sm ${colors[tone]}`}
    >
      <span className="text-[var(--mist)]">{label}</span>{" "}
      <span className="font-medium text-[var(--snow)]">{value}</span>
    </div>
  );
}
