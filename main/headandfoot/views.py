import json
import logging
import datetime
import requests

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .models import PublicExperience
from openhumans.models import OpenHumansMember
import io
import uuid

logger = logging.getLogger(__name__)


