from FTApp.logger import get_logger
from FTApp.run import app
from FTApp import db
from FTApp.models import City, English, Experience, Specialisation
from faker import Faker

fake = Faker('uk_UA')
CITY_LIST = [
    'Віддалена робота',
    'Вінниця',
    'Дніпро',
    'Донецьк',
    'Житомир',
    'Запоріжжя',
    'Івано-Франківськ',
    'Київ',
    'Кіровоград',
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
    'Чернігів',

]

LANG_LEVELS = [
    'No English',
    'Beginner/Elementary',
    'Pre-Intermediate',
    'Intermediate',
    'Upper-Intermediate',
    'Advanced/Fluent',
]

EXP_LEVEL = [
    'Без досвіду',
    'Менше року',
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

    for spec_name in list(sorted(SPECIALISATIONS)):
        specialisation = Specialisation(name=spec_name)
        db.session.add(specialisation)

    db.session.commit()


with app.app_context():
    db.create_all()
    add_data_to_database()
