from flask import Blueprint

company_bp = Blueprint('company', __name__)

from . import company
