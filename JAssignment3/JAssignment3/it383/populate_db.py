"""
Run this script ONCE after migrations to seed sample data:
    python manage.py shell < populate_db.py
"""

import os
import django
from decimal import Decimal
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
django.setup()

from core.models import Department, User, Asset, MaintenanceLog

# --- Departments ---
cs_dept, _ = Department.objects.get_or_create(name='Computer Science')
hr_dept, _ = Department.objects.get_or_create(name='Human Resources')
accounting_dept, _ = Department.objects.get_or_create(name='Accounting')

# --- Users ---
users_data = [
    ('jsmith', 'EMP001', cs_dept),
    ('mjones', 'EMP002', hr_dept),
    ('kwilliams', 'EMP003', accounting_dept),
    ('dbrown', 'EMP004', cs_dept),
    ('lgarcia', 'EMP005', hr_dept),
]

users = []
for username, emp_id, dept in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'employee_id': emp_id, 'department': dept}
    )
    if created:
        user.set_password('password123')
        user.save()
    users.append(user)

# --- 15 Sample Assets ---
assets_data = [
    ('Dell Latitude 5420', 'SN-LAP-001', Decimal('1350.00'), users[0]),
    ('HP EliteDesk 800', 'SN-DSK-002', Decimal('920.00'), users[1]),
    ('Cisco Catalyst 2960', 'SN-NET-003', Decimal('2850.00'), users[0]),
    ('HP LaserJet Pro MFP', 'SN-PRT-004', Decimal('520.00'), users[2]),
    ('LG UltraFine 27"', 'SN-MON-005', Decimal('450.00'), users[3]),
    ('Lenovo ThinkPad T14', 'SN-LAP-006', Decimal('1650.00'), users[4]),
    ('APC Smart-UPS 1500', 'SN-UPS-007', Decimal('320.00'), users[0]),
    ('Polycom VVX 401', 'SN-PHN-008', Decimal('220.00'), users[1]),
    ('Seagate Backup Plus 5TB', 'SN-HDD-009', Decimal('150.00'), users[2]),
    ('MacBook Pro M3', 'SN-MAC-010', Decimal('2100.00'), users[3]),
    ('BenQ TH685 Projector', 'SN-PRJ-011', Decimal('780.00'), users[4]),
    ('Dell PowerEdge R750', 'SN-SRV-012', Decimal('6200.00'), users[0]),
    ('Logitech BRIO 4K', 'SN-CAM-013', Decimal('120.00'), users[1]),
    ('Keychron K8 Wireless', 'SN-KBD-014', Decimal('180.00'), users[2]),
    ('TP-Link EAP660 HD', 'SN-WAP-015', Decimal('280.00'), users[3]),
]

created_assets = []
for name, serial, cost, user in assets_data:
    asset, _ = Asset.objects.get_or_create(
        serial_number=serial,
        defaults={'name': name, 'cost': cost, 'assigned_to': user}
    )
    created_assets.append(asset)

print(f"✅ {len(created_assets)} assets ready")

# --- 5 Maintenance Logs ---
logs_data = [
    (created_assets[0], 'Replaced keyboard and cleaned vents', Decimal('85.00'), date(2025, 1, 20)),
    (created_assets[2], 'Updated firmware and configured VLANs', Decimal('250.00'), date(2025, 2, 15)),
    (created_assets[3], 'Fixed paper feed mechanism', Decimal('110.00'), date(2025, 3, 10)),
    (created_assets[11], 'Added SSD storage upgrade', Decimal('550.00'), date(2025, 4, 25)),
    (created_assets[6], 'Replaced battery and surge protector', Decimal('120.00'), date(2025, 5, 12)),
]

log_count = 0
for asset, desc, cost, sdate in logs_data:
    log, created = MaintenanceLog.objects.get_or_create(
        asset=asset,
        service_date=sdate,
        defaults={'description': desc, 'cost': cost}
    )
    if created:
        log_count += 1

print(f"✅ {log_count} maintenance logs created")
print("🎉 Database seeded successfully!")
