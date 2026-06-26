"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { askPaper } from "@/lib/api";
import type { AskResponse } from "@/types/api";
import { Loader2, MessageCircle, Send } from "lucide-react";

const SUGGESTED = [
  "What methods does this paper use?",
  "What are the main findings?",
  "What limitations are discussed?",
  "Is code or data availability mentioned?",
];

interface AskPanelProps {
  identifier: string;
  paperTitle: string;
  pdfAnalyzed?: boolean;
}

export function AskPanel({ identifier, paperTitle, pdfAnalyzed }: AskPanelProps) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<AskResponse | null>(null);

  async function submit(value: string) {
    const trimmed = value.trim();
    if (!trimmed) return;

    setLoading(true);
    setError(null);

    try {
      const result = await askPaper(identifier, trimmed);
      setResponse(result);
      setQuestion(trimmed);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not answer question.");
      setResponse(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass mt-10 rounded-3xl p-6 sm:p-8"
    >
      <div className="mb-6 flex items-start gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-[var(--ink)]">
          <MessageCircle className="h-5 w-5 text-[var(--gold-bright)]" />
        </div>
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--gold-dim)]">
            RAG Q&A
          </p>
          <h3 className="font-serif text-2xl font-medium text-[var(--snow)]">Ask this paper</h3>
          <p className="mt-1 text-sm text-[var(--mist)]">
            Retrieval-augmented answers from{" "}
            <span className="text-[var(--snow)]">{paperTitle}</span>
            {pdfAnalyzed ? " (full text)" : " (metadata / abstract)"}.
          </p>
        </div>
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          submit(question);
        }}
        className="relative"
      >
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What methods does this paper use?"
          disabled={loading}
          className="w-full rounded-2xl border border-[var(--ink-border)] bg-[var(--ink)] py-4 pl-5 pr-32 text-sm text-[var(--snow)] outline-none transition placeholder:text-[var(--mist)] focus:border-[var(--gold-dim)]"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="absolute right-2 top-1/2 flex -translate-y-1/2 items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--gold-dim)] to-[var(--gold)] px-4 py-2.5 text-sm font-medium text-[var(--ink)] disabled:opacity-50"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          Ask
        </button>
      </form>

      <div className="mt-3 flex flex-wrap gap-2">
        {SUGGESTED.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => {
              setQuestion(item);
              submit(item);
            }}
            disabled={loading}
            className="rounded-full border border-[var(--ink-border)] bg-[var(--ink-elevated)] px-3 py-1 text-xs text-[var(--mist)] transition hover:border-[var(--gold-dim)] hover:text-[var(--snow)]"
          >
            {item}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {error ? (
          <motion.p
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mt-5 rounded-xl border border-[color-mix(in_srgb,var(--rose)_35%,var(--ink-border))] bg-[color-mix(in_srgb,var(--rose)_8%,var(--ink))] px-4 py-3 text-sm text-[var(--rose)]"
          >
            {error}
          </motion.p>
        ) : null}
      </AnimatePresence>

      <AnimatePresence>
        {response ? (
          <motion.div
            key={response.question}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 space-y-5"
          >
            <div className="rounded-2xl border border-[var(--ink-border)] bg-[var(--ink)] p-5">
              <p className="mb-2 text-[10px] uppercase tracking-widest text-[var(--gold-dim)]">
                Answer
                {response.model ? (
                  <span className="ml-2 text-[var(--mist)]">via {response.model}</span>
                ) : null}
              </p>
              <p className="whitespace-pre-wrap text-sm leading-relaxed text-[var(--snow)]">
                {response.answer}
              </p>
            </div>

            {response.citations.length > 0 ? (
              <div>
                <p className="mb-3 text-[10px] uppercase tracking-widest text-[var(--gold-dim)]">
                  Sources ({response.chunks_used} chunks)
                </p>
                <div className="space-y-3">
                  {response.citations.map((cite) => (
                    <div
                      key={cite.index}
                      className="rounded-xl border border-[var(--ink-border)] bg-[var(--ink-elevated)] p-4"
                    >
                      <div className="mb-2 flex items-center justify-between gap-2">
                        <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--gold-bright)]">
                          {cite.section ?? "body"} · #{cite.index + 1}
                        </span>
                        <span className="text-xs text-[var(--mist)]">
                          relevance {(cite.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-xs leading-relaxed text-[var(--mist)]">{cite.excerpt}</p>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </motion.div>
        ) : null}
      </AnimatePresence>
    </motion.section>
  );
}
