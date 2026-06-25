"use client";

import { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { analyzePaper, analyzeUploadedPdf } from "@/lib/api";
import type { QualityReport } from "@/types/api";
import { ReportView } from "./report-view";
import { ArrowRight, FileUp, Loader2, Search } from "lucide-react";

const EXAMPLES = ["2301.07041", "10.1038/nature12373", "arxiv:1706.03762"];

type AnalyzeMode = "identifier" | "pdf";

export function AnalyzeSection() {
  const [mode, setMode] = useState<AnalyzeMode>("identifier");
  const [identifier, setIdentifier] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<QualityReport | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleIdentifierSubmit(e: React.FormEvent) {
    e.preventDefault();
    const value = identifier.trim();
    if (!value) return;

    setLoading(true);
    setError(null);
    setReport(null);

    try {
      setReport(await analyzePaper(value));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function handlePdfSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setReport(null);

    try {
      setReport(await analyzeUploadedPdf(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section id="analyze" className="relative z-10 mx-auto w-full max-w-6xl px-6 pb-28">
      <div className="glass rounded-[2rem] p-8 sm:p-10">
        <div className="mb-8 max-w-2xl">
          <p className="mb-2 text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--gold-dim)]">
            Analyze
          </p>
          <h2 className="font-serif text-3xl font-medium tracking-tight text-[var(--snow)] sm:text-4xl">
            DOI, arXiv ID, or PDF
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-[var(--mist)]">
            PeerLens fetches metadata, auto-downloads open-access arXiv PDFs, extracts sections,
            and runs integrity + reproducibility checks.
          </p>
        </div>

        <div className="mb-6 flex gap-2 rounded-2xl border border-[var(--ink-border)] bg-[var(--ink)] p-1">
          <ModeButton active={mode === "identifier"} onClick={() => setMode("identifier")}>
            <Search className="h-4 w-4" />
            Identifier
          </ModeButton>
          <ModeButton active={mode === "pdf"} onClick={() => setMode("pdf")}>
            <FileUp className="h-4 w-4" />
            Upload PDF
          </ModeButton>
        </div>

        {mode === "identifier" ? (
          <form onSubmit={handleIdentifierSubmit} className="space-y-4">
            <div className="relative">
              <Search className="pointer-events-none absolute left-5 top-1/2 h-5 w-5 -translate-y-1/2 text-[var(--mist)]" />
              <input
                type="text"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="10.1038/nature12373 or 2301.07041"
                className="w-full rounded-2xl border border-[var(--ink-border)] bg-[var(--ink-elevated)] py-4 pl-14 pr-36 font-mono text-sm text-[var(--snow)] outline-none transition placeholder:text-[var(--mist)] focus:border-[var(--gold-dim)] focus:shadow-[0_0_0_4px_color-mix(in_srgb,var(--gold)_12%,transparent)]"
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
        ) : (
          <form onSubmit={handlePdfSubmit} className="space-y-4">
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf,.pdf"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="flex w-full flex-col items-center justify-center gap-3 rounded-2xl border border-dashed border-[var(--ink-border-bright)] bg-[var(--ink-elevated)] px-6 py-12 transition hover:border-[var(--gold-dim)]"
            >
              <FileUp className="h-8 w-8 text-[var(--gold-bright)]" />
              <span className="text-sm text-[var(--snow)]">
                {file ? file.name : "Choose a PDF (max 10 MB)"}
              </span>
              <span className="text-xs text-[var(--mist)]">
                Extracts sections and scans for code/data repository links
              </span>
            </button>
            <button
              type="submit"
              disabled={loading || !file}
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--gold-dim)] to-[var(--gold)] px-6 py-3 text-sm font-medium text-[var(--ink)] transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Analyzing PDF
                </>
              ) : (
                <>
                  Analyze PDF
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </form>
        )}

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

        <AnimatePresence>
          {report ? <ReportView key={report.identifier} report={report} /> : null}
        </AnimatePresence>
      </div>
    </section>
  );
}

function ModeButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex flex-1 items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm transition ${
        active
          ? "bg-[var(--ink-surface)] text-[var(--snow)] shadow-sm"
          : "text-[var(--mist)] hover:text-[var(--snow)]"
      }`}
    >
      {children}
    </button>
  );
}
