from __future__ import annotations

import importlib
import inspect
import sys
from collections.abc import Iterable, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any

from ansysmcp.serialization import to_jsonable

APP_CLASS_PATHS: dict[str, tuple[str, str]] = {
    "desktop": ("ansys.aedt.core", "Desktop"),
    "hfss": ("ansys.aedt.core", "Hfss"),
    "q3d": ("ansys.aedt.core", "Q3d"),
    "q2d": ("ansys.aedt.core", "Q2d"),
    "maxwell2d": ("ansys.aedt.core", "Maxwell2d"),
    "maxwell3d": ("ansys.aedt.core", "Maxwell3d"),
    "icepak": ("ansys.aedt.core", "Icepak"),
    "hfss3dlayout": ("ansys.aedt.core", "Hfss3dLayout"),
    "mechanical": ("ansys.aedt.core", "Mechanical"),
    "rmxprt": ("ansys.aedt.core", "Rmxprt"),
    "circuit": ("ansys.aedt.core", "Circuit"),
    "maxwellcircuit": ("ansys.aedt.core", "MaxwellCircuit"),
    "emit": ("ansys.aedt.core", "Emit"),
    "twinbuilder": ("ansys.aedt.core", "TwinBuilder"),
}

APP_ALIASES = {
    "hfss3d": "hfss",
    "hfss_3d_layout": "hfss3dlayout",
    "hfss-3d-layout": "hfss3dlayout",
    "q3dextractor": "q3d",
    "q2dextractor": "q2d",
    "maxwell_2d": "maxwell2d",
    "maxwell_3d": "maxwell3d",
    "maxwell_circuit": "maxwellcircuit",
    "twin_builder": "twinbuilder",
}


@dataclass
class AedtSessionState:
    app_name: str
    app: Any


class AedtError(RuntimeError):
    """Raised when an AEDT operation cannot be completed."""


