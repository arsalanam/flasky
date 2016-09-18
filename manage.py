


#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,  Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

appl = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(appl)
migrate = Migrate(appl, db)





def make_shell_context():
    return dict(appl=appl, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()