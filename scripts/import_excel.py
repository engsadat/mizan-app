"""
One-time migration: source/employees data source.xlsx → Mizan DB.
Run from hr_webapp/: python scripts/import_excel.py

Imports ALL employees regardless of status.
is_replacement is auto-set for status == 'بديل'.
Official headcount uses only 'على قوة العمل'.

Excel column map (0-based, sheet 'data'):
  0  = المؤهل الدراسي  (qualification)
  1  = سنة التخرج      (grad_year)
  2  = الايميل         (email)
  3  = رقم الجوال      (phone)
  4  = تاريخ المباشرة  (hire_date)
  5  = رقم الهوية      (id_number)
  6  = عدد سنوات الخبرة (experience_years)
  7  = استيفاء المتطلبات (not stored)
  8  = المهنة          (profession)
  9  = تاريخ انتهاء العقد (contract_end_date)
  10 = تاريخ الاستقالة  (resignation_date)
  11 = الموقف الحالي   (status — all values imported)
  12 = السبب           (status_reason)
  13 = تقييم المدير المباشر (not stored)
  14 = الجنسية         (nationality)
  15 = الكفالة         (kafala)
  16 = المنطقة         (region)
  17 = CBU             (cbu)
  18 = إشراف - دعم فني (supervision_type / category)
  19 = المكتب          (office)
  20 = الاسم           (full_name)
  21 = الوظيفة         (job_code title)
  22 = الكود2          (serial_no / employee code)
  23 = سعر الوحدة      (unit_price)
  24 = المدير المباشر  (direct_manager)
  25 = كشف حضور       (attendance_group name)
  26 = رقم_مسلسل      (not stored separately)
  27 = RE              (re_code)
"""
import sys, os, shutil
from pathlib import Path
from datetime import date, datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import (
    Employee, EmployeeStatus, JobCode, Nationality,
    Office, AttendanceGroup, EmployeeStatusHistory,
)
import openpyxl

_default_excel = Path(__file__).resolve().parents[2] / 'source' / 'employees data source.xlsx'
EXCEL = Path(os.environ.get('EXCEL_PATH', str(_default_excel)))

STATUS_REPLACEMENT = 'بديل'

ERR_VALS = {'#REF!', '=#REF!', '#VALUE!', '#N/A', '#NAME?', '#DIV/0!', '#NULL!', '#NUM!'}


def load_wb(path):
    tmp = str(path) + '.tmp.xlsx'
    shutil.copy2(str(path), tmp)
    wb = openpyxl.load_workbook(tmp, data_only=True)
    os.remove(tmp)
    return wb


def sv(v):
    if v is None:
        return ''
    s = str(v).strip()
    return '' if s in ERR_VALS else s


def parse_date(v):
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = sv(v)
    if not s:
        return None
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_int(v):
    s = sv(v)
    if not s:
        return None
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def parse_float(v):
    s = sv(v)
    if not s:
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def get_or_create_status(name, cache):
    if name not in cache:
        obj = EmployeeStatus.query.filter_by(name_ar=name).first()
        if not obj:
            obj = EmployeeStatus(name_ar=name)
            db.session.add(obj)
            db.session.flush()
        cache[name] = obj.id
    return cache[name]


def get_or_create_nationality(name, cache):
    if name not in cache:
        obj = Nationality.query.filter_by(name_ar=name).first()
        if not obj:
            obj = Nationality(name_ar=name)
            db.session.add(obj)
            db.session.flush()
        cache[name] = obj.id
    return cache[name]


def get_or_create_job_code(title, cache):
    if title not in cache:
        obj = JobCode.query.filter_by(title=title).first()
        if not obj:
            obj = JobCode(title=title)
            db.session.add(obj)
            db.session.flush()
        cache[title] = obj.id
    return cache[title]


def get_or_create_office(name, region, cache):
    key = (name, region)
    if key not in cache:
        obj = Office.query.filter_by(name=name).first()
        if not obj:
            obj = Office(name=name, region=region)
            db.session.add(obj)
            db.session.flush()
        cache[key] = obj.id
    return cache[key]


