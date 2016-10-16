


#!/usr/bin/env python3
import os
from app import create_app, db

from flask import g
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_login import  current_user
from flaskext.markdown import Markdown




from flask_bcrypt import Bcrypt


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
markdown=Markdown(app,extensions=['nl2br','tables','extra'])




@app.before_request
def _before_request():
    g.user = current_user



def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()