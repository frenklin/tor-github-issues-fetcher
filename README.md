# tor-github-issues-fetcher
example app scalable git-hub issue fetcher (for scale move queues to redis and spawn more processes)

1. tor or some round robin sock proxy, python3, queue, threading, urllib, ssl, sqlite3 is required
2. append torrc MaxCircuitDirtiness 15
3. set prject_url = '/repos/REPO_URL'
4. run python main.py
5. go sleep
6. check main.db database

may be useful for someone who needs data for machine learning or some analytics
