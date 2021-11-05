from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QWidget

from db_toolobox.filesystem_utils import Paths
from db_toolobox.temperature_distribution_wgt import TemperatureDistWgt


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)
        central_layout = QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.tab_widget = QTabWidget(self.central_widget)
        central_layout.addWidget(self.tab_widget)

        self.temperature_dist_wgt = TemperatureDistWgt(
            self.tab_widget,
            html_path=Path(Paths.energy_plus_dir, "eplustbl.htm"),
            output_dir=Paths.energy_plus_dir,
        )

        self.tab_widget.addTab(self.temperature_dist_wgt, "Temperature distribution")
        self.setMinimumSize(600, 400)
