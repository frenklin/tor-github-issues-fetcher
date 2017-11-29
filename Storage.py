import sqlite3

class Storage:
    def __init__(self):
        self._db = sqlite3.connect('main.db')

        if len(self._db.execute('select * from sqlite_master').fetchall()) <= 0:
            self.createDatabase()

    def createDatabase(self):
        self._db.execute('CREATE TABLE projects(id INTEGER PRIMARY KEY, project_json TEXT)')
        self._db.execute('CREATE TABLE issues(id_issue INTEGER PRIMARY KEY, id_project INTEGER, issue_json TEXT, events_json TEXT, comments_json TEXT)')
        self._db.commit()

    def getProjects(self):
        return self._db.execute('SELECT id FROM projects')

    def getProject(self, id_project):
        return self._db.execute('SELECT id, project_json FROM projects WHERE id = ?', [id_project])

    def insertProject(self, id_project, project_json):
        self._db.execute('INSERT INTO projects(id, project_json) VALUES(?,?)',
                         [id_project, project_json])
        self._db.commit()

    def insertIssue(self, id_issue, id_project, issue_json, events_json, comments_json):
        self._db.execute('INSERT INTO issues(id_issue, id_project, issue_json, events_json, comments_json) VALUES(?, ?, ?, ?, ?)', [id_issue, id_project, issue_json, events_json, comments_json])
        self._db.commit()

    def getIssues(self, id_project):
        return self._db.execute('SELECT id_issue FROM issues WHERE id_project = ?', [id_project])

    def getIssue(self, id_project, id_issue):
        return self._db.execute('SELECT id_issue, id_project, issue_json, events_json, comments_json FROM issues WHERE id_issue = ? AND id_project = ?', [id_issue, id_project])

