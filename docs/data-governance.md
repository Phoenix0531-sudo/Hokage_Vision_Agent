# Data Governance

Hokage Vision Agent does not download, scrape, or redistribute copyrighted anime images by default.

Dataset work must start from a manifest that records local source paths, license status, redistribution permission, classes, and annotation review state. Unknown licenses are treated as not redistributable.

Legacy Naruto/Hokage screenshots, local captures, and annotations are treated as local research material only. Do not publish them as a reusable public dataset, do not use them commercially, and do not upload them to releases until rights and redistribution terms are documented.

Historical model weights are also treated as research and portfolio artifacts only. They should remain outside git and outside default releases until the training data provenance, class list, metrics, and license terms are recorded.

Adding a new character class requires new images, rights review, annotations, class-name updates, dataset yaml updates, training or fine-tuning, evaluation, model registry updates, and README/docs updates.
