# Personal Website - Flask Authentication System

A comprehensive Flask-based personal website with a complete user authentication system featuring registration, login, logout, and session management.

## Features

### 🔐 Authentication System
- **User Registration**: Secure user registration with email validation
- **User Login**: Login with username or email
- **Password Security**: Werkzeug password hashing with salt
- **Session Management**: Flask-Login integration with "Remember Me" functionality
- **Protected Routes**: Login-required decorator for secure pages
- **CSRF Protection**: Flask-WTF CSRF protection on all forms

### 🎨 Modern UI
- **Bootstrap 5**: Responsive, modern design
- **Bootstrap Icons**: Beautiful iconography
- **Flash Messages**: User feedback system
- **Mobile Responsive**: Works on all devices

### 🛡️ Security Features
- Password hashing with salt (Werkzeug)
- CSRF protection on forms
- Secure session management
- Protected routes with login_required decorator
- Email validation
- Password confirmation validation

## Quick Start

### 1. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

### 4. Default Admin User
A default admin user is created automatically:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: admin123

## Project Structure

```
personal-website/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # User model with authentication
│   ├── forms.py                 # WTF forms for auth
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Auth routes (login, register, logout)
│   ├── main/                    # Main application blueprint
│   │   ├── __init__.py
│   │   └── routes.py            # Main routes (home, dashboard, profile)
│   └── templates/               # Jinja2 templates
│       ├── base.html            # Base template with navigation
│       ├── index.html           # Home page
│       ├── dashboard.html       # Protected dashboard
│       ├── profile.html         # User profile page
│       └── auth/                # Authentication templates
│           ├── login.html
│           ├── register.html
│           ├── reset_password_request.html
│           └── reset_password.html
├── venv/                        # Virtual environment
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env                         # Environment variables
└── README.md                    # This file
```

## Routes

### Public Routes
- `/` - Home page
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/reset_password_request` - Password reset request
- `/auth/logout` - User logout

### Protected Routes (Login Required)
- `/dashboard` - User dashboard
- `/profile` - User profile page

## Configuration

The application uses environment variables for configuration:

```bash
# .env file
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
FLASK_APP=run.py
```

## Database

The application uses SQLite for development. The User model includes:

- `id` - Primary key
- `username` - Unique username (3-20 characters)
- `email` - Unique email address
- `password_hash` - Hashed password (never stored in plain text)
- `created_at` - Account creation timestamp
- `last_login` - Last login timestamp
- `is_active` - Account status

## Security Implementation

### Password Security
- Passwords are hashed using Werkzeug's `generate_password_hash()`
- Salt-based hashing prevents rainbow table attacks
- Minimum 8 character password requirement

### Session Security
- Flask-Login handles session management
- Secure cookie settings in production
- "Remember Me" functionality with configurable duration

### CSRF Protection
- Flask-WTF provides CSRF protection
- All forms include CSRF tokens
- Automatic validation on form submission

### Form Validation
- Server-side validation using WTForms
- Email format validation
- Password confirmation matching
- Username and email uniqueness checks

## Testing the System

1. **Registration**: Create a new account at `/auth/register`
2. **Login**: Sign in at `/auth/login` 
3. **Protected Access**: Try accessing `/dashboard` without login (should redirect)
4. **Dashboard**: Access dashboard after login
5. **Profile**: View user profile information
6. **Logout**: Sign out and verify session is cleared

## Development

### Adding New Protected Routes
```python
from flask_login import login_required

@app.route('/new-protected-route')
@login_required
def protected_view():
    return render_template('protected.html')
```

### Customizing User Model
Extend the User model in `app/models.py` to add additional fields:

```python
class User(UserMixin, db.Model):
    # ... existing fields ...
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
```

## Production Deployment

For production deployment:

1. Set strong `SECRET_KEY` in environment
2. Use PostgreSQL instead of SQLite
3. Enable HTTPS
4. Set secure cookie flags
5. Configure proper logging
6. Set up email for password reset functionality

## Dependencies

- Flask 2.3.3 - Web framework
- Flask-SQLAlchemy 3.0.5 - Database ORM
- Flask-Login 0.6.3 - User session management
- Flask-WTF 1.1.1 - Form handling and CSRF protection
- WTForms 3.0.1 - Form validation
- Werkzeug 2.3.7 - Password hashing utilities
- email-validator 2.0.0 - Email validation
- python-dotenv 1.0.0 - Environment variable management
- Flask-Migrate 4.0.5 - Database migrations

## License

This project is open source and available under the MIT License.