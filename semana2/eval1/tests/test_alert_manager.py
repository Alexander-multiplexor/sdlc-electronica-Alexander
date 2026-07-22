from pathlib import Path

import pytest

from semana2.eval1.src.alert_manager import (
    AlertManager,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)


def test_alert_manager_despacha_a_consola_y_archivo(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    log_file = tmp_path / "alerts.log"
    manager = AlertManager()
    manager.add_strategy(ConsoleAlertStrategy())
    manager.add_strategy(FileAlertStrategy(log_file))

    manager.notify("ALERTA: TEMPERATURA_ALTA en TEMP-01")

    # Verificar salida en consola
    captured = capsys.readouterr()
    assert "ALERTA: TEMPERATURA_ALTA en TEMP-01" in captured.out

    # Verificar escritura en archivo
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "ALERTA: TEMPERATURA_ALTA en TEMP-01" in content