import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from dork_scrap import url_parse, start
from google_scrap import google_search
from flask import Flask, render_template, request, Response, stream_with_context
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', page_title="Google Dorking Tool")


@app.route('/search')
def search():
    domain = request.args.get('domain', '').strip()
    if not domain:
        return Response("data: " + json.dumps({"error": "No domain provided"}) + "\n\n",
                        mimetype='text/event-stream')

    def generate():
        total_dorks = 0
        total_results = 0

        for x in range(1, 8000):
            dorks = start(url_parse(x), domain)
            if not dorks:
                continue

            for dork in dorks:
                total_dorks += 1
                yield f"data: {json.dumps({'type': 'dork', 'dork': dork, 'count': total_dorks})}\n\n"

                results = google_search(dork)
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

        yield f"data: {json.dumps({'type': 'done', 'dorks': total_dorks, 'results': total_results})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