class AedtSessionManager:
    def __init__(self) -> None:
        self._state: AedtSessionState | None = None
        self._lock = RLock()

    @contextmanager
    def locked(self):
        """Serialize PyAEDT calls against the stateful AEDT Desktop session."""
        with self._lock:
            yield

    @property
    def active(self) -> bool:
        return self._state is not None

    @property
    def app(self) -> Any:
        if self._state is None:
            raise AedtError("No active AEDT session. Call aedt_start_session first.")
        return self._state.app

    @property
    def app_name(self) -> str:
        if self._state is None:
            raise AedtError("No active AEDT session. Call aedt_start_session first.")
        return self._state.app_name

    def start(
        self,
        app_name: str,
        *,
        version: str | int | float | None = None,
        project: str | None = None,
        design: str | None = None,
        solution_type: str | None = None,
        non_graphical: bool = False,
        new_desktop: bool = True,
        close_on_exit: bool = False,
        student_version: bool = False,
        machine: str | None = None,
        port: int | None = None,
        aedt_process_id: int | None = None,
        extra_kwargs: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            normalized = normalize_app_name(app_name)
            app_class = import_app_class(normalized)

            kwargs: dict[str, Any] = {
                "version": version,
                "project": project,
                "design": design,
                "solution_type": solution_type,
                "non_graphical": non_graphical,
                "new_desktop": new_desktop,
                "close_on_exit": close_on_exit,
                "student_version": student_version,
                "machine": machine,
                "port": port,
                "aedt_process_id": aedt_process_id,
            }
            if extra_kwargs:
                kwargs.update(dict(extra_kwargs))

            app = instantiate_with_supported_kwargs(app_class, kwargs)
            self._state = AedtSessionState(app_name=normalized, app=app)
            return self.info()

    def release(
        self,
        *,
        close_projects: bool = False,
        close_desktop: bool = False,
    ) -> dict[str, Any]:
        with self._lock:
            if self._state is None:
                return {"released": False, "reason": "no_active_session"}

            app = self._state.app
            release_result: Any = None
            if hasattr(app, "release_desktop"):
                release_result = call_with_supported_kwargs(
                    app.release_desktop,
                    {
                        "close_projects": close_projects,
                        "close_desktop": close_desktop,
                        "close_on_exit": close_desktop,
                    },
                    positional_fallback=[close_projects, close_desktop],
                )
            elif close_desktop and hasattr(app, "close_desktop"):
                release_result = app.close_desktop()

            self._state = None
            return {"released": True, "result": to_jsonable(release_result)}

    def info(self) -> dict[str, Any]:
        with self._lock:
            if self._state is None:
                return {"active": False, "available_apps": sorted(APP_CLASS_PATHS)}

            app = self._state.app
            info = {
                "active": True,
                "app_name": self._state.app_name,
                "app_type": f"{type(app).__module__}.{type(app).__name__}",
            }
        for attr in (
            "project_name",
            "design_name",
            "active_project_name",
            "active_design_name",
            "project_list",
            "solution_type",
            "design_type",
            "aedt_version_id",
            "aedt_version_string",
            "project_path",
        ):
            if hasattr(app, attr):
                try:
                    value = getattr(app, attr)
                    if callable(value):
                        continue
                    info[attr] = to_jsonable(value)
                except Exception as exc:
                    info[attr] = {"error": str(exc)}
        return info

    def save_project(
        self,
        *,
        project_name: str | None = None,
        project_path: str | None = None,
        overwrite: bool = True,
    ) -> dict[str, Any]:
        app = self.app
        target = get_desktop(app) or app
        if hasattr(target, "save_project"):
            result = call_with_supported_kwargs(
                target.save_project,
                {
                    "project_name": project_name,
                    "project_file": project_path,
                    "project_path": project_path,
                    "overwrite": overwrite,
                },
                positional_fallback=[
                    item
                    for item in (project_name, project_path, overwrite)
                    if item is not None
                ],
            )
            return {"saved": True, "result": to_jsonable(result)}
        raise AedtError("Active AEDT object does not expose save_project.")

    def open_project(self, project_path: str, design_name: str | None = None) -> dict[str, Any]:
        app = self.app
        target = get_desktop(app) or app
        resolved_path = str(Path(project_path).expanduser())
        if hasattr(target, "load_project"):
            result = call_with_supported_kwargs(
                target.load_project,
                {"project_file": resolved_path, "design_name": design_name},
                positional_fallback=(
                    [resolved_path]
                    if design_name is None
                    else [resolved_path, design_name]
                ),
            )
            return {"opened": True, "result": to_jsonable(result), "path": resolved_path}
        raise AedtError("Active AEDT object does not expose load_project.")

    def target(self, target: str, *, module_name: str | None = None) -> Any:
        app = self.app
        name = target.lower().strip()
        if name == "app":
            return app
        if name == "desktop":
            desktop = get_desktop(app)
            if desktop is None:
                raise AedtError("Desktop object is unavailable for the active session.")
            return desktop
        if name == "odesktop":
            return get_required_attr(get_desktop(app) or app, "odesktop")
        if name == "oproject":
            return get_active_project_object(app)
        if name == "odesign":
            return get_active_design_object(app)
        if name == "oeditor":
            if hasattr(app, "oeditor"):
                return app.oeditor
            return get_active_design_object(app).SetActiveEditor("3D Modeler")
        if name == "omodule":
            if not module_name:
                raise AedtError("module_name is required when target is omodule.")
            design = get_active_design_object(app)
            return design.GetModule(module_name)
        attr_targets = {
            "modeler": "modeler",
            "post": "post",
            "mesh": "mesh",
            "materials": "materials",
            "variable_manager": "variable_manager",
            "parametrics": "parametrics",
            "optimizations": "optimizations",
            "setups": "setups",
            "boundaries": "boundaries",
            "configurations": "configurations",
        }
        if name in attr_targets:
            return get_required_attr(app, attr_targets[name])
        raise AedtError(f"Unsupported target '{target}'.")


def normalize_app_name(app_name: str) -> str:
    normalized = app_name.replace(" ", "").replace("-", "").replace("_", "").lower()
    normalized = APP_ALIASES.get(normalized, normalized)
    if normalized not in APP_CLASS_PATHS:
        supported = ", ".join(sorted(APP_CLASS_PATHS))
        raise AedtError(f"Unsupported app '{app_name}'. Supported apps: {supported}.")
    return normalized


def import_app_class(app_name: str) -> type[Any]:
    module_name, class_name = APP_CLASS_PATHS[app_name]
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        raise AedtError(
            "PyAEDT is unavailable. Install dependencies with 'uv sync' and run on a Python "
            "version supported by PyAEDT."
        ) from exc
    try:
        return getattr(module, class_name)
    except AttributeError as exc:
        raise AedtError(f"PyAEDT module '{module_name}' does not expose '{class_name}'.") from exc


def instantiate_with_supported_kwargs(factory: type[Any], kwargs: Mapping[str, Any]) -> Any:
    supported = filter_supported_kwargs(factory, kwargs)
    return factory(**supported)


def call_with_supported_kwargs(
    func: Any,
    kwargs: Mapping[str, Any],
    *,
    positional_fallback: Iterable[Any] | None = None,
) -> Any:
    supported = filter_supported_kwargs(func, kwargs)
    if supported:
        return func(**supported)
    if positional_fallback is not None:
        return func(*list(positional_fallback))
    return func()


def filter_supported_kwargs(callable_obj: Any, kwargs: Mapping[str, Any]) -> dict[str, Any]:
    clean = {key: value for key, value in kwargs.items() if value is not None}
    try:
        signature = inspect.signature(callable_obj)
    except (TypeError, ValueError):
        return clean
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return clean
    return {key: value for key, value in clean.items() if key in signature.parameters}


def get_desktop(app: Any) -> Any | None:
    if hasattr(app, "odesktop") and hasattr(app, "project_list"):
        return app
    for attr in ("desktop_class", "desktop", "_desktop"):
        if hasattr(app, attr):
            try:
                value = getattr(app, attr)
            except Exception:
                continue
            if value is not None:
                return value
    return None


def get_active_project_object(app: Any) -> Any:
    if hasattr(app, "oproject"):
        return app.oproject
    desktop = get_desktop(app)
    if desktop is not None and hasattr(desktop, "active_project"):
        project = desktop.active_project()
        if project is not None:
            return project
    raise AedtError("Active project object is unavailable.")


def get_active_design_object(app: Any) -> Any:
    if hasattr(app, "odesign"):
        return app.odesign
    desktop = get_desktop(app)
    if desktop is not None and hasattr(desktop, "active_design"):
        design = desktop.active_design()
        if design is not None:
            return design
    raise AedtError("Active design object is unavailable.")


def get_required_attr(obj: Any, attr: str) -> Any:
    if not hasattr(obj, attr):
        raise AedtError(f"{type(obj).__name__} does not expose '{attr}'.")
    return getattr(obj, attr)


def environment_report() -> dict[str, Any]:
    report: dict[str, Any] = {
        "python": sys.version,
        "available_apps": sorted(APP_CLASS_PATHS),
    }
    try:
        module = importlib.import_module("ansys.aedt.core")
        report["pyaedt_available"] = True
        report["pyaedt_module"] = getattr(module, "__file__", None)
        report["pyaedt_version"] = getattr(module, "__version__", None)
    except ImportError as exc:
        report["pyaedt_available"] = False
        report["pyaedt_error"] = str(exc)
    return report


def api_manifest(app_name: str | None = None, *, include_private: bool = False) -> dict[str, Any]:
    app_names = [normalize_app_name(app_name)] if app_name else sorted(APP_CLASS_PATHS)
    manifest: dict[str, Any] = {}
    for name in app_names:
        app_class = import_app_class(name)
        methods: dict[str, str] = {}
        attributes: list[str] = []
        for member_name in dir(app_class):
            if not include_private and member_name.startswith("_"):
                continue
            try:
                member = getattr(app_class, member_name)
            except Exception:
                continue
            if callable(member):
                methods[member_name] = signature_text(member)
            else:
                attributes.append(member_name)
        manifest[name] = {
            "class": f"{app_class.__module__}.{app_class.__name__}",
            "constructor": signature_text(app_class),
            "methods": dict(sorted(methods.items())),
            "attributes": sorted(attributes),
        }
    return manifest


def signature_text(callable_obj: Any) -> str:
    try:
        return str(inspect.signature(callable_obj))
    except (TypeError, ValueError):
        return "(...)"
