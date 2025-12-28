"""File downloader utility"""
import os
import requests
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal, QObject


class FileDownloader(QThread):
    """Thread for downloading files"""
    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(str)  # filepath
    error = pyqtSignal(str)  # error message
    
    def __init__(self, url, destination_path):
        super().__init__()
        self.url = url
        self.destination_path = Path(destination_path)
        self.destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(self.destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            self.progress.emit(downloaded, total_size)
            
            self.finished.emit(str(self.destination_path))
        except Exception as e:
            self.error.emit(str(e))

