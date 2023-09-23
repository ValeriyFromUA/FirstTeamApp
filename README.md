![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Flask-Login](https://img.shields.io/badge/Flask--Login-%23000.svg?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-%23003B57.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Poetry](https://img.shields.io/badge/poetry-%231227B7.svg?style=for-the-badge&logo=python&logoColor=white)

# FirstTeamAPP

It's just an early version of the application, more features will be added in the future, but for now, only the basic
functionality is available.
This application is created to assist beginners in finding their first job in IT. FirstTeamAPP is exclusively targeted
at Candidates with no more than 1 year of experience.

Features:

- Candidates are automatically suggested to Employers if their skills meet the requirements set by the Team.
- In the list of Candidates, the Team only sees those recommended Candidates that match their capabilities, so they must
  create at least one Opportunity to initiate the search.
- Candidates only see Opportunities recommended to them, filtered by technology. For convenience, Opportunities from the
  Candidate's city are displayed first, followed by all others.

## Installation

1. Clone the repository:
   ```git clone https://github.com/ValeriyFromUA/FirstTeamApp.git```

2. Install the dependencies: ```poetry install```

3. Create an `.env` file. and add your own data following the structure of the `.env_example` file.
4. Adjust the configuration if needed in `FTApp/config.py`
5. Run `data_for_db.py` to create database and add data.
6. Run `run.py` to start application

## Running with Docker ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

1. Make sure your system is working with Make and Docker. If not, install Make and/or Docker on your system.
2. To run the application using docker, use `make quick_run`. This command will automatically mount and run the image.

If necessary, you can create `make build` and run `make run` the image separately.
More in Makefile.

### Possible errors with older versions of FirstTeamAPP:

If you have error:

```commandline
File "/home/valerii/.cache/pypoetry/virtualenvs/firstteamapp-gc46IiXx-py3.8/lib/python3.8/site-packages/flask_uploads.py", line 26, in <module>
    from werkzeug import secure_filename, FileStorage
```

change in flask_uploads.py:

```commandline
from werkzeug import secure_filename, FileStorage
```

to

```commandline
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
```

or install a new app from this repository.

### If you require more details or clarifications, feel free to contact me:

- Telegram: [@FR0M_UA](https://t.me/FR0M_UA)
- email: [hitehnik132@gmail.com](mailto:hitehnik132@gmail.com)