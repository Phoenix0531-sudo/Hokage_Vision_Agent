# Model Zoo

Model weights are external artifacts. They are not committed to this repository.

Use the registry to track local or release-provided model metadata:

```bash
hokage-vision model list
hokage-vision model compare --models models/a.pt models/b.pt --mock
```

Before publishing weights, confirm training data rights, model license, class list, metrics, and release notes.
