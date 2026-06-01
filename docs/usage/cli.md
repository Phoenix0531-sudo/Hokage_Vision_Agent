# CLI

The command line entrypoint is `hokage-vision`.

```bash
hokage-vision --help
hokage-vision detect image examples/images/sample.jpg --backend mock
hokage-vision detect folder examples/images --backend mock
hokage-vision agent run "检测 examples/images 里的图片"
```

Phase 4 provides real mock detection for images and folders. Dataset, training, model, GUI, API, and agent commands are exposed as stable placeholders and become fully wired in later phases.
