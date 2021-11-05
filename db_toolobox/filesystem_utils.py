import os
from pathlib import Path
from typing import List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStyle,
    QWidget,
)

from db_toolobox.misc_widgets import IconSize


class Paths:
    design_builder_dir = Path(os.path.expandvars("%LOCALAPPDATA%/DesignBuilder"))
    energy_plus_dir = Path(design_builder_dir, "EnergyPlus")


def create_extension_string(extensions: Optional[List[str]]) -> str:
    """Create qt compatible extension string."""
    return " ".join(["*" + ext for ext in extensions]) if extensions else "*.*"


def stringify_path(path: Optional[Path]) -> str:
    """Convert optional path to string."""
    return str(path) if path else ""


def get_open_paths_from_fs(
    parent: QWidget,
    caption: str,
    base_path: Optional[Path],
    extensions: Optional[List[str]],
) -> Optional[List[Path]]:
    """Let user select files from filesystem."""
    extensions_str = create_extension_string(extensions)
    file_paths, _ = QFileDialog.getOpenFileNames(
        parent=parent,
        caption=caption,
        filter=f"FILES ({extensions_str})",
        dir=stringify_path(base_path),
    )
    return [Path(path) for path in file_paths] if file_paths else None


def get_open_path_from_fs(
    parent: QWidget,
    caption: str,
    base_path: Optional[Path],
    extensions: Optional[List[str]],
) -> Optional[Path]:
    """Let user select a single file from filesystem."""
    extensions_str = create_extension_string(extensions)
    file_path, _ = QFileDialog.getOpenFileName(
        parent=parent,
        caption=caption,
        filter=f"FILES ({extensions_str})",
        dir=stringify_path(base_path),
    )
    return Path(file_path) if file_path else None


def get_save_path_from_fs(
    parent: QWidget, caption: str, base_path: Optional[Path], extension: str
) -> Optional[Path]:
    """Let user select a single file from filesystem."""
    file_path, _ = QFileDialog.getSaveFileName(
        parent=parent,
        caption=caption,
        filter=f"CFS (*{extension})",
        dir=stringify_path(base_path),
    )
    return Path(file_path) if file_path else None


def get_dir_path_from_fs(
    parent: QWidget, caption: str, base_path: Optional[Path]
) -> Optional[Path]:
    """Let user select a single directory from filesystem."""
    dir_path = QFileDialog.getExistingDirectory(
        parent=parent,
        caption=caption,
        dir=stringify_path(base_path),
        options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
    )
    return Path(dir_path) if dir_path else None


class FileSelector(QWidget):
    """
    Compound widget to prompt user to select file path on button click.
    Widget label displays current selection.

    Parameters
    ----------
    parent : QWidget
        Parent widget.
    extensions : list of str
        Allowed extensions in filesystem dialog, example ['.html', '.py'].
    caption : str
        Text to be displayed as a title of filesystem dialog.
    current_path : Path, optional
        Initial placeholder of the filesystem dialog input.

    """

    pathChanged = Signal(Path)

    def __init__(
        self,
        parent: QWidget,
        caption: str = "Select file",
        extensions: Optional[List[str]] = None,
        current_path: Optional[Path] = None,
    ):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.extensions = extensions
        self.caption = caption
        self.label = QLabel(self)
        self.label.setObjectName("pathLabel")
        self.button = QPushButton(self)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.button.setIconSize(IconSize.SMALL)
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button.clicked.connect(self.change_path)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignRight)
        self.current_path = current_path

    @property
    def current_path(self) -> Optional[Path]:
        """Currently selected directory."""
        return Path(self.label.text()) if self.label.text() else None

    @current_path.setter
    def current_path(self, path: Path) -> None:
        """Set current directory (updates label)."""
        self.label.setText(str(path))

    def change_path(self) -> None:
        """Allow user to change directory using native filesystem dialog."""
        path = get_open_path_from_fs(
            self, self.caption, self.current_path, self.extensions
        )
        if path and path != self.current_path:
            self.current_path = path
            self.pathChanged.emit(path)


class DirSelector(QWidget):
    """
    Compound widget to prompt user to select directory path on button click.
    Widget label displays current selection.

    Parameters
    ----------
    parent : QWidget
        Parent widget.
    caption : str
        Text to be displayed as a title of filesystem dialog.
    current_dir : Path, optional
        Initial placeholder of the filesystem dialog input.

    """

    directoryChanged = Signal(Path)

    def __init__(
        self,
        parent: QWidget,
        caption: str = "Select directory",
        current_dir: Optional[Path] = None,
    ):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.caption = caption
        self._current_dir = current_dir
        self.label = QLabel(self)
        self.label.setObjectName("pathLabel")
        self.button = QPushButton(self)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.button.setIconSize(IconSize.SMALL)
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button.clicked.connect(self.change_directory)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignRight)

    @property
    def current_dir(self) -> Optional[Path]:
        """Currently selected directory."""
        return Path(self.label.text()) if self.label.text() else None

    @current_dir.setter
    def current_dir(self, path: Path) -> None:
        """Set current directory (updates label)."""
        self.label.setText(str(path))

    def change_directory(self) -> None:
        """Allow user to change directory using native filesystem dialog."""
        path = get_dir_path_from_fs(self, self.caption, self.current_dir)
        if path and path != self.current_dir:
            self.current_dir = path
            self.directoryChanged.emit(path)
