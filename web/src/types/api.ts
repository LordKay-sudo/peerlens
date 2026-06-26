export type SignalSeverity = "info" | "warning" | "concern";

export type PaperSource = "arxiv" | "crossref" | "upload";

export interface QualitySignal {
  id: string;
  name: string;
  severity: SignalSeverity;
  message: string;
  evidence?: string | null;
  dimension: string;
}

export interface PaperMetadata {
  identifier: string;
  source: PaperSource;
  title: string;
  authors: string[];
  abstract?: string | null;
  published?: string | null;
  doi?: string | null;
  url?: string | null;
  keywords: string[];
  references_count?: number | null;
  sections?: Record<string, string>;
  pdf_analyzed?: boolean;
}

export interface QualityReport {
  identifier: string;
  paper: PaperMetadata;
  signals: QualitySignal[];
  summary: string;
  generated_at: string;
  sections?: Record<string, string>;
  pdf_analyzed?: boolean;
}

export interface CitationSpan {
  index: number;
  section?: string | null;
  excerpt: string;
  score: number;
}

export interface AskResponse {
  identifier: string;
  question: string;
  answer: string;
  citations: CitationSpan[];
  model?: string | null;
  chunks_used: number;
  pdf_analyzed: boolean;
  demo_mode?: boolean;
}
