"""In-memory employee cache from Excel."""

from scripts.load_employees import load_employees


class EmployeeCache:
    """Simple in-memory cache of employees from Excel."""

    _cache = None

    @classmethod
    def load(cls):
        """Load employees from Excel if not already cached."""
        if cls._cache is None:
            cls._cache = load_employees()
        return cls._cache

    @classmethod
    def get_all(cls):
        """Get all employees."""
        return cls.load()

    @classmethod
    def get_by_id(cls, emp_id):
        """Get employee by ID."""
        employees = cls.get_all()
        for emp in employees:
            if emp['id'] == emp_id:
                return emp
        return None

    @classmethod
    def search(cls, query='', region='', status=''):
        """Filter employees by search query, region, and status."""
        employees = cls.get_all()
        filtered = employees

        # Filter by status
        if status and status != 'all':
            filtered = [e for e in filtered if e['status'] == status]

        # Filter by region
        if region:
            filtered = [e for e in filtered if e['region'] == region]

        # Search by name, job, or phone
        if query:
            q_lower = query.lower()
            filtered = [
                e for e in filtered
                if q_lower in (e.get('name', '') or '').lower()
                or q_lower in (e.get('job', '') or '').lower()
                or q_lower in (e.get('phone', '') or '').lower()
            ]

        return sorted(filtered, key=lambda e: (e.get('region', ''), e.get('name', '')))

    @classmethod
    def count_by_status(cls, status):
        """Count employees by status."""
        employees = cls.get_all()
        return sum(1 for e in employees if e.get('status') == status)


class Pagination:
    """Simple in-memory pagination."""

    def __init__(self, items, page=1, per_page=50):
        self.items = items
        self.page = max(1, page)
        self.per_page = per_page
        self.total = len(items)
        self.pages = (self.total + per_page - 1) // per_page

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_num(self):
        return self.page - 1 if self.has_prev else None

    @property
    def next_num(self):
        return self.page + 1 if self.has_next else None

    def iter_pages(self, left_edge=1, left_margin=1, right_margin=1, right_edge=1):
        """Iterator for page numbers to display."""
        last = 0
        for num in range(1, self.pages + 1):
            if (
                (num <= left_edge or num > self.pages - right_edge)
                or (self.page - left_margin <= num <= self.page + right_margin)
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def get_page_items(self):
        """Get items for current page."""
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]
