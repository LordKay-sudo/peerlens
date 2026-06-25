"use client";

import { ArrowDown, BookOpen, Shield, Zap } from "lucide-react";

const highlights = [
  { icon: BookOpen, label: "DOI & arXiv ingestion" },
  { icon: Shield, label: "Explainable signals" },
  { icon: Zap, label: "FastAPI + open source" },
];

export function Hero() {
  return (
    <section className="relative z-10 mx-auto flex w-full max-w-6xl flex-col px-6 pb-20 pt-8">
      <div className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-[var(--ink-border)] bg-[var(--ink-elevated)] px-4 py-1.5 text-xs tracking-wide text-[var(--mist)]">
        <span className="h-1.5 w-1.5 rounded-full bg-[var(--teal)] shadow-[0_0_8px_var(--teal)]" />
        Open infrastructure · v0.1
      </div>

      <h1 className="max-w-4xl font-serif text-5xl font-medium leading-[1.05] tracking-tight sm:text-6xl lg:text-7xl">
        <span className="text-gradient">See through the paper.</span>
        <br />
        <span className="text-[var(--snow)]">Trust what&apos;s inside.</span>
      </h1>

      <p className="mt-6 max-w-2xl text-lg leading-relaxed text-[var(--mist)] sm:text-xl">
        PeerLens turns metadata into{" "}
        <span className="text-[var(--snow)]">transparent quality signals</span> — each with
        severity, evidence, and dimension. Decision support for science, not a black-box score.
      </p>

      <div className="mt-10 flex flex-wrap items-center gap-4">
        <a
          href="#analyze"
          className="gold-glow inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-[var(--gold-dim)] to-[var(--gold)] px-7 py-3.5 text-sm font-medium text-[var(--ink)] transition hover:brightness-110"
        >
          Analyze a paper
          <ArrowDown className="h-4 w-4" />
        </a>
        <p className="text-sm text-[var(--mist)]">
          Try{" "}
          <code className="rounded-md bg-[var(--ink-surface)] px-2 py-0.5 font-mono text-xs text-[var(--gold-bright)]">
            2301.07041
          </code>{" "}
          or any DOI
        </p>
      </div>

      <div className="mt-16 grid gap-4 sm:grid-cols-3">
        {highlights.map(({ icon: Icon, label }) => (
          <div
            key={label}
            className="glass flex items-center gap-3 rounded-2xl px-5 py-4 transition hover:border-[var(--gold-dim)]"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[var(--ink)]">
              <Icon className="h-4 w-4 text-[var(--gold-bright)]" strokeWidth={1.75} />
            </div>
            <span className="text-sm text-[var(--snow)]">{label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
