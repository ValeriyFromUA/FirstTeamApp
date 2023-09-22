import os
from FTApp import create_app, db

app = create_app(config_name='development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
