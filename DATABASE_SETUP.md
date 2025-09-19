# Database Setup Documentation

## Overview

This document describes the database setup and models for the Flask personal website project.

## Database Configuration

### Development Environment
- **Database**: SQLite (`app-dev.db`)
- **Location**: Project root directory
- **Configuration**: Automatically configured via `config.py`

### Production Environment
- **Database**: PostgreSQL (configurable via environment variables)
- **Connection**: Set via `DATABASE_URL` environment variable
- **Configuration**: Production-ready settings in `config.py`

## Database Models

### User Model (`users` table)
**Purpose**: Authentication and content management

**Fields**:
- `id` (Integer, Primary Key): Unique identifier
- `username` (String, 64 chars): Unique username
- `email` (String, 120 chars): Unique email address
- `password_hash` (String, 255 chars): Hashed password
- `is_admin` (Boolean): Admin privileges flag
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Methods**:
- `set_password(password)`: Hash and store password
- `check_password(password)`: Verify password against hash

**Relationships**:
- One-to-Many with BlogPost (as author)

### BlogPost Model (`blog_posts` table)
**Purpose**: Blog content management

**Fields**:
- `id` (Integer, Primary Key): Unique identifier
- `title` (String, 200 chars): Post title
- `slug` (String, 200 chars): URL-friendly identifier (unique, indexed)
- `content` (Text): Full post content
- `excerpt` (Text): Short description/summary
- `author_id` (Integer, Foreign Key): Reference to User
- `published` (Boolean): Publication status
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `tags` (String, 500 chars): Comma-separated tags

**Methods**:
- `get_tags_list()`: Returns tags as a Python list
- `set_tags_from_list(tags_list)`: Set tags from a Python list

**Relationships**:
- Many-to-One with User (author)

### Project Model (`projects` table)
**Purpose**: Portfolio/project showcase

**Fields**:
- `id` (Integer, Primary Key): Unique identifier
- `title` (String, 200 chars): Project title
- `description` (Text): Project description
- `technologies` (String, 500 chars): Comma-separated technologies
- `github_url` (String, 500 chars): GitHub repository URL
- `live_url` (String, 500 chars): Live demo URL
- `image_url` (String, 500 chars): Project image URL
- `featured` (Boolean): Featured project flag
- `order` (Integer): Display order (for sorting)
- `created_at` (DateTime): Creation timestamp

**Methods**:
- `get_technologies_list()`: Returns technologies as a Python list
- `set_technologies_from_list(tech_list)`: Set technologies from a Python list

### Contact Model (`contacts` table)
**Purpose**: Contact form submissions storage

**Fields**:
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, 100 chars): Sender's name
- `email` (String, 120 chars): Sender's email
- `subject` (String, 200 chars): Message subject
- `message` (Text): Message content
- `created_at` (DateTime): Submission timestamp
- `is_read` (Boolean): Read status flag

**Methods**:
- `mark_as_read()`: Mark message as read
- `mark_as_unread()`: Mark message as unread

## Database Operations

### Initialization
```bash
# Initialize migration repository
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Migration Workflow
```bash
# After model changes, create new migration
flask db migrate -m "Description of changes"

# Review generated migration file in migrations/versions/

# Apply migration
flask db upgrade
```

### Development Commands
```bash
# Enter Flask shell with models available
flask shell

# Initialize empty database (alternative to migrations)
flask init-db

# Seed database with sample data
flask seed-db
```

## Database Files

### SQLite Files
- `app-dev.db`: Development database
- `app.db`: Default database (if DEV_DATABASE_URL not set)

### Migration Files
- `migrations/`: Flask-Migrate repository
- `migrations/versions/`: Individual migration files
- `migrations/alembic.ini`: Alembic configuration

## Testing

### Database Testing
Run the comprehensive database test:
```bash
python test_db.py
```

This test verifies:
- All model creation and relationships
- Password hashing and verification
- Tag and technology list methods
- Contact read/unread functionality
- Database queries and filters

### Manual Testing
```python
# In Flask shell (flask shell)
from app.models import User, BlogPost, Project, Contact

# Create test user
user = User(username='test', email='test@example.com')
user.set_password('password')
db.session.add(user)
db.session.commit()

# Verify password
user.check_password('password')  # Returns True
```

## Environment Variables

### Required for Production
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Optional Configuration
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@yoursite.com
```

## Security Considerations

1. **Password Hashing**: Uses Werkzeug's secure password hashing
2. **SQL Injection**: Protected by SQLAlchemy ORM
3. **Environment Variables**: Sensitive data stored in environment variables
4. **Database URL**: Never hardcode production database credentials

## Performance Considerations

1. **Indexes**: Added on frequently queried fields (username, email, slug)
2. **Relationships**: Lazy loading configured for optimal performance
3. **Pagination**: Implemented for blog posts to handle large datasets
4. **Query Optimization**: Use specific queries rather than loading all data

## Backup and Maintenance

### SQLite Backup
```bash
# Backup development database
cp app-dev.db app-dev-backup-$(date +%Y%m%d).db
```

### PostgreSQL Backup
```bash
# Backup production database
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql
```

## Troubleshooting

### Common Issues

1. **Migration Conflicts**: 
   - Delete migrations/versions/* and recreate with `flask db migrate`

2. **Database Locked (SQLite)**:
   - Ensure all database connections are properly closed
   - Restart the application

3. **Foreign Key Constraints**:
   - Ensure referenced records exist before creating relationships
   - Use proper cascade settings for deletions

### Debug Mode
Enable SQLAlchemy query logging:
```python
# In config.py
SQLALCHEMY_ECHO = True  # Only for debugging
```

## Future Enhancements

1. **Full-Text Search**: Add search functionality for blog posts
2. **Categories**: Add category system for blog posts
3. **Comments**: Add comment system for blog posts
4. **File Uploads**: Add image upload functionality for projects
5. **Admin Interface**: Create admin panel for content management
6. **API Endpoints**: Add REST API for mobile app integration