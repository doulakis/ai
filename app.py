import os
from app import create_app, db
from app.models import User, BlogPost, Project, Contact

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'BlogPost': BlogPost,
        'Project': Project,
        'Contact': Contact
    }


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command('seed-db')
def seed_db():
    """Seed the database with sample data."""
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create sample project
    project = Project(
        title='Personal Website',
        description='A Flask-based personal website with portfolio, blog, and contact features.',
        technologies='Python, Flask, SQLAlchemy, HTML, CSS, JavaScript',
        github_url='https://github.com/username/personal-website',
        featured=True,
        order=1
    )
    db.session.add(project)
    
    # Create sample blog post
    blog_post = BlogPost(
        title='Welcome to My Blog',
        slug='welcome-to-my-blog',
        content='This is my first blog post! I\'m excited to share my thoughts and experiences here.',
        excerpt='Welcome to my personal blog where I share my thoughts and experiences.',
        author=admin,
        published=True,
        tags='welcome, first post, blog'
    )
    db.session.add(blog_post)
    
    db.session.commit()
    print('Database seeded with sample data!')


if __name__ == '__main__':
    app.run(debug=True)