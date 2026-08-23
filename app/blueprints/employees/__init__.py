from flask import Blueprint
emp_bp = Blueprint('employees', __name__)
from . import routes  # noqa
