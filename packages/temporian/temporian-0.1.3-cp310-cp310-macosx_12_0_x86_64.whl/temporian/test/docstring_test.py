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
import sys
import doctest
import inspect
import traceback
import tempfile
from pathlib import Path

from absl.testing import absltest

import numpy as np
import pandas as pd
import temporian as tp


def or_zero(v):
    if v is None:
        return 0
    return v


class DocstringsTest(absltest.TestCase):
    """
    Tests all code examples included in docstrings, using builtin doctest module.
    E.g:
    >>> print("hello")
    hello

    """

    def test_docstrings(self):
        tested_modules = set()
        tmp_dir_handle = tempfile.TemporaryDirectory()
        tmp_dir = Path(tmp_dir_handle.name)

        for api_object in tp.__dict__.values():
            if inspect.ismodule(api_object):
                module = api_object
            else:
                module = inspect.getmodule(api_object)
                if module is None:
                    continue

            # Avoid testing twice
            module_name = module.__name__
            if "temporian" not in module_name or module_name in tested_modules:
                continue

            tested_modules.add(module.__name__)
            try:
                # Run with np,pd,tp + tmp_dir + module globals as exec context
                _, test_count = doctest.testmod(
                    module,
                    globs={"np": np, "tp": tp, "pd": pd, "tmp_dir": tmp_dir},
                    extraglobs=module.__dict__,
                    # Use ... to match anything and ignore different whitespaces
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
                    raise_on_error=True,
                    verbose=False,
                )
                if test_count:
                    print(f"Tested {test_count} doc examples on: {module_name}")
                else:
                    print(f"No examples in {module_name}")

            # Failure due to mismatch on expected result
            except doctest.DocTestFailure as e:
                test = e.test
                ex = e.example
                lineno = or_zero(test.lineno) + ex.lineno
                path = inspect.getfile(module)
                # Re-raise as bazel assertion
                self.assertEqual(
                    ex.want,
                    e.got,
                    (
                        f"Docstring example starting at line {lineno} failed"
                        f" on file {path}\n"
                        f">>> {ex.source}"
                    ),
                )

            # Failure due to exception raised during code execution
            except doctest.UnexpectedException as e:
                test = e.test
                ex = e.example
                lineno = or_zero(test.lineno) + ex.lineno
                path = inspect.getfile(module)
                print("\n\nTraceback:")
                traceback.print_tb(e.exc_info[2], file=sys.stdout)
                print("\n\n")
                # pylint: disable=raise-missing-from
                raise AssertionError(
                    "Exception running docstring example starting at line "
                    f"{lineno} on file {path}\n>>> {ex.source}{e.exc_info[0]}:"
                    f" {e.exc_info[1]}"
                )
                # pylint: enable=raise-missing-from
        tmp_dir_handle.cleanup()


if __name__ == "__main__":
    absltest.main()
