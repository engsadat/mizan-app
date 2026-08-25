import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Paths
    PROJECT_ROOT = Path(__file__).resolve().parent
    HR_ROOT = PROJECT_ROOT.parent
    DATA_FOLDER = PROJECT_ROOT / 'data'

    # Excel data sources (can be overridden by environment variables)
    EXCEL_SOURCES = {
        'po_master': os.environ.get('EXCEL_PO_MASTER') or str(DATA_FOLDER / 'po_master.xlsx'),
        'invoices': os.environ.get('EXCEL_INVOICES') or str(DATA_FOLDER / 'invoices.xlsx'),
        'po6_detail': os.environ.get('EXCEL_PO6') or str(DATA_FOLDER / 'po6_detail.xlsx'),
        'variations': os.environ.get('EXCEL_VARIATIONS') or str(DATA_FOLDER / 'variations.xlsx'),
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mizan_dev.db'
    WTF_CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + str(Path(__file__).resolve().parent / 'instance' / 'mizan.db').replace('\\', '/'),
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig,
}
