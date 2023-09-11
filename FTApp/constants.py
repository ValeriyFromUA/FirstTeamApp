import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET_KEY')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
CV_DIR = os.path.join(STATIC_DIR, 'cv')
TEAM_LOGO_DIR = os.path.join(STATIC_DIR, 'team_logo')
CANDIDATE_PIC_DIR = os.path.join(STATIC_DIR, 'candidate_pic')
