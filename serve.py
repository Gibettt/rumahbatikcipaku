#!/usr/bin/env python3
"""Static server for this mirror.

Plain http.server answers POST with a 501 error PAGE. Sites that fetch content
over POST inject that HTML into the DOM, which is where stray "ERROR RESPONSE"
blocks come from. Answer POST with an empty 200 instead -- the slot is already
inlined into the HTML at download time.
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


class MirrorHandler(SimpleHTTPRequestHandler):
    def _handle_custom_routes(self):
        # Serve any batik_assets request robustly
        if "batik_assets" in self.path:
            asset_filename = self.path.split("batik_assets/")[-1].split("?")[0]
            asset_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "batik_assets",
                asset_filename
            )
            if os.path.isfile(asset_path):
                try:
                    with open(asset_path, "rb") as f:
                        content = f.read()
                    ext = os.path.splitext(asset_filename)[1].lower()
                    mime = "image/jpeg"
                    if ext == ".png":
                        mime = "image/png"
                    elif ext == ".svg":
                        mime = "image/svg+xml"
                    elif ext == ".mp4":
                        mime = "video/mp4"
                    self.send_response(200)
                    self.send_header("Content-Type", mime)
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    if self.command != "HEAD":
                        self.wfile.write(content)
                    return True
                except Exception as e:
                    self.send_error(500, str(e))
                    return True

        # Redirect root to /id/
        if self.path in ("", "/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/id/")
            self.end_headers()
            return True

        # Serve global CSS for Demandware's VirtualStatic-GlobalCSS route
        if "VirtualStatic-GlobalCSS" in self.path:
            global_css_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "on/demandware.static/Sites-ck-idn-Site/-/in_ID/v1789349912533/css/global.css"
            )
            try:
                with open(global_css_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(content)
                return True
            except Exception as e:
                self.send_error(500, str(e))
                return True

        # Serve UGCGallery-List as JSON
        if "UGCGallery-List" in self.path:
            ugc_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "on/demandware.store/Sites-ck-idn-Site/in_ID/UGCGallery-List/index.html"
            )
            try:
                with open(ugc_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(content)
                return True
            except Exception as e:
                self.send_error(500, str(e))
                return True

        # Provide empty response for missing JS endpoints, trackers, and favicon
        if any(x in self.path for x in ("popup.js", "service-worker.js", "ConsentTracking", "favicon.ico")):
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return True

        return False

    def do_GET(self):
        if self._handle_custom_routes():
            return
        super().do_GET()

    def do_HEAD(self):
        if self._handle_custom_routes():
            return
        super().do_HEAD()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "GET, HEAD, POST, OPTIONS")
        self.end_headers()

    def log_message(self, fmt, *args):
        msg = fmt % args
        if " 404 " in msg or " 501 " in msg:
            sys.stderr.write("%s\n" % msg)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print("Serving on http://localhost:%d/" % port)
    HTTPServer(("127.0.0.1", port), MirrorHandler).serve_forever()
