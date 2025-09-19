from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import Contact, BlogPost, Project

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Home page."""
    # Get featured projects
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.order).limit(3).all()
    
    # Get recent blog posts
    recent_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    return render_template('index.html', 
                         featured_projects=featured_projects,
                         recent_posts=recent_posts)


@main.route('/portfolio')
def portfolio():
    """Portfolio page."""
    projects = Project.query.order_by(Project.order, Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)


@main.route('/blog')
def blog():
    """Blog listing page."""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(published=True)\
                         .order_by(BlogPost.created_at.desc())\
                         .paginate(page=page, per_page=10, error_out=False)
    return render_template('blog.html', posts=posts)


@main.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page."""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('blog_post.html', post=post)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if name and email and subject and message:
            contact_msg = Contact(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            
            flash('Thank you for your message! I\'ll get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html')