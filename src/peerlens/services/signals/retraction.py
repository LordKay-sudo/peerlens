from peerlens.models.context import AnalysisContext
from peerlens.models.schemas import QualitySignal, SignalSeverity
from peerlens.services.signals.base import SignalChecker


def _is_retracted(record: dict) -> tuple[bool, str | None]:
    for update in record.get("update-to", []) or []:
        update_type = (update.get("type") or "").lower()
        if update_type == "retraction":
            label = update.get("label") or update.get("DOI") or "retraction record"
            return True, f"Crossref update-to: {label}"

    for relation in record.get("relation", []) or []:
        relation_type = (relation.get("type") or "").lower()
        if relation_type in {"is-retracted-by", "retracts"}:
            target = relation.get("id") or relation.get("doi") or relation_type
            return True, f"Crossref relation: {target}"

    title = " ".join(record.get("title") or []).lower()
    if "retracted" in title:
        return True, "Title contains 'retracted'"

    return False, None


class RetractionChecker(SignalChecker):
    id = "retraction_status"
    name = "Retraction status"
    dimension = "integrity"

    def check(self, context: AnalysisContext) -> list[QualitySignal]:
        if not context.paper.doi:
            return [
                QualitySignal(
                    id="no_doi_for_retraction_check",
                    name="Retraction check skipped",
                    severity=SignalSeverity.INFO,
                    message="No DOI available; Crossref retraction status could not be checked.",
                    dimension=self.dimension,
                )
            ]

        if not context.crossref_record:
            return [
                QualitySignal(
                    id="crossref_unavailable",
                    name="Retraction check unavailable",
                    severity=SignalSeverity.INFO,
                    message="Crossref metadata was not loaded for this DOI.",
                    dimension=self.dimension,
                )
            ]

        retracted, evidence = _is_retracted(context.crossref_record)
        if retracted:
            return [
                QualitySignal(
                    id="paper_retracted",
                    name="Retracted publication",
                    severity=SignalSeverity.CONCERN,
                    message=(
                        "Crossref metadata indicates this DOI is associated with a retraction. "
                        "Do not use this work as established evidence without reviewing the notice."
                    ),
                    evidence=evidence,
                    dimension=self.dimension,
                )
            ]

        return [
            QualitySignal(
                id="not_retracted",
                name="No retraction on record",
                severity=SignalSeverity.INFO,
                message="Crossref shows no retraction relation or update for this DOI.",
                dimension=self.dimension,
            )
        ]
