from flask import render_template
from . import company_bp

@company_bp.route('/')
def view():
    return render_template('company/view.html')
