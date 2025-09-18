#!/usr/bin/env python3
"""
Main Flask application entry point
"""
import os
from app import create_app, db
from app.models import User
from flask_migrate import upgrade


def deploy():
    """Run deployment tasks."""
    # Create database tables
    db.create_all()
    
    # Create a default admin user if it doesn't exist
    if not User.get_by_username('admin'):
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Created default admin user (username: admin, password: admin123)")


app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in flask shell"""
    return {'db': db, 'User': User}


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Create database tables
    db.create_all()
    
    # Create a default admin user if it doesn't exist
    if not User.get_by_username('admin'):
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Created default admin user (username: admin, password: admin123)")


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create default admin user
        if not User.get_by_username('admin'):
            admin = User(
                username='admin',
                email='admin@example.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Created default admin user (username: admin, password: admin123)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)