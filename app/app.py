import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dork_scrap import url_parse, start
from google_scrap import google_search
from flask import Flask, render_template, request, Response, stream_with_context
import json
import queue
import threading

app = Flask(__name__)

WORKERS = 5


@app.route('/')
def home():
    return render_template('index.html', page_title="Google Dorking Tool")


@app.route('/search')
def search():
    domain = request.args.get('domain', '').strip()
    try:
        workers = int(request.args.get('workers', WORKERS))
        workers = max(1, min(workers, 20))
    except ValueError:
        workers = WORKERS

    if not domain:
        return Response(
            "data: " + json.dumps({"error": "No domain provided"}) + "\n\n",
            mimetype='text/event-stream'
        )

    def generate():
        result_q = queue.Queue()
        dork_q   = queue.Queue()
        total_dorks   = 0
        total_results = 0
        scrape_done   = threading.Event()

        def worker():
            while True:
                item = dork_q.get()
                if item is None:
                    dork_q.task_done()
                    break
                dork = item
                try:
                    results = google_search(dork)
                    result_q.put(("results", dork, results))
                except Exception as e:
                    result_q.put(("error", dork, str(e)))
                finally:
                    dork_q.task_done()

        def scraper():
            for x in range(1, 8000):
                dorks = start(url_parse(x), domain)
                for dork in dorks:
                    result_q.put(("dork", dork, None))
                    dork_q.put(dork)
            for _ in range(workers):
                dork_q.put(None)
            scrape_done.set()

        thread_pool = [threading.Thread(target=worker, daemon=True) for _ in range(workers)]
        for t in thread_pool:
            t.start()

        scraper_thread = threading.Thread(target=scraper, daemon=True)
        scraper_thread.start()

        finished_workers = 0
        while finished_workers < workers or not result_q.empty():
            try:
                msg = result_q.get(timeout=1)
            except queue.Empty:
                if scrape_done.is_set() and not any(t.is_alive() for t in thread_pool):
                    break
                continue

            kind = msg[0]

            if kind == "dork":
                total_dorks += 1
                yield f"data: {json.dumps({'type': 'dork', 'dork': msg[1], 'count': total_dorks})}\n\n"

            elif kind == "results":
                dork, results = msg[1], msg[2]
                for title, link, snippet in results:
                    total_results += 1
                    payload = {
                        "type": "result",
                        "dork": dork,
                        "title": title,
                        "link": link,
                        "snippet": snippet,
                        "count": total_results,
                    }
                    yield f"data: {json.dumps(payload)}\n\n"

            elif kind == "error":
                yield f"data: {json.dumps({'type': 'search_error', 'dork': msg[1], 'error': msg[2]})}\n\n"

        scraper_thread.join(timeout=5)
        yield f"data: {json.dumps({'type': 'done', 'dorks': total_dorks, 'results': total_results})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
