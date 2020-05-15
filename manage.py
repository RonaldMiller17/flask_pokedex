import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from database import init_db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('', MigrateCommand)
# manager.add_command('initdb', init_db)

if __name__ == "__main__":
    manager.run()