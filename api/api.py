import os
# from app.blueprints.sql.models import IPAddress
from app.blueprints.mongo.models import IPAddress
# from app import create_app, db, cli
from app import create_app, sql_db

import os
from dotenv import load_dotenv

def find_env_file():
    current_dir = os.getcwd()
    while True:
        env_file_path = os.path.join(current_dir, '.env')
        if os.path.isfile(env_file_path):
            return env_file_path
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            return None
        current_dir = parent_dir

dotenv_path = find_env_file()
if dotenv_path:
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': sql_db,
        'IPAddress': IPAddress,
    }

if __name__ == "__main__":
    app.run(port=5005, debug=True, host="0.0.0.0")