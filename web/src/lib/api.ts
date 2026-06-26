import type { AskResponse, QualityReport } from "@/types/api";

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

export async function analyzeUploadedPdf(file: File): Promise<QualityReport> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE}/api/v1/papers/analyze/upload`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const detail =
      typeof payload.detail === "string"
        ? payload.detail
        : "PDF upload failed. Ensure the file is a valid PDF.";
    throw new Error(detail);
  }

  return response.json();
}

export async function askPaper(identifier: string, question: string): Promise<AskResponse> {
  const response = await fetch(`${API_BASE}/api/v1/papers/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, question }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const detail =
      typeof payload.detail === "string"
        ? payload.detail
        : "Could not answer this question.";
    throw new Error(detail);
  }

  return response.json();
}
