"""Website download manager for HTML/CSS/JS files"""
import os
import re
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class DownloadManager:
    """Manages downloading and caching website files"""
    
    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_url_hash(self, url):
        """Generate hash for URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def download_website(self, url, game_name):
        """Download website HTML, CSS, and JS files"""
        if BeautifulSoup is None:
            return {
                'success': False,
                'error': 'BeautifulSoup4 is not installed. Please install it with: pip install beautifulsoup4'
            }
        
        try:
            # Create game-specific directory
            game_dir = self.cache_dir / self.get_url_hash(url)
            game_dir.mkdir(exist_ok=True, parents=True)
            
            # Download main HTML
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Save original HTML
            html_file = game_dir / "index.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Download and replace CSS links
            css_files = []
            for link in soup.find_all('link', rel='stylesheet'):
                href = link.get('href')
                if href:
                    css_url = urljoin(url, href)
                    css_path = self._download_file(css_url, game_dir, 'css')
                    if css_path:
                        css_files.append(css_path)
                        link['href'] = str(css_path.relative_to(game_dir))
            
            # Download and replace JS scripts
            js_files = []
            for script in soup.find_all('script', src=True):
                src = script.get('src')
                if src:
                    js_url = urljoin(url, src)
                    js_path = self._download_file(js_url, game_dir, 'js')
                    if js_path:
                        js_files.append(js_path)
                        script['src'] = str(js_path.relative_to(game_dir))
            
            # Download images
            img_files = []
            for img in soup.find_all('img', src=True):
                src = img.get('src')
                if src and not src.startswith('data:'):
                    img_url = urljoin(url, src)
                    img_path = self._download_file(img_url, game_dir, 'images')
                    if img_path:
                        img_files.append(img_path)
                        img['src'] = str(img_path.relative_to(game_dir))
            
            # Save modified HTML
            modified_html = str(soup)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(modified_html)
            
            return {
                'success': True,
                'html_file': html_file,
                'css_files': css_files,
                'js_files': js_files,
                'img_files': img_files,
                'base_dir': game_dir
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _download_file(self, url, base_dir, file_type):
        """Download a single file"""
        try:
            # Create subdirectory for file type
            subdir = base_dir / file_type
            subdir.mkdir(exist_ok=True)
            
            # Get filename from URL
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or f"file_{self.get_url_hash(url)}"
            
            # Clean filename
            filename = re.sub(r'[^\w\.-]', '_', filename)
            
            file_path = subdir / filename
            
            # Skip if already downloaded
            if file_path.exists():
                return file_path
            
            # Download file
            response = self.session.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return file_path
        except:
            return None
    
    def get_local_path(self, url):
        """Get local path for downloaded website"""
        game_dir = self.cache_dir / self.get_url_hash(url)
        html_file = game_dir / "index.html"
        if html_file.exists():
            return html_file
        return None
    
    def is_downloaded(self, url):
        """Check if website is downloaded"""
        return self.get_local_path(url) is not None
    
    def get_download_size(self, url):
        """Get total size of downloaded files"""
        game_dir = self.cache_dir / self.get_url_hash(url)
        if not game_dir.exists():
            return 0
        
        total_size = 0
        for file_path in game_dir.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        return total_size
    
    def clear_cache(self, url=None):
        """Clear cache for a specific URL or all cache"""
        if url:
            game_dir = self.cache_dir / self.get_url_hash(url)
            if game_dir.exists():
                import shutil
                shutil.rmtree(game_dir)
                return True
        else:
            # Clear all cache
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(exist_ok=True, parents=True)
                return True
        return False
    
    def get_cache_info(self):
        """Get information about cached games"""
        if not self.cache_dir.exists():
            return {'count': 0, 'total_size': 0, 'games': []}
        
        games = []
        total_size = 0
        
        for game_dir in self.cache_dir.iterdir():
            if game_dir.is_dir():
                size = sum(f.stat().st_size for f in game_dir.rglob('*') if f.is_file())
                total_size += size
                games.append({
                    'path': str(game_dir),
                    'size': size,
                    'size_mb': size / (1024 * 1024)
                })
        
        return {
            'count': len(games),
            'total_size': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'games': games
        }

