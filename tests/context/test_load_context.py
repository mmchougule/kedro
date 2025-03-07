# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

import pytest

from kedro.context import KedroContextError, load_context


@pytest.fixture(autouse=True)
def restore_cwd():
    cwd_ = os.getcwd()
    yield
    os.chdir(cwd_)


@pytest.fixture
def fake_project(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    kedro_cli = project / "kedro_cli.py"
    script = """
def __get_kedro_context__():
    return "fake"
    """
    kedro_cli.write_text(script, encoding="utf-8")
    yield project


def test_load(fake_project, tmp_path):
    """Test getting project context"""
    result = load_context(str(fake_project))
    assert result == "fake"
    assert str(fake_project.resolve()) in sys.path
    assert os.getcwd() == str(fake_project.resolve())

    other_path = tmp_path / "other"
    other_path.mkdir()
    pattern = (
        "Cannot load context for `{}`, since another project "
        "`.*` has already been loaded".format(other_path.resolve())
    )
    with pytest.raises(KedroContextError, match=pattern):
        load_context(str(other_path))
