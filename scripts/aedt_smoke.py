from __future__ import annotations

import argparse
import json
from typing import Any

from ansysmcp.operations import list_projects, new_project
from ansysmcp.session import AedtSessionManager, environment_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke test ansysmcp against PyAEDT/AEDT.")
    parser.add_argument("--version", default="2024.2", help="AEDT version, for example 2024.2.")
    parser.add_argument(
        "--mode",
        choices=["environment", "desktop", "app"],
        default="environment",
        help="Smoke level to run.",
    )
    parser.add_argument("--app", default="hfss", help="PyAEDT app name when --mode app is used.")
    parser.add_argument("--port", type=int, default=None, help="Existing gRPC port to attach to.")
    parser.add_argument("--machine", default=None, help="Remote AEDT host for gRPC attach.")
    parser.add_argument(
        "--create-project",
        default=None,
        help="Create a native AEDT project by name.",
    )
    parser.add_argument("--graphical", action="store_true", help="Launch AEDT with UI.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result: dict[str, Any] = {"environment": environment_report()}
    if args.mode == "environment":
        print(json.dumps(result, indent=2, default=str))
        return

    manager = AedtSessionManager()
    app_name = "desktop" if args.mode == "desktop" else args.app
    try:
        result["session"] = manager.start(
            app_name,
            version=args.version,
            non_graphical=not args.graphical,
            new_desktop=args.port is None,
            close_on_exit=False,
            machine=args.machine,
            port=args.port,
        )
        if args.create_project:
            result["created_project"] = new_project(manager, project_name=args.create_project)
        result["projects"] = list_projects(manager)
    finally:
        result["release"] = manager.release(close_projects=True, close_desktop=True)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
