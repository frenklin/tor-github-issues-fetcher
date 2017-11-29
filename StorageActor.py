from Storage import Storage
from threading import Thread

class StorageActor(Thread):

    def __init__(self, queue, queues):
        Thread.__init__(self)
        self.queue = queue
        self.queues = queues

    def run(self):
        self.db = Storage()
        while True:
            table_name, json_data, extra_data = self.queue.get()
            try:

                if table_name == 'issue':
                    #print('StorageActor issue = {}'.format(extra_data['id_issue']))
                    print(".", end="")
                    self.db.insertIssue(id_issue = extra_data['id_issue'], id_project = extra_data['id_project'], issue_json = str(json_data['issue_json']), events_json = str(json_data['events_json']), comments_json = str(json_data['comments_json']))

                elif table_name == 'issue_validate':
                    #print('StorageActor issue_validate = {}'.format(extra_data['id_issue']))
                    if len(self.db.getIssue(id_project = extra_data['id_project'], id_issue = extra_data['id_issue']).fetchall()) == 0:
                        self.queues['fetch'].put(('issue', extra_data))

                elif table_name == 'project_validate':
                    #print('StorageActor project_validate = {}'.format(extra_data['id_project']))
                    if len(self.db.getProject(id_project=extra_data['id_project']).fetchall()) == 0:
                        self.db.insertProject(id_project=extra_data['id_project'], project_json=str(json_data['project_json']))
                    self.queues['fetch'].put(('project', extra_data))

                else:
                    raise BaseException('Unknown table_name in insert queue {}'.format(table_name))
                self.queue.task_done()

            except BaseException as e:
                print('StorageActor Error')
                print(e)
                print(extra_data)
