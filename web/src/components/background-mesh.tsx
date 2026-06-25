export function BackgroundMesh() {
  return (
    <div className="pointer-events-none fixed inset-0 overflow-hidden" aria-hidden>
      <div className="grid-lines absolute inset-0 opacity-60" />
      <div className="noise absolute inset-0" />
      <div
        className="orb absolute -left-32 top-[-10%] h-[520px] w-[520px] rounded-full opacity-40 blur-3xl"
        style={{
          background:
            "radial-gradient(circle, color-mix(in srgb, var(--gold) 70%, transparent), transparent 70%)",
        }}
      />
      <div
        className="orb orb-delay-1 absolute right-[-8%] top-[15%] h-[480px] w-[480px] rounded-full opacity-30 blur-3xl"
        style={{
          background:
            "radial-gradient(circle, color-mix(in srgb, var(--violet) 65%, transparent), transparent 70%)",
        }}
      />
      <div
        className="orb orb-delay-2 absolute bottom-[-15%] left-[30%] h-[560px] w-[560px] rounded-full opacity-25 blur-3xl"
        style={{
          background:
            "radial-gradient(circle, color-mix(in srgb, var(--teal) 55%, transparent), transparent 70%)",
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[var(--ink)]" />
    </div>
  );
}
