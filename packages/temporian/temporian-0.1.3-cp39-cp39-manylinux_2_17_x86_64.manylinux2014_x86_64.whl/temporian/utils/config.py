# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration options.

This module contains configuration options for Temporian. These options can be
set by setting them at runtime, or by setting the corresponding environment
variables.

For example, to configure the maximum number of indexes to show when displaying
an EventSet to 5, you can either:

- Run `temporian.config.max_printed_indexes = 5`
- Set the `TEMPORIAN_MAX_PRINTED_INDEXES` environment variable to 5, for example
    by running `export TEMPORIAN_MAX_PRINTED_INDEXES=5` in a terminal before
    running your Temporian code.
"""

import os

debug_mode = bool(os.environ.get("TEMPORIAN_DEBUG_MODE", False))
"""Whether to run Temporian in debugging mode. This will enable additional
checks and logging, which may slow down execution."""

# Limits for repr(evset), print(evset)
max_printed_indexes = int(os.environ.get("TEMPORIAN_MAX_PRINTED_INDEXES", 5))
"""Maximum number of index values to show when printing an EventSet."""
max_printed_features = int(os.environ.get("TEMPORIAN_MAX_PRINTED_FEATURES", 10))
"""Maximum number of features to show when printing an EventSet."""
max_printed_events = int(os.environ.get("TEMPORIAN_MAX_PRINTED_EVENTS", 20))
"""Maximum number of events to show when printing an EventSet."""

# Limits for html display of evsets (notebooks)
max_display_indexes = int(os.environ.get("TEMPORIAN_MAX_DISPLAY_INDEXES", 5))
"""Maximum number of index values to show when displaying an EventSet in a
notebook."""
max_display_features = int(os.environ.get("TEMPORIAN_MAX_DISPLAY_FEATURES", 20))
"""Maximum number of features to show when displaying an EventSet in a
notebook."""
max_display_events = int(os.environ.get("TEMPORIAN_MAX_DISPLAY_EVENTS", 20))
"""Maximum number of events to show per index value when displaying an EventSet
in a notebook."""
max_display_chars = int(os.environ.get("TEMPORIAN_MAX_DISPLAY_CHARS", 32))
"""Maximum number of characters to show per cell when displaying an EventSet in
a notebook."""

# Configs for both repr and html
# Decimal numbers precision
print_precision = int(os.environ.get("TEMPORIAN_PRINT_PRECISION", 4))
"""Number of decimal places to show when printing a float value."""
