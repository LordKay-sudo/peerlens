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
}

export interface QualityReport {
  identifier: string;
  paper: PaperMetadata;
  signals: QualitySignal[];
  summary: string;
  generated_at: string;
}
