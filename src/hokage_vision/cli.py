from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import typer

from hokage_vision import __version__
from hokage_vision.agents.providers.rule_based import RuleBasedAgent
from hokage_vision.core.errors import HokageVisionError
from hokage_vision.core.types import ModelInfo
from hokage_vision.data.annotation import assist_annotation
from hokage_vision.data.manifest import create_dataset_manifest
from hokage_vision.data.validation import validate_yolo_dataset
from hokage_vision.training.registry import ModelRegistry
from hokage_vision.training.smoke import run_smoke_training
from hokage_vision.training.trainer import run_yolo_training
from hokage_vision.vision.backends.mock import MockBackend
from hokage_vision.vision.evaluation import evaluate_model
from hokage_vision.vision.inference import InferenceService
from hokage_vision.vision.model_compare import compare_model_paths

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
    save_rendered: bool = typer.Option(
        False, "--save-rendered", help="Save a rendered result image."
    ),
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
    model: Path | None = typer.Option(
        None, "--model", help="Optional model path for future real labeling."
    ),
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
    """Run a lightweight smoke training flow."""
    _echo_json(run_smoke_training())


@train_app.command("yolo")
def train_yolo(
    data: Path = typer.Option(..., "--data", help="YOLO dataset yaml."),
    epochs: int = typer.Option(1, "--epochs", min=1),
    batch: int = typer.Option(1, "--batch", min=1),
    image_size: int = typer.Option(640, "--imgsz", min=1),
    device: str = typer.Option("cpu", "--device"),
    dry_run: bool = typer.Option(True, "--dry-run/--execute"),
) -> None:
    """Plan or run YOLO training."""
    try:
        result = run_yolo_training(
            data,
            epochs=epochs,
            batch=batch,
            image_size=image_size,
            device=device,
            dry_run=dry_run,
        )
    except HokageVisionError as exc:
        raise typer.BadParameter(str(exc)) from exc
    _echo_json(result)


@model_app.command("list")
def model_list() -> None:
    """List registered models."""
    _echo_json({"models": ModelRegistry().list_models()})


@model_app.command("register")
def model_register(
    name: str = typer.Option(..., "--name"),
    path: Path = typer.Option(..., "--path"),
    backend: str = typer.Option("ultralytics", "--backend"),
) -> None:
    """Register a model."""
    model = ModelInfo(
        name=name, version="0.1.0", path=path, backend=backend, classes=["obito", "naruto", "gaara"]
    )
    _echo_json(ModelRegistry().register(model))


@model_app.command("evaluate")
def model_evaluate(
    model: Path = typer.Option(..., "--model"),
    data: Path = typer.Option(..., "--data"),
) -> None:
    """Evaluate one model."""
    _echo_json(evaluate_model(model, data, mock=True))


@model_app.command(
    "compare", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def model_compare(
    ctx: typer.Context,
    models: list[Path] | None = typer.Option(None, "--models"),
    mock: bool = typer.Option(False, "--mock"),
) -> None:
    """Compare multiple model weights."""
    selected_models = list(models or []) + [Path(arg) for arg in ctx.args]
    if not selected_models:
        raise typer.BadParameter("At least one model path is required.")
    _echo_json({"models": compare_model_paths(selected_models, mock=mock)})


@agent_app.command("run")
def agent_run(task: str) -> None:
    """Run the default rule-based agent."""
    response = RuleBasedAgent().run(task)
    _echo_json(asdict(response))


@app.command("gui")
def gui() -> None:
    """Launch the desktop GUI."""
    from hokage_vision.ui.app import run_app

    raise typer.Exit(run_app())


@app.command("api")
def api(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port", min=1, max=65535),
) -> None:
    """Launch the FastAPI service."""
    try:
        import uvicorn
    except ImportError as exc:
        raise typer.BadParameter("Install the API extra with: pip install -e '.[api]'") from exc

    uvicorn.run("hokage_vision.api.app:app", host=host, port=port)


def main() -> None:
    app()
