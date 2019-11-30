# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
SECRET = os.environ.get("LINE_CHANNEL_SECRET")
USER_ID = os.environ.get("USER_ID")