"""Tests for ohlc_tools.commands.resample."""

import os
from click.testing import CliRunner
from ohlc_tools.commands.resample import cli


class TestResampleCli:
    def test_h1_to_h4(self, sample_h1_csv, tmp_path):
        out = str(tmp_path / "out_h4.csv")
        runner = CliRunner()
        result = runner.invoke(cli, [sample_h1_csv, "--timeframe", "H4", "--output", out])
        assert result.exit_code == 0
        assert os.path.isfile(out)

    def test_invalid_timeframe(self, sample_h1_csv, tmp_path):
        out = str(tmp_path / "out.csv")
        runner = CliRunner()
        result = runner.invoke(cli, [sample_h1_csv, "--timeframe", "INVALID", "--output", out])
        assert result.exit_code != 0
