from GitHubData import GitHubData
from Storage import Storage
from GitHubDataActor import GitHubDataActor
from StorageActor import StorageActor
from queue import Queue
from threading import Thread
import time
import sys


# fetch -> validate(store) -> fetch -> store

project_url = '/repos/Microsoft/vscode'
sock_proxy_host = 'localhost'
sock_proxy_port = 9050

queues = {'fetch':Queue(), 'store':Queue()}

workers = []

for x in range(16):
    worker = GitHubDataActor(queues['fetch'], queues, sock_proxy_host, sock_proxy_port)
    worker.daemon = True
    worker.start()
    workers.append(worker)

worker = StorageActor(queues['store'], queues)
worker.daemon = True
worker.start()
workers.append(worker)

queues['fetch'].put(('project_validate', {'project_url': project_url})) #next_queue, link, table_name, extra_data

time.sleep(15)

queues['store'].join()
queues['fetch'].join()
queues['store'].join()


print('Done!')
