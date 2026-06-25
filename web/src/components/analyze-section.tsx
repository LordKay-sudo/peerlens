"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { analyzePaper } from "@/lib/api";
import type { QualityReport } from "@/types/api";
import { ReportView } from "./report-view";
import { ArrowRight, Loader2, Search } from "lucide-react";

const EXAMPLES = ["2301.07041", "10.1038/nature12373", "arxiv:1706.03762"];

export function AnalyzeSection() {
  const [identifier, setIdentifier] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<QualityReport | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const value = identifier.trim();
    if (!value) return;

    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const result = await analyzePaper(value);
      setReport(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section id="analyze" className="relative z-10 mx-auto w-full max-w-6xl px-6 pb-28">
      <div className="glass rounded-[2rem] p-8 sm:p-10">
        <div className="mb-8 max-w-xl">
          <p className="mb-2 text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--gold-dim)]">
            Analyze
          </p>
          <h2 className="font-serif text-3xl font-medium tracking-tight text-[var(--snow)] sm:text-4xl">
            Paste a DOI or arXiv ID
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-[var(--mist)]">
            PeerLens fetches open metadata and runs explainable checks. v0.1 analyzes abstracts
            and bibliographic data — not full PDFs yet.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Search className="pointer-events-none absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-[var(--mist)]" />
            <input
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="10.1038/nature12373 or 2301.07041"
              className="w-full rounded-2xl border border-[var(--ink-border)] bg-[var(--ink)] py-4 pl-14 pr-36 font-mono text-sm text-[var(--snow)] outline-none transition placeholder:text-[var(--mist)] focus:border-[var(--gold-dim)] focus:shadow-[0_0_0_4px_color-mix(in_srgb,var(--gold)_12%,transparent)]"
              disabled={loading}
              spellCheck={false}
            />
            <button
              type="submit"
              disabled={loading || !identifier.trim()}
              className="absolute right-2 top-1/2 flex -translate-y-1/2 items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--gold-dim)] to-[var(--gold)] px-5 py-2.5 text-sm font-medium text-[var(--ink)] transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Analyzing
                </>
              ) : (
                <>
                  Run
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-[var(--mist)]">Try:</span>
            {EXAMPLES.map((ex) => (
              <button
                key={ex}
                type="button"
                onClick={() => setIdentifier(ex)}
                className="rounded-full border border-[var(--ink-border)] bg-[var(--ink-elevated)] px-3 py-1 font-mono text-xs text-[var(--gold-bright)] transition hover:border-[var(--gold-dim)]"
              >
                {ex}
              </button>
            ))}
          </div>
        </form>

        <AnimatePresence mode="wait">
          {error ? (
            <motion.div
              key="error"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mt-6 rounded-2xl border border-[color-mix(in_srgb,var(--rose)_40%,var(--ink-border))] bg-[color-mix(in_srgb,var(--rose)_8%,var(--ink))] px-5 py-4 text-sm text-[var(--rose)]"
            >
              {error}
            </motion.div>
          ) : null}
        </AnimatePresence>

        <AnimatePresence>{report ? <ReportView key={report.identifier} report={report} /> : null}</AnimatePresence>
      </div>
    </section>
  );
}
