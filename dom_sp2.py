from datetime import date, datetime, timedelta
from os import getcwd, path, listdir, chdir
from tabula import read_pdf, environment_info, convert_into_by_batch
from PyPDF2 import PdfFileReader, PdfFileMerger
import base
import os
import fitz as fz
import tabula

dt_now = base.get_date_today()
BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES = base.get_directories()
YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM = base.get_info_dom()
DATA_FILES = base.rename_pages_dom()
