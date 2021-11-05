from pathlib import Path
from typing import Dict

from db_temperature_distribution.parser import Table, process_time_bins
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QStyle,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from db_toolobox.filesystem_utils import DirSelector, FileSelector
from db_toolobox.misc_widgets import ErrorHandler, IconSize, ToolWidget, cursor_waiting


class TemperatureDistWgt(ToolWidget):
    """
    Tool to parse EnergyPlus time bin distribution tables.

    """

    description = """EnergyPlus reports temperature distribution time bins in great detail.
This utility extracts only the summary row."""

    def __init__(self, parent: QWidget, html_path: Path, output_dir: Path):
        super().__init__(parent, QVBoxLayout)
        self.dir_selector = DirSelector(self)
        self.dir_selector.current_dir = output_dir
        self.file_selector = FileSelector(self, extensions=[".htm", ".html"])
        self.file_selector.current_path = html_path

        self.update_results_btn = QPushButton(self)
        self.update_results_btn.setIcon(
            self.style().standardIcon(QStyle.SP_BrowserReload)
        )
        self.update_results_btn.setIconSize(IconSize.MEDIUM)
        self.update_results_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.content_layout.setAlignment(self.run_script_btn, Qt.AlignRight)

        self._model = QStandardItemModel()
        self.treeview = QTreeView(self)
        self.treeview.setModel(self._model)

        self.content_layout.addWidget(self.file_selector)
        self.content_layout.addWidget(self.dir_selector)
        self.content_layout.addWidget(self.treeview)
        self.content_layout.addStretch(1)
        self.content_layout.addWidget(self.update_results_btn)

        self.update_results_btn.clicked.connect(self.update_tables)

    def _set_tree_node_spanned(self) -> None:
        """Span all columns for tree nodes."""
        for i in range(self._model.rowCount()):
            self.treeview.setFirstColumnSpanned(i, QModelIndex(), True)

    def _clear_treeview(self) -> None:
        """Clear currently populated treeview."""
        self._model.clear()

    def _populate_treeview(self, all_time_bins: Dict[str, Table]):
        """Display parsed time bin data in treeview."""
        self._model.setColumnCount(12)
        for temperature, table in all_time_bins.items():
            parent_item = QStandardItem(temperature)
            for row in table:
                parent_item.appendRow([QStandardItem(str(cell)) for cell in row])
            self._model.appendRow(parent_item)

    @cursor_waiting
    def update_tables(self) -> None:
        """Trigger script with current settings."""
        html_path = self.file_selector.current_path
        with ErrorHandler(self):
            all_time_bins = process_time_bins(html_path)
            self._clear_treeview()
            self._populate_treeview(all_time_bins)
            self._set_tree_node_spanned()
