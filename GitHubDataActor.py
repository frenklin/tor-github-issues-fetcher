from GitHubData import GitHubData
from threading import Thread


class GitHubDataActor(Thread):

    def __init__(self, queue, queues, sock_proxy_host, sock_proxy_port):
        Thread.__init__(self)
        self.queue = queue
        self.queues = queues
        self._gitHubConnection = GitHubData(sock_proxy_host, sock_proxy_port)


    def run(self):
        while True:
            table_name, extra_data = self.queue.get()
            try:
                json_data = {}
                if table_name == 'issue':
                    #print('GitHubDataActor issue = {}'.format(extra_data['id_issue']))
                    json_data['issue_json'] = self._gitHubConnection.getGitHubData('{}/issues/{}'.format(extra_data['project_url'], extra_data['id_issue']))
                    json_data['events_json'] = self._gitHubConnection.getGitHubData('{}/issues/{}/events?event=assigned'.format(extra_data['project_url'], extra_data['id_issue']))
                    json_data['comments_json'] = self._gitHubConnection.getGitHubData('{}/issues/{}/comments'.format(extra_data['project_url'], extra_data['id_issue']))
                    self.queues['store'].put((table_name, json_data, extra_data))
                elif table_name == 'project_validate':
                    #print('GitHubDataActor project_validate = {}'.format(extra_data['project_url']))
                    data = dict(extra_data)
                    json_data['project_json'] = self._gitHubConnection.getGitHubData(extra_data['project_url'])
                    data['id_project'] = json_data['project_json']['id']
                    self.queues['store'].put((table_name, json_data, data))
                elif table_name == 'project':
                    #print('GitHubDataActor project = {}'.format(extra_data['project_url']))
                    pages_loading = True
                    page_number = 1
                    while pages_loading:
                        issues = self._gitHubConnection.getGitHubData(extra_data['project_url'] + '/issues?state=closed&page={}&per_page=100'.format(page_number))

                        print('GitHubDataActor project page = {} count = {}'.format(page_number, len(issues)))

                        if len(issues) == 0:
                            pages_loading = False
                            break

                        for issue in issues:
                            data = dict(extra_data)
                            data['id_issue'] = issue['number']
                            self.queues['store'].put(('issue_validate', '', data))

                        page_number += 1
            except BaseException as e:
                print('GitHubDataActor Error')
                print(e)
                print(extra_data)

            self.queue.task_done()
