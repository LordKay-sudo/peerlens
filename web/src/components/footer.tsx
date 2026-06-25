export function Footer() {
  return (
    <footer className="relative z-10 border-t border-[var(--ink-border)]">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-4 px-6 py-10 sm:flex-row">
        <p className="font-serif text-sm text-[var(--mist)]">
          PeerLens · decision support for science
        </p>
        <p className="text-xs text-[var(--mist)]">
          MIT License ·{" "}
          <a
            href="https://github.com/LordKay-sudo/peerlens"
            className="text-[var(--gold-bright)] hover:underline"
          >
            github.com/LordKay-sudo/peerlens
          </a>
        </p>
      </div>
    </footer>
  );
}
