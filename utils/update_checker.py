"""Update checker thread"""
import requests
from PyQt6.QtCore import QThread, pyqtSignal


class UpdateChecker(QThread):
    """Thread for checking updates"""
    update_available = pyqtSignal(str, str, dict)  # version, url, release_data
    no_update = pyqtSignal()
    
    def __init__(self, current_version, repo_url):
        super().__init__()
        self.current_version = current_version
        self.repo_url = repo_url
    
    def compare_versions(self, v1, v2):
        """Compare two version strings properly"""
        try:
            # Try using packaging library if available
            try:
                from packaging import version
                return version.parse(v1) > version.parse(v2)
            except ImportError:
                pass
            
            # Fallback to manual comparison
            v1_parts = [int(x) for x in v1.split('.')]
            v2_parts = [int(x) for x in v2.split('.')]
            # Pad shorter version with zeros
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            return v1_parts > v2_parts
        except:
            # Last resort: string comparison
            return v1 > v2
    
    def run(self):
        try:
            parts = self.repo_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                api_url = f"https://api.github.com/repos/{parts[0]}/{parts[1]}/releases/latest"
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data.get('tag_name', '').replace('v', '').replace('V', '')
                    current_version = self.current_version.replace('v', '').replace('V', '')
                    
                    # Properly compare versions
                    if latest_version and self.compare_versions(latest_version, current_version):
                        self.update_available.emit(latest_version, data.get('html_url', ''), data)
                    else:
                        self.no_update.emit()
                else:
                    self.no_update.emit()
            else:
                self.no_update.emit()
        except Exception as e:
            print(f"Update check error: {e}")
            self.no_update.emit()

