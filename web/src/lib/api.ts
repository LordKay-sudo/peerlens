import type { QualityReport } from "@/types/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export async function analyzePaper(identifier: string): Promise<QualityReport> {
  const response = await fetch(`${API_BASE}/api/v1/papers/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const detail =
      typeof payload.detail === "string"
        ? payload.detail
        : "Analysis failed. Check the identifier and try again.";
    throw new Error(detail);
  }

  return response.json();
}
