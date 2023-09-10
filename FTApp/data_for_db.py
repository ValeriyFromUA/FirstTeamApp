from FTApp import db
from FTApp.models import City, English, Experience, Specialisation
from FTApp.run import app

CITY_LIST = [
    'Вінниця',
    'Дніпро',
    'Донецьк',
    'Житомир',
    'Запоріжжя',
    'Івано-Франківськ',
    'Київ',
    'Кропивницький',
    'Луганськ',
    'Луцьк',
    'Львів',
    'Миколаїв',
    'Одеса',
    'Полтава',
    'Рівне',
    'Севастополь',
    'Суми',
    'Тернопіль',
    'Ужгород',
    'Харків',
    'Херсон',
    'Хмельницький',
    'Черкаси',
    'Чернівці',
    'Чернігів'
]

LANG_LEVELS = [
    'Beginner (A1)',
    'Elementary (A2)',
    'Pre-Intermediate (B1)',
    'Intermediate (B2)',
    'Upper-Intermediate (C1)',
    'Advanced (C2)',
    'Fluent (C2)',
    'Native Speaker'
]

EXP_LEVEL = [
    'Без досвіду',
    'Менше 1 року',
    '1 рік',
]

SPECIALISATIONS = [
    'Python',
    'JavaScript',
    'Java',
    'C++',
    'C#',
    'Ruby',
    'PHP',
    'Swift',
    'Kotlin',
    'TypeScript',
    'Go (Golang)',
    'Rust',
    'MATLAB',
    'Perl',
    'Dart',
    'R',
    'Scala',
    'Lua',
    'Bash (Shell)',
    'HTML',
    'CSS',
    'Objective-C',
    'Haskell',
    'Groovy',
    'Elixir',
    'Clojure',
    'VHDL',
    'COBOL',
    'Delphi',
    'Pascal',
    '1C',
    'QA (Quality Assurance)',
    'Manual QA',
    'Automation QA',
    'Design / UI/UX',
    '2D/3D Artist / Illustrator',
    'Project Manager',
    'Product Manager',
    'Architect / CTO (Chief Technology Officer)',
    'DevOps',
    'Business Analyst',
    'Data Science',
    'Data Analyst',
    'Sysadmin (System Administrator)',
    'Gamedev / Unity',
    'SQL / DBA (Database Administrator)',
    'Security',
    'Data Engineer',
    'Scrum Master / Agile Coach'
]


def add_data_to_database():
    for city_name in CITY_LIST:
        city = City(name=city_name)
        db.session.add(city)

    for level_name in LANG_LEVELS:
        english_level = English(level=level_name)
        db.session.add(english_level)

    for exp_name in EXP_LEVEL:
        experience_level = Experience(name=exp_name)
        db.session.add(experience_level)

    for spec_name in SPECIALISATIONS:
        specialisation = Specialisation(name=spec_name)
        db.session.add(specialisation)

    db.session.commit()


with app.app_context():
    db.create_all()
    add_data_to_database()
