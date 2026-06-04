from dork_scrap import url_parse, start
from google_scrap import google_search
import argparse
import queue
import threading


def run_threaded(domain, workers):
    dork_q = queue.Queue()
    total_results = 0
    lock = threading.Lock()

    def worker():
        nonlocal total_results
        while True:
            dork = dork_q.get()
            if dork is None:        # poison pill
                dork_q.task_done()
                break
            try:
                results = google_search(dork)
                with lock:
                    total_results += len(results)
            except Exception as e:
                print(f"[!] Error on '{dork}': {e}")
            finally:
                dork_q.task_done()

    pool = [threading.Thread(target=worker, daemon=True) for _ in range(workers)]
    for t in pool:
        t.start()

    total_dorks = 0
    for x in range(1, 8000):
        dorks = start(url_parse(x), domain)
        for dork in dorks:
            total_dorks += 1
            dork_q.put(dork)

    for _ in range(workers):
        dork_q.put(None)
    dork_q.join()

    print(f"\n[✓] Done — {total_dorks} dorks, {total_results} results")


def run_single(domain):
    for x in range(1, 8000):
        dorks = start(url_parse(x), domain)
        for dork in dorks:
            google_search(dork)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Hacking Dorks")
    parser.add_argument('-d', '--domain', required=False, help='Target domain (e.g. example.com)')
    parser.add_argument('-brows', '--brows', action='store_true', help='Run in browser mode (launches Flask UI)')
    parser.add_argument('-t', '--threads', type=int, metavar='N', default=1,
                        help='Number of parallel worker threads (e.g. -t 5)')
    args = parser.parse_args()

    if args.brows:
        import webbrowser
        from app.app import app

        def open_browser():
            webbrowser.open("http://127.0.0.1:5000")

        threading.Timer(1.2, open_browser).start()
        print("[*] Starting browser UI at http://127.0.0.1:5000 ...")
        app.run(debug=False, threaded=True)

    else:
        if not args.domain:
            parser.error("argument -d/--domain is required in CLI mode")

        workers = max(1, args.threads)

        if workers > 1:
            print(f"[*] Running with {workers} threads")
            run_threaded(args.domain, workers)
        else:
            run_single(args.domain)
