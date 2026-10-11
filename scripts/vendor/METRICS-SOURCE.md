Classic profile metrics use lowlighter/metrics v3.34 at commit
65836723097537a54cd8eb90f61839426b4266b6.

Template: classic, with header, activity, community, repositories and metadata.
Source: https://github.com/lowlighter/metrics/tree/65836723097537a54cd8eb90f61839426b4266b6/source/templates/classic
License: MIT, included in METRICS-LICENSE.

The checked-in SVGs are generated snapshots. The metrics workflow refreshes them
only when the repository has a separately configured METRICS_TOKEN secret.
Without this secret, it keeps the current snapshot. The regular profile visual
workflow continues to refresh the other components independently.
