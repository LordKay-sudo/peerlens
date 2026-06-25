"use client";

import { Eye, GitBranch, Layers } from "lucide-react";

const features = [
  {
    icon: Eye,
    title: "Transparent by design",
    body: "Every signal ships with severity, dimension, and optional evidence — no opaque scores.",
  },
  {
    icon: Layers,
    title: "Pluggable checkers",
    body: "Add domain-specific rules, LLM extraction, or human rubrics without rewriting the core.",
  },
  {
    icon: GitBranch,
    title: "Open & forkable",
    body: "MIT licensed. Inspect the pipeline, adapt it for your field, contribute signals back.",
  },
];

export function Features() {
  return (
    <section className="relative z-10 mx-auto w-full max-w-6xl px-6 pb-24">
      <div className="mb-10">
        <p className="mb-2 text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--gold-dim)]">
          Philosophy
        </p>
        <h2 className="font-serif text-3xl font-medium text-[var(--snow)]">
          Infrastructure, not authority
        </h2>
      </div>

      <div className="grid gap-5 md:grid-cols-3">
        {features.map(({ icon: Icon, title, body }) => (
          <article
            key={title}
            className="glass rounded-2xl p-6 transition duration-300 hover:-translate-y-1 hover:border-[var(--gold-dim)]"
          >
            <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-[var(--ink)]">
              <Icon className="h-5 w-5 text-[var(--gold-bright)]" strokeWidth={1.75} />
            </div>
            <h3 className="mb-2 font-medium text-[var(--snow)]">{title}</h3>
            <p className="text-sm leading-relaxed text-[var(--mist)]">{body}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
