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
        'employees': os.environ.get('EXCEL_EMPLOYEES') or str(DATA_FOLDER / 'source' / 'employees data source.xlsx'),
        'projects': os.environ.get('EXCEL_PROJECTS') or str(DATA_FOLDER / 'source' / 'project_2026_database_ver1_updated.xlsx'),
        'invoices': os.environ.get('EXCEL_INVOICES') or str(DATA_FOLDER / 'Invoices' / 'Jun_Inv.xlsx'),
        'contacts': os.environ.get('EXCEL_CONTACTS') or str(DATA_FOLDER / 'source' / 'contacts.xlsx'),
        'po_master': os.environ.get('EXCEL_PO_MASTER') or str(DATA_FOLDER / 'po_master.xlsx'),
        'po6_detail': os.environ.get('EXCEL_PO6') or str(DATA_FOLDER / 'po6_detail.xlsx'),
        'variations': os.environ.get('EXCEL_VARIATIONS') or str(DATA_FOLDER / 'variations.xlsx'),
    }

    # Job code constants (Phase 1: hardcoded; Phase 2: load from Excel)
    JOB_CODES = {
        'مهندس أمن وسلامة': {'code': 'HSE-ENG', 'rate': 5000},
        'مراقب أمن وسلامة': {'code': 'HSE-SUP', 'rate': 3500},
        'مراقب موقع': {'code': 'SITE-SUP', 'rate': 3000},
        'مهندس مقيم': {'code': 'RES-ENG', 'rate': 6000},
        'مهندس موقع': {'code': 'SITE-ENG', 'rate': 5500},
    }

    # Region constants (Phase 1 audit: reversed order per user requirements)
    REGIONS = ['نجران', 'الباحة', 'جازان', 'عسير']
    REGION_CODES = {'عسير': 'AS', 'جازان': 'JZ', 'الباحة': 'BA', 'نجران': 'NJ'}
    REPORT_MONTH = "يونيو 2026"
    PROJECT_MGR = "م/ يسري أحمد عبد السلام"


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
