from pathlib import Path
import pytest
from typer.testing import CliRunner

from lorcania_cli.main import app

runner = CliRunner()


@pytest.mark.vcr()
def test_without_out_file():
    result = runner.invoke(app, ["collection", "show"])
    assert result.exit_code == 0
    assert "collection" in result.stdout


@pytest.mark.vcr()
def test_with_out_file(tmp_path: Path):
    out_file = tmp_path / "collection.xlsx"
    result = runner.invoke(app, ["collection", "show", "--out-file", str(out_file)])
    assert result.exit_code == 0
    assert out_file.is_file()
