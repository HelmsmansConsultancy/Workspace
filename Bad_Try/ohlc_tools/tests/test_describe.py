"""Tests for ohlc_tools.commands.describe."""

from click.testing import CliRunner
from ohlc_tools.commands.describe import cli


class TestDescribeCli:
    def test_runs_successfully(self, sample_h1_csv):
        runner = CliRunner()
        result = runner.invoke(cli, [sample_h1_csv])
        assert result.exit_code == 0

    def test_output_contains_key_fields(self, sample_h1_csv):
        runner = CliRunner()
        result = runner.invoke(cli, [sample_h1_csv, "--no-color"])
        output = result.output
        assert "File size"  in output
        assert "Timeframe"  in output
        assert "Timezone"   in output
        assert "Start date" in output
        assert "End date"   in output

    def test_missing_file_exits_nonzero(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(cli, [str(tmp_path / "missing.csv")])
        assert result.exit_code != 0
