"use client";

import type { PaperMetadata } from "@/types/api";
import { Calendar, ExternalLink, FileText, Hash, Users } from "lucide-react";

function formatDate(iso?: string | null) {
  if (!iso) return null;
  try {
    return new Intl.DateTimeFormat("en", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }).format(new Date(iso));
  } catch {
    return iso;
  }
}

interface PaperCardProps {
  paper: PaperMetadata;
}

export function PaperCard({ paper }: PaperCardProps) {
  const published = formatDate(paper.published);

  return (
    <article className="glass gold-glow sticky top-8 min-w-0 rounded-3xl p-8">
      <div className="mb-4 flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--ink)]">
          <FileText className="h-4 w-4 text-[var(--gold-bright)]" />
        </div>
        <span className="rounded-full border border-[var(--ink-border)] px-3 py-0.5 font-mono text-[10px] uppercase tracking-widest text-[var(--gold-bright)]">
          {paper.source}
        </span>
      </div>

      <h2 className="break-words font-serif text-2xl font-medium leading-snug tracking-tight text-[var(--snow)] [overflow-wrap:anywhere] sm:text-3xl">
        {paper.title}
      </h2>

      {paper.authors.length > 0 ? (
        <div className="mt-5 flex gap-3">
          <Users className="mt-0.5 h-4 w-4 shrink-0 text-[var(--mist)]" />
          <p className="text-sm leading-relaxed text-[var(--mist)]">
            {paper.authors.slice(0, 8).join(" · ")}
            {paper.authors.length > 8 ? ` · +${paper.authors.length - 8} more` : ""}
          </p>
        </div>
      ) : null}

      <dl className="mt-6 space-y-3 border-t border-[var(--ink-border)] pt-6">
        {published ? (
          <div className="flex items-center gap-3 text-sm">
            <Calendar className="h-4 w-4 text-[var(--gold-dim)]" />
            <dt className="sr-only">Published</dt>
            <dd className="text-[var(--mist)]">{published}</dd>
          </div>
        ) : null}
        {paper.doi ? (
          <div className="flex items-center gap-3 text-sm">
            <Hash className="h-4 w-4 text-[var(--gold-dim)]" />
            <dt className="sr-only">DOI</dt>
            <dd className="font-mono text-xs text-[var(--snow)]">{paper.doi}</dd>
          </div>
        ) : null}
        {paper.references_count != null ? (
          <div className="flex items-center gap-3 text-sm">
            <FileText className="h-4 w-4 text-[var(--gold-dim)]" />
            <dt className="sr-only">References</dt>
            <dd className="text-[var(--mist)]">{paper.references_count} references</dd>
          </div>
        ) : null}
      </dl>

      {paper.abstract ? (
        <div className="mt-6 border-t border-[var(--ink-border)] pt-6">
          <p className="mb-2 text-[10px] font-medium uppercase tracking-widest text-[var(--gold-dim)]">
            Abstract
          </p>
          <p className="text-sm leading-relaxed text-[var(--mist)]">{paper.abstract}</p>
        </div>
      ) : null}

      {paper.keywords.length > 0 ? (
        <div className="mt-6 flex flex-wrap gap-2">
          {paper.keywords.slice(0, 6).map((kw) => (
            <span
              key={kw}
              className="rounded-full border border-[var(--ink-border)] bg-[var(--ink)] px-3 py-1 text-xs text-[var(--mist)]"
            >
              {kw}
            </span>
          ))}
        </div>
      ) : null}

      {paper.url ? (
        <a
          href={paper.url}
          target="_blank"
          rel="noreferrer"
          className="mt-6 inline-flex items-center gap-2 text-sm text-[var(--gold-bright)] transition hover:text-[var(--gold)]"
        >
          View original
          <ExternalLink className="h-3.5 w-3.5" />
        </a>
      ) : null}
    </article>
  );
}
