"""Fullscreen game window"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QKeySequence, QShortcut


class FullscreenGameWindow(QWidget):
    """Fullscreen window for playing games"""
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use proper fullscreen window flags
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Top bar (hidden by default, shown on mouse move)
        self.top_bar = QWidget()
        self.top_bar.setMaximumHeight(40)
        self.top_bar.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
        top_bar_layout = QHBoxLayout(self.top_bar)
        top_bar_layout.setContentsMargins(10, 5, 10, 5)
        
        self.exit_btn = QPushButton("✕ Exit Fullscreen (ESC)")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                color: black;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
            }
        """)
        self.exit_btn.clicked.connect(self.close)
        top_bar_layout.addWidget(self.exit_btn)
        top_bar_layout.addStretch()
        
        self.top_bar.hide()
        layout.addWidget(self.top_bar)
        
        # Web view - make it fill the entire screen
        self.web_view = QWebEngineView()
        self.web_view.setSizePolicy(
            Qt.SizePolicy.Policy.Expanding,
            Qt.SizePolicy.Policy.Expanding
        )
        layout.addWidget(self.web_view, stretch=1)
        
        # Shortcuts
        QShortcut(QKeySequence("Escape"), self, self.close)
        QShortcut(QKeySequence("F11"), self, self.toggle_fullscreen)
        
        # Mouse tracking for showing/hiding top bar
        self.setMouseTracking(True)
        self.top_bar_timer = QTimer()
        self.top_bar_timer.setSingleShot(True)
        self.top_bar_timer.timeout.connect(self.hide_top_bar)
        
        # Hide cursor after inactivity
        self.cursor_timer = QTimer()
        self.cursor_timer.setSingleShot(True)
        self.cursor_timer.timeout.connect(self.hide_cursor)
        self.last_mouse_move = None
    
    def set_url(self, url):
        """Set the URL to load"""
        self.web_view.setUrl(url)
        # Try to trigger fullscreen in the web content after page loads
        QTimer.singleShot(2000, self.request_game_fullscreen)
    
    def set_html(self, html):
        """Set HTML content"""
        self.web_view.setHtml(html)
        # Try to trigger fullscreen in the web content after page loads
        QTimer.singleShot(2000, self.request_game_fullscreen)
    
    def request_game_fullscreen(self):
        """Request fullscreen mode for the game content"""
        # Inject JavaScript to request fullscreen on the game canvas/container
        fullscreen_script = """
        (function() {
            // Try to find and request fullscreen on common game containers
            function requestFullscreen() {
                // Try canvas elements first (common in HTML5 games)
                var canvases = document.querySelectorAll('canvas');
                for (var i = 0; i < canvases.length; i++) {
                    var canvas = canvases[i];
                    if (canvas && (canvas.requestFullscreen || canvas.webkitRequestFullscreen || canvas.mozRequestFullScreen || canvas.msRequestFullscreen)) {
                        try {
                            if (canvas.requestFullscreen) {
                                canvas.requestFullscreen();
                            } else if (canvas.webkitRequestFullscreen) {
                                canvas.webkitRequestFullscreen();
                            } else if (canvas.mozRequestFullScreen) {
                                canvas.mozRequestFullScreen();
                            } else if (canvas.msRequestFullscreen) {
                                canvas.msRequestFullscreen();
                            }
                            console.log('Canvas fullscreen requested');
                            return;
                        } catch(err) {
                            console.log('Canvas fullscreen failed:', err);
                        }
                    }
                }
                
                // Try iframe
                var iframes = document.querySelectorAll('iframe');
                for (var i = 0; i < iframes.length; i++) {
                    var iframe = iframes[i];
                    try {
                        if (iframe.contentDocument || iframe.contentWindow) {
                            var doc = iframe.contentDocument || iframe.contentWindow.document;
                            var iframeCanvas = doc.querySelector('canvas');
                            if (iframeCanvas && iframeCanvas.requestFullscreen) {
                                iframeCanvas.requestFullscreen();
                                console.log('Iframe canvas fullscreen requested');
                                return;
                            }
                        }
                    } catch(e) {
                        console.log('Iframe access error:', e);
                    }
                }
                
                // Try game container divs
                var gameContainers = document.querySelectorAll('[id*="game"], [class*="game"], [id*="canvas"], [class*="canvas"]');
                for (var i = 0; i < gameContainers.length; i++) {
                    var container = gameContainers[i];
                    if (container && container.requestFullscreen) {
                        try {
                            container.requestFullscreen();
                            console.log('Game container fullscreen requested');
                            return;
                        } catch(err) {
                            console.log('Container fullscreen failed:', err);
                        }
                    }
                }
                
                // Try body or main container as last resort
                var body = document.body;
                if (body && (body.requestFullscreen || body.webkitRequestFullscreen)) {
                    try {
                        if (body.requestFullscreen) {
                            body.requestFullscreen();
                        } else if (body.webkitRequestFullscreen) {
                            body.webkitRequestFullscreen();
                        }
                        console.log('Body fullscreen requested');
                    } catch(err) {
                        console.log('Body fullscreen failed:', err);
                    }
                }
            }
            
            // Try immediately
            requestFullscreen();
            
            // Also try after delays in case elements load later
            setTimeout(requestFullscreen, 500);
            setTimeout(requestFullscreen, 1000);
            setTimeout(requestFullscreen, 2000);
            setTimeout(requestFullscreen, 3000);
            setTimeout(requestFullscreen, 5000);
        })();
        """
        self.web_view.page().runJavaScript(fullscreen_script)
    
    def showEvent(self, event):
        """Show fullscreen on show"""
        super().showEvent(event)
        # Show in true fullscreen mode
        self.showFullScreen()
        # Ensure web view takes full screen
        QTimer.singleShot(100, self.ensure_fullscreen)
    
    def ensure_fullscreen(self):
        """Ensure the window and content are in fullscreen"""
        if not self.isFullScreen():
            self.showFullScreen()
        # Request fullscreen for game content
        self.request_game_fullscreen()
    
    def mouseMoveEvent(self, event):
        """Show top bar on mouse move"""
        # Show cursor
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.cursor_timer.stop()
        
        # Show top bar when mouse is near top
        if event.pos().y() < 80:
            self.top_bar.show()
            self.top_bar_timer.stop()
        else:
            # Hide top bar after 2 seconds of mouse inactivity at top
            self.top_bar_timer.start(2000)
        
        # Hide cursor after 3 seconds of no movement
        self.cursor_timer.start(3000)
        
        super().mouseMoveEvent(event)
    
    def hide_top_bar(self):
        """Hide the top bar"""
        self.top_bar.hide()
    
    def hide_cursor(self):
        """Hide the cursor"""
        self.setCursor(Qt.CursorShape.BlankCursor)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            self.ensure_fullscreen()
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        # Ensure web view fills the screen
        self.web_view.setGeometry(0, 0, self.width(), self.height())
    
    def closeEvent(self, event):
        """Emit closed signal"""
        # Exit fullscreen before closing
        if self.isFullScreen():
            self.showNormal()
        self.closed.emit()
        super().closeEvent(event)