def get_or_create_attendance_group(name, office_id, cache):
    if name not in cache:
        obj = AttendanceGroup.query.filter_by(name=name).first()
        if not obj:
            obj = AttendanceGroup(name=name, office_id=office_id)
            db.session.add(obj)
            db.session.flush()
        cache[name] = obj.id
    return cache[name]


def main(app=None):
    if app is None:
        app = create_app()
    with app.app_context():
        db.create_all()

        existing = Employee.query.count()
        if existing > 0:
            print(f'DB already has {existing} employees. Aborting to prevent duplicate import.')
            print('Delete the DB file and re-run to force a fresh import.')
            return

        if not EXCEL.exists():
            print(f'ERROR: Excel file not found: {EXCEL}')
            sys.exit(1)

        wb = load_wb(EXCEL)
        ws = wb['data']
        rows = list(ws.iter_rows(min_row=2, values_only=True))

        status_cache = {}
        nat_cache    = {}
        job_cache    = {}
        office_cache = {}
        att_cache    = {}

        added = skipped = dupes = 0
        seen_names = set()

        for row in rows:
            name = sv(row[20])
            if not name:
                skipped += 1
                continue

            # Deduplicate — Excel repeats each employee across region sections
            if name in seen_names:
                dupes += 1
                continue
            seen_names.add(name)

            status_name = sv(row[11]) or 'غير محدد'
            status_id   = get_or_create_status(status_name, status_cache)

            nat_name  = sv(row[14])
            nat_id    = get_or_create_nationality(nat_name, nat_cache) if nat_name else None

            job_title = sv(row[21])
            jc_id     = get_or_create_job_code(job_title, job_cache) if job_title else None

            office_name = sv(row[19])
            region      = sv(row[16])
            cbu         = sv(row[17])
            office_id   = get_or_create_office(office_name, cbu, office_cache) if office_name else None

            att_name = sv(row[25])
            att_id   = get_or_create_attendance_group(att_name, office_id, att_cache) if att_name else None

            emp = Employee(
                full_name           = name,
                phone               = sv(row[3]),
                email               = sv(row[2]),
                id_number           = sv(row[5]),
                nationality_id      = nat_id,
                kafala              = sv(row[15]),
                region              = region,
                cbu                 = cbu,
                office_id           = office_id,
                supervision_type    = sv(row[18]),
                category            = sv(row[18]),
                attendance_group_id = att_id,
                job_code_id         = jc_id,
                unit_price          = parse_float(row[23]),
                hire_date           = parse_date(row[4]),
                contract_end_date   = parse_date(row[9]),
                resignation_date    = parse_date(row[10]),
                qualification       = sv(row[0]),
                grad_year           = parse_int(row[1]),
                experience_years    = parse_int(row[6]),
                profession          = sv(row[8]),
                direct_manager      = sv(row[24]),
                status_reason       = sv(row[12]),
                serial_no           = sv(row[22]),
                re_code             = sv(row[27]),
                current_status_id   = status_id,
                is_replacement      = (status_name == STATUS_REPLACEMENT),
            )
            db.session.add(emp)
            db.session.flush()

            db.session.add(EmployeeStatusHistory(
                employee_id = emp.id,
                old_status  = None,
                new_status  = status_name,
                change_date = date.today(),
                reason      = 'استيراد أولي من ملف Excel',
                recorded_by = 'import_script',
            ))
            added += 1

        db.session.commit()

        # Summary by status
        from sqlalchemy import func
        counts = (
            db.session.query(EmployeeStatus.name_ar, func.count(Employee.id))
            .join(Employee, Employee.current_status_id == EmployeeStatus.id)
            .group_by(EmployeeStatus.name_ar)
            .all()
        )
        print(f'\nDone. Total imported: {added} | Skipped (no name): {skipped} | Duplicates: {dupes}')
        print('\nتوزيع الموظفين بحسب الحالة:')
        for status, count in sorted(counts, key=lambda x: -x[1]):
            print(f'  {status}: {count}')


if __name__ == '__main__':
    main()
