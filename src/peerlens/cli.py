import argparse
import asyncio
import json
import sys

import uvicorn

from peerlens.config import get_settings
from peerlens.services.reports import analyze_paper


def main() -> None:
    parser = argparse.ArgumentParser(description="PeerLens — research quality signals")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="Run the API server")
    serve_parser.add_argument("--host", default=None)
    serve_parser.add_argument("--port", type=int, default=None)
    serve_parser.add_argument("--reload", action="store_true")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a paper by DOI or arXiv ID")
    analyze_parser.add_argument("identifier", help="DOI or arXiv identifier")

    args = parser.parse_args()

    if args.command == "serve":
        settings = get_settings()
        uvicorn.run(
            "peerlens.main:app",
            host=args.host or settings.host,
            port=args.port or settings.port,
            reload=args.reload,
            log_level=settings.log_level,
        )
        return

    if args.command == "analyze":
        report = asyncio.run(analyze_paper(args.identifier))
        json.dump(report.model_dump(mode="json"), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
