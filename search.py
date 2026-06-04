from dork_scrap import url_parse, start
from google_scrap import google_search
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Hacking Dorks")
    parser.add_argument('-d', '--domain', required=False, help='Target domain (e.g. example.com)')
    parser.add_argument('-brows', '--brows', action='store_true', help='Run in browser mode (launches Flask UI)')
    args = parser.parse_args()

    if args.brows:
        # Launch the Flask web UI
        import webbrowser
        import threading
        from app.app import app

        def open_browser():
            webbrowser.open("http://127.0.0.1:5000")

        threading.Timer(1.2, open_browser).start()
        print("[*] Starting browser UI at http://127.0.0.1:5000 ...")
        app.run(debug=False)

    else:
        if not args.domain:
            parser.error("argument -d/--domain is required in CLI mode")

        for x in range(1, 8000):
            dorks = start(url_parse(x), args.domain)
            for dork in dorks:
                google_search(dork)
