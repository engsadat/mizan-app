"""
Run once on a fresh server to create the admin user and initialize the DB.
Usage:  python scripts/setup_admin.py --username admin --password <yourpassword>
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import User

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', default='admin')
    parser.add_argument('--password', required=True)
    parser.add_argument('--role', default='admin', choices=['admin', 'editor', 'viewer'])
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        db.create_all()
        existing = User.query.filter_by(username=args.username).first()
        if existing:
            existing.set_password(args.password)
            existing.role = args.role
            db.session.commit()
            print(f'Updated user: {args.username} (role={args.role})')
        else:
            u = User(username=args.username, role=args.role)
            u.set_password(args.password)
            db.session.add(u)
            db.session.commit()
            print(f'Created user: {args.username} (role={args.role})')

if __name__ == '__main__':
    main()
