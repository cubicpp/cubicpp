Classic profile metrics use lowlighter/metrics v3.34 at commit
65836723097537a54cd8eb90f61839426b4266b6.

Template: classic, with header, activity, community, repositories and metadata.
Source: https://github.com/lowlighter/metrics/tree/65836723097537a54cd8eb90f61839426b4266b6/source/templates/classic
License: MIT, included in METRICS-LICENSE.

Runtime: official ghcr.io/lowlighter/metrics v3.34 image pinned to digest
sha256:257392f90340f916cb8b815026f259399f6b246d3eb7de38b58bfe7a07bd5b65.
The workflow loads this exact image under the local metrics:3.34.0 tag so the
pinned upstream Action reuses it instead of rebuilding its broken Dockerfile.

The checked-in SVGs are generated snapshots. The metrics workflow refreshes them
only when the repository has a separately configured METRICS_TOKEN secret.
Without this secret, it keeps the current snapshot. The regular profile visual
workflow continues to refresh the other components independently.
