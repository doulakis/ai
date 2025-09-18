from flask import render_template, flash
from flask_login import login_required, current_user
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    """Home page"""
    return render_template('index.html', title='Home')


@bp.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard page - requires authentication"""
    return render_template('dashboard.html', title='Dashboard')


@bp.route('/profile')
@login_required
def profile():
    """User profile page - requires authentication"""
    return render_template('profile.html', title='Profile')