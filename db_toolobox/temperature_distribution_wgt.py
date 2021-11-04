from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget

from db_toolobox.filesystem_utils import DirSelector, FileSelector


class TemperatureDistWgt(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.dir_selector = DirSelector(self)
        self.file_selector = FileSelector(self, extensions=[".htm", ".html"])

        self.run_script_button = QPushButton("Run", self)

        layout.addWidget(self.file_selector)
        layout.addWidget(self.dir_selector)
        layout.addWidget(self.run_script_button)
        layout.addStretch(1)

        self.run_script_button.clicked.connect(self.run_script)

    @property
    def html_path(self) -> Path:
        return self.file_selector.current_path

    @html_path.setter
    def html_path(self, path: Path) -> None:
        self.file_selector.current_path = path

    @property
    def output_dir(self) -> Path:
        return self.dir_selector.current_dir

    @output_dir.setter
    def output_dir(self, path: Path) -> None:
        self.dir_selector.current_dir = path

    def update_existing_directory(self) -> None:
        """Select output directory to store results."""
        if path := QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            str(self.output_dir),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        ):
            self.output_dir = Path(path)

    def update_existing_html(self) -> None:
        """Select html file to extract the results from."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File", str(self.html_path), "Summary file (*.htm *.html)"
        )
        if path:
            self.html_path = Path(path)

    def run_script(self) -> None:
        """Trigger script with current settings."""
