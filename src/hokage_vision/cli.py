from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import typer

from hokage_vision import __version__
from hokage_vision.agents.providers.rule_based import RuleBasedAgent
from hokage_vision.core.errors import HokageVisionError
from hokage_vision.data.annotation import assist_annotation
from hokage_vision.data.manifest import create_dataset_manifest
from hokage_vision.data.validation import validate_yolo_dataset
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.inference import InferenceService

app = typer.Typer(
    name="hokage-vision",
    help="Hokage Vision Agent command line interface.",
    no_args_is_help=True,
)
detect_app = typer.Typer(help="Run image, video, or folder detection.")
dataset_app = typer.Typer(help="Dataset management commands.")
dataset_manifest_app = typer.Typer(help="Dataset manifest commands.")
annotation_app = typer.Typer(help="Annotation assistance commands.")
train_app = typer.Typer(help="Training commands.")
model_app = typer.Typer(help="Model registry, evaluation, and comparison commands.")
agent_app = typer.Typer(help="Agent assistant commands.")

app.add_typer(detect_app, name="detect")
app.add_typer(dataset_app, name="dataset")
dataset_app.add_typer(dataset_manifest_app, name="manifest")
app.add_typer(annotation_app, name="annotation")
app.add_typer(train_app, name="train")
app.add_typer(model_app, name="model")
app.add_typer(agent_app, name="agent")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit


@app.callback()
def root(
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the installed Hokage Vision Agent version.",
    ),
) -> None:
    """Run Hokage Vision Agent commands."""


def _service_for_backend(backend: str) -> InferenceService:
    if backend != "mock":
        msg = f"Backend '{backend}' is not available yet. Use --backend mock in this phase."
        raise typer.BadParameter(msg)
    return InferenceService(MockBackend())


def _echo_json(value: object) -> None:
    typer.echo(json.dumps(value, ensure_ascii=False, indent=2, default=str))


@detect_app.command("image")
def detect_image(
    image_path: Path,
    backend: str = typer.Option("mock", "--backend", help="Vision backend to use."),
    save_rendered: bool = typer.Option(False, "--save-rendered", help="Save a rendered result image."),
    save_json: bool = typer.Option(False, "--save-json", help="Save a JSON result file."),
) -> None:
    """Detect anime character boxes in one image."""
    try:
        result = _service_for_backend(backend).detect_image(
            image_path,
            save_rendered=save_rendered,
            save_json=save_json,
        )
    except HokageVisionError as exc:
        raise typer.BadParameter(str(exc)) from exc
    _echo_json(asdict(result))


@detect_app.command("folder")
def detect_folder(
    folder: Path,
    backend: str = typer.Option("mock", "--backend", help="Vision backend to use."),
    recursive: bool = typer.Option(False, "--recursive", help="Scan nested folders."),
) -> None:
    """Detect anime character boxes in supported images from a folder."""
    try:
        results = _service_for_backend(backend).detect_folder(folder, recursive=recursive)
    except HokageVisionError as exc:
        raise typer.BadParameter(str(exc)) from exc
    _echo_json([asdict(result) for result in results])


@detect_app.command("video")
def detect_video(
    video_path: Path,
    backend: str = typer.Option("mock", "--backend", help="Vision backend to use."),
    frame_stride: int = typer.Option(30, "--frame-stride", min=1, help="Process every Nth frame."),
) -> None:
    """Detect anime character boxes in a video file."""
    try:
        summary = _service_for_backend(backend).detect_video(video_path, frame_stride=frame_stride)
    except HokageVisionError as exc:
        raise typer.BadParameter(str(exc)) from exc
    _echo_json(asdict(summary))


@dataset_app.command("validate")
def dataset_validate(dataset_yaml: Path) -> None:
    """Validate a YOLO dataset configuration."""
    _echo_json(asdict(validate_yolo_dataset(dataset_yaml)))


@dataset_manifest_app.command("create")
def dataset_manifest_create(
    images: Path = typer.Option(..., "--images", help="Local image folder."),
    output: Path = typer.Option(..., "--output", help="Manifest output path."),
) -> None:
    """Create a dataset manifest."""
    manifest = create_dataset_manifest(images, output)
    _echo_json(manifest.model_dump(mode="json"))


@annotation_app.command("assist")
def annotation_assist(
    images: Path = typer.Option(..., "--images", help="Local image folder."),
    model: Path | None = typer.Option(None, "--model", help="Optional model path for future real labeling."),
    output: Path = typer.Option(..., "--output", help="Candidate label output folder."),
    review_required: bool = typer.Option(True, "--review-required/--no-review-required"),
) -> None:
    """Generate candidate YOLO labels for human review."""
    result = assist_annotation(images, output)
    result["model"] = str(model) if model else None
    result["review_required"] = review_required
    _echo_json(result)


@train_app.command("smoke")
def train_smoke() -> None:
    """Run a lightweight smoke training flow. Placeholder until Phase 7."""
    _echo_json({"status": "placeholder", "training": "smoke", "dry_run": True})


@train_app.command("yolo")
def train_yolo(
    data: Path = typer.Option(..., "--data", help="YOLO dataset yaml."),
    epochs: int = typer.Option(1, "--epochs", min=1),
    dry_run: bool = typer.Option(True, "--dry-run/--execute"),
) -> None:
    """Plan or run YOLO training. Placeholder until Phase 7."""
    _echo_json({"status": "placeholder", "data": str(data), "epochs": epochs, "dry_run": dry_run})


@model_app.command("list")
def model_list() -> None:
    """List registered models. Placeholder until Phase 8."""
    _echo_json({"models": [], "status": "placeholder"})


@model_app.command("register")
def model_register(
    name: str = typer.Option(..., "--name"),
    path: Path = typer.Option(..., "--path"),
    backend: str = typer.Option("ultralytics", "--backend"),
) -> None:
    """Register a model. Placeholder until Phase 8."""
    _echo_json({"status": "placeholder", "name": name, "path": str(path), "backend": backend})


@model_app.command("evaluate")
def model_evaluate(
    model: Path = typer.Option(..., "--model"),
    data: Path = typer.Option(..., "--data"),
) -> None:
    """Evaluate one model. Placeholder until Phase 8."""
    _echo_json({"status": "placeholder", "model": str(model), "data": str(data)})


@model_app.command("compare")
def model_compare(
    models: list[Path] = typer.Option(..., "--models"),
    mock: bool = typer.Option(False, "--mock"),
) -> None:
    """Compare multiple model weights. Placeholder until Phase 8."""
    _echo_json({"status": "placeholder", "models": [str(model) for model in models], "mock": mock})


@agent_app.command("run")
def agent_run(task: str) -> None:
    """Run the default rule-based agent."""
    response = RuleBasedAgent().run(task)
    _echo_json(asdict(response))


@app.command("gui")
def gui() -> None:
    """Launch the desktop GUI. Placeholder until Phase 10."""
    _echo_json({"status": "placeholder", "app": "gui"})


@app.command("api")
def api() -> None:
    """Launch the FastAPI service. Placeholder until Phase 11."""
    _echo_json({"status": "placeholder", "app": "api"})


def main() -> None:
    app()
