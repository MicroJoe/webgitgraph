import os

from pygit2 import clone_repository, GitError
from flask import Flask, request, make_response

import settings

app = Flask(__name__)


def return_text(*argc, **argv):
    resp = make_response(*argc, **argv)
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/')
def home():
    return 'webgitgraph 0.1'


@app.route('/svg/')
def repo():
    repo_url = request.args.get('url', '')

    if not repo_url:
        return 'pls give url'

    repo_name = repo_url.split('/')[-1]

    if not repo_name:
        return_text('url must not be terminated by a slash', 400)

    repo_path = os.path.join(settings.REPOS_DIR, repo_name)

    try:
        clone_repository(repo_url, repo_path)
    except GitError as e:
        resp = make_response(str(e), 400)
        resp.headers['Content-Type'] = 'text/plain'
        return resp
    except Exception as e:
        resp = make_response(str(e), 400)
        resp.headers['Content-Type'] = 'text/plain'
        return resp

    return 'cloned'


if __name__ == "__main__":
    app.run(debug=True)
