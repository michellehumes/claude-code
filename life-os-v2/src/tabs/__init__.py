"""
Tab builders for Life OS v2

Each module contains functions to build specific tab groups:
- financial.py: Tabs 1-11 (Financial Dashboard)
- job_search.py: Tabs 12-18 (Job Search System)
- goals.py: Tabs 19-22 (Goals System)
- household.py: Tabs 23-25 (Household System)
- shelzys.py: Tabs 26-34 (Shelzy's Designs Business)
- fertility.py: Tabs 35-40 (Fertility & Health)
- executive.py: Tabs 41-46 (Executive Dashboards)
- oura.py: Tabs 47-54 (Oura Ring Integration)
"""

from .financial import FinancialTabBuilder
from .job_search import JobSearchTabBuilder
from .goals import GoalsTabBuilder
from .household import HouseholdTabBuilder
from .shelzys import ShelzysTabBuilder
from .fertility import FertilityTabBuilder
from .executive import ExecutiveTabBuilder
from .oura import OuraTabBuilder

__all__ = [
    "FinancialTabBuilder",
    "JobSearchTabBuilder",
    "GoalsTabBuilder",
    "HouseholdTabBuilder",
    "ShelzysTabBuilder",
    "FertilityTabBuilder",
    "ExecutiveTabBuilder",
    "OuraTabBuilder",
]
