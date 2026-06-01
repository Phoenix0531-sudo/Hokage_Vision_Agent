# Annotation Assistance

Annotation assistance generates candidate YOLO labels from an existing model backend. These labels are always treated as `review_required: true`.

The tool does not replace human review and does not create legally usable training data without verified image sources and usage rights.

```bash
hokage-vision annotation assist --images examples/images --output data/interim/labels --review-required
```
