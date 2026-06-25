"use client";

import { Sparkles, Code2 } from "lucide-react";
import Link from "next/link";

export function Header() {
  return (
    <header className="relative z-20 mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6">
      <Link href="/" className="group flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-[var(--ink-border-bright)] bg-[var(--ink-surface)] shadow-[0_0_24px_color-mix(in_srgb,var(--gold)_15%,transparent)] transition group-hover:border-[var(--gold-dim)]">
          <Sparkles className="h-5 w-5 text-[var(--gold-bright)]" strokeWidth={1.75} />
        </div>
        <div>
          <p className="font-serif text-lg font-medium tracking-tight text-[var(--snow)]">
            PeerLens
          </p>
          <p className="text-xs tracking-wide text-[var(--mist)]">Research quality signals</p>
        </div>
      </Link>

      <nav className="flex items-center gap-4">
        <a
          href="#analyze"
          className="hidden text-sm text-[var(--mist)] transition hover:text-[var(--snow)] sm:inline"
        >
          Analyze
        </a>
        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noreferrer"
          className="hidden text-sm text-[var(--mist)] transition hover:text-[var(--snow)] sm:inline"
        >
          API
        </a>
        <a
          href="https://github.com/LordKay-sudo/peerlens"
          target="_blank"
          rel="noreferrer"
          className="glass flex items-center gap-2 rounded-full px-4 py-2 text-sm text-[var(--snow)] transition hover:border-[var(--gold-dim)]"
        >
          <Code2 className="h-4 w-4" />
          <span className="hidden sm:inline">GitHub</span>
        </a>
      </nav>
    </header>
  );
}
