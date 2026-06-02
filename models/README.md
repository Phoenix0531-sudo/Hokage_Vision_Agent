# Models

Model weights are not committed to git. Place local weights here only for local experiments, or download reviewed release artifacts with a documented license.

`registry.example.json` shows the expected metadata shape for smoke workflow entries and future external weight releases. `model-card.template.md` records the minimum information needed before a real weight can be presented professionally.

A local `registry.json` may be created by `hokage-vision model register`, but real model weights need separate provenance, metrics, checksum, release notes, and license review.

Historical Hokage/Naruto weights are treated as research and portfolio artifacts only, non-commercial, and not redistributed by default. Before any release, record the training data source, class list, metrics, intended use, and license.
