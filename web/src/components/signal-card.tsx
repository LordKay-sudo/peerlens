"use client";

import type { SignalSeverity } from "@/types/api";
import { cn } from "@/lib/utils";
import { AlertTriangle, AlertCircle, Info } from "lucide-react";

const severityConfig: Record<
  SignalSeverity,
  { label: string; icon: typeof Info; className: string; dot: string }
> = {
  info: {
    label: "Info",
    icon: Info,
    className: "border-[color-mix(in_srgb,var(--teal)_35%,var(--ink-border))] bg-[color-mix(in_srgb,var(--teal)_8%,var(--ink-surface))]",
    dot: "bg-[var(--teal)] shadow-[0_0_10px_var(--teal)]",
  },
  warning: {
    label: "Warning",
    icon: AlertTriangle,
    className: "border-[color-mix(in_srgb,var(--amber)_35%,var(--ink-border))] bg-[color-mix(in_srgb,var(--amber)_8%,var(--ink-surface))]",
    dot: "bg-[var(--amber)] shadow-[0_0_10px_var(--amber)]",
  },
  concern: {
    label: "Concern",
    icon: AlertCircle,
    className: "border-[color-mix(in_srgb,var(--rose)_35%,var(--ink-border))] bg-[color-mix(in_srgb,var(--rose)_8%,var(--ink-surface))]",
    dot: "bg-[var(--rose)] shadow-[0_0_10px_var(--rose)]",
  },
};

interface SignalCardProps {
  name: string;
  severity: SignalSeverity;
  message: string;
  evidence?: string | null;
  dimension: string;
  index: number;
}

export function SignalCard({
  name,
  severity,
  message,
  evidence,
  dimension,
  index,
}: SignalCardProps) {
  const config = severityConfig[severity];
  const Icon = config.icon;

  return (
    <article
      className={cn(
        "group rounded-2xl border p-5 transition duration-300 hover:-translate-y-0.5 hover:shadow-lg",
        config.className,
      )}
      style={{ animationDelay: `${index * 80}ms` }}
    >
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <span className={cn("h-2 w-2 rounded-full", config.dot)} />
          <h4 className="font-medium text-[var(--snow)]">{name}</h4>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-[var(--ink)] px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-[var(--mist)]">
            {dimension}
          </span>
          <span className="flex items-center gap-1 text-xs text-[var(--mist)]">
            <Icon className="h-3.5 w-3.5" />
            {config.label}
          </span>
        </div>
      </div>
      <p className="text-sm leading-relaxed text-[var(--mist)]">{message}</p>
      {evidence ? (
        <div className="mt-4 rounded-xl border border-[var(--ink-border)] bg-[var(--ink)] px-4 py-3">
          <p className="mb-1 text-[10px] font-medium uppercase tracking-widest text-[var(--gold-dim)]">
            Evidence
          </p>
          <p className="font-mono text-xs leading-relaxed text-[var(--snow)]">{evidence}</p>
        </div>
      ) : null}
    </article>
  );
}
