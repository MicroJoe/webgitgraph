import os
import io

from pygit2 import clone_repository, discover_repository, Repository, GitError
from flask import Flask, request, make_response

import settings
import gitgraph

app = Flask(__name__)


def text(*argc, **argv):
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
        return text('url must not be terminated by a slash', 400)

    repo_path = os.path.join(settings.REPOS_DIR, repo_name + '.git')

    if os.path.exists(repo_path):
        repo_path = discover_repository(repo_path)
        repo = Repository(repo_path)

        # try:
        #    origin = repo.remotes[0]
        # except IndexError:
        #    return text('no remote')

        # origin.fetch()

        data = gitgraph.retrieve_repo_activity(repo)['continuous_days_commits']

        res = io.StringIO()
        gitgraph.draw_activity([day for day in data], res)

        return res.getvalue()

    try:
        # We only need a bare repository, not a full workdir
        repo = clone_repository(repo_url, repo_path, bare=True)
    except GitError as e:
        return text(str(e), 400)
    except Exception as e:
        return text(str(e), 400)

    return 'cloned'


if __name__ == "__main__":
    app.run(debug=True)
