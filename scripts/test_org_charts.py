"""
Test script: populate sample data and run gen_org_charts.py
This verifies the script works end-to-end.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import (
    Employee, EmployeeStatus, JobCode, Project, Nationality, Office
)
from datetime import date, datetime

# Initialize Flask app
app = create_app()
app.app_context().push()

# Clear existing data (for testing)
db.drop_all()
db.create_all()

print("Creating sample data...")

# Create statuses
active_status = EmployeeStatus(name_ar='على قوة العمل')
replacement_status = EmployeeStatus(name_ar='بديل')
db.session.add_all([active_status, replacement_status])
db.session.commit()
print(f"[OK] Created statuses")

# Create job codes
job1 = JobCode(code='RE-E3', title='مهندس مقيم E3', standard_rate=28000)
job2 = JobCode(code='SI-E2', title='مراقب موقع E2', standard_rate=12000)
job3 = JobCode(code='HSE-E3', title='مهندس أمن وسلامة E3', standard_rate=21000)
db.session.add_all([job1, job2, job3])
db.session.commit()
print(f"[OK] Created job codes")

# Create nationalities
nat1 = Nationality(name_ar='سعودي', country_code='SA')
nat2 = Nationality(name_ar='باكستاني', country_code='PK')
nat3 = Nationality(name_ar='مصري', country_code='EG')
db.session.add_all([nat1, nat2, nat3])
db.session.commit()
print(f"[OK] Created nationalities")

# Create sample employees
emp1 = Employee(
    full_name='أحمد محمد علي',
    region='عسير',
    job_code_id=job1.id,
    nationality_id=nat1.id,
    re_code='AS-001',
    phone='0501234567',
    hire_date=date(2020, 1, 15),
    current_status_id=active_status.id,
    category='مهندس',
    direct_manager='محمد سلام'
)

emp2 = Employee(
    full_name='محمد سلام',
    region='عسير',
    job_code_id=job2.id,
    nationality_id=nat2.id,
    re_code='AS-002',
    phone='0502345678',
    hire_date=date(2019, 6, 10),
    current_status_id=active_status.id,
    category='مراقب'
)

emp3 = Employee(
    full_name='علي حسن أحمد',
    region='جازان',
    job_code_id=job3.id,
    nationality_id=nat3.id,
    re_code='JZ-001',
    phone='0503456789',
    hire_date=date(2021, 3, 20),
    current_status_id=active_status.id,
    category='مهندس'
)

emp4 = Employee(
    full_name='فاطمة خالد محمود',
    region='الباحة',
    job_code_id=job2.id,
    nationality_id=nat1.id,
    re_code='BA-001',
    phone='0504567890',
    hire_date=date(2022, 5, 5),
    current_status_id=active_status.id,
    category='مراقب'
)

db.session.add_all([emp1, emp2, emp3, emp4])
db.session.commit()
print(f"[OK] Created 4 sample employees")

# Create sample projects
proj1 = Project(
    name='مشروع توسيع شبكة المياه - عسير',
    region='عسير',
    contractor_name='شركة النور للمقاولات',
    project_state='تحت التنفيذ',
    included=True,
    value=5000000,
    re_code='AS-001',
    start_date=date(2026, 1, 1),
    end_date=date(2026, 12, 31)
)

proj2 = Project(
    name='مشروع محطة معالجة - جازان',
    region='جازان',
    contractor_name='شركة الخليج للمقاولات',
    project_state='تحت التنفيذ',
    included=True,
    value=3500000,
    re_code='JZ-001',
    start_date=date(2026, 2, 1),
    end_date=date(2026, 11, 30)
)

proj3 = Project(
    name='مشروع أنابيب صرف - الباحة',
    region='الباحة',
    contractor_name='شركة الأمل للمقاولات',
    project_state='تحت التنفيذ',
    included=True,
    value=2800000,
    re_code='BA-001',
    start_date=date(2026, 3, 15),
    end_date=date(2026, 10, 15)
)

db.session.add_all([proj1, proj2, proj3])
db.session.commit()
print(f"[OK] Created 3 sample projects")

print(f"\nSample data created successfully!")
print(f"Now running gen_org_charts.py...")
print("="*60)

# Now run the actual org charts generation script
import subprocess
result = subprocess.run(
    [sys.executable, 'scripts/gen_org_charts.py'],
    cwd=Path(__file__).parent.parent,
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("="*60)
if result.returncode == 0:
    print("[SUCCESS] Test completed successfully!")
else:
    print(f"[FAILED] Test failed with return code {result.returncode}")

sys.exit(result.returncode)
