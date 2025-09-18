from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import db
from app.auth import bp
from app.models import User
from app.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route with support for email or username"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find user by email first, then by username
        user = User.get_by_email(form.email_or_username.data)
        if user is None:
            user = User.get_by_username(form.email_or_username.data)
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email/username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Update last login timestamp
        user.update_last_login()
        
        # Log the user in
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to next page or home
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route for new users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data.lower()
        )
        user.set_password(form.password.data)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now registered!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    flash(f'You have been logged out, {current_user.username}.', 'info')
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user:
            # In a real application, you would send an email here
            # For now, we'll just show a message
            flash('Check your email for instructions to reset your password', 'info')
        else:
            flash('Email address not found', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', 
                         title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token (simplified implementation)"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # In a real application, you would verify the token here
    # For this demo, we'll just show the form
    form = PasswordResetForm()
    if form.validate_on_submit():
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)