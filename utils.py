from datetime import datetime, timezone
from typing import Optional

def calculate_urgency(deadline_at: Optional[datetime]) -> bool:
    if not deadline_at:
        return False
    now = datetime.now(timezone.utc)
    if deadline_at.tzinfo is None:
        deadline_at = deadline_at.replace(tzinfo=timezone.utc)
    return (deadline_at - now).days <= 3

def calculate_days_until_deadline(deadline_at: Optional[datetime]) -> Optional[int]:
    if not deadline_at:
        return None
    now = datetime.now(timezone.utc)
    if deadline_at.tzinfo is None:
        deadline_at = deadline_at.replace(tzinfo=timezone.utc)
    return (deadline_at - now).days

def determine_quadrant(is_important: bool, is_urgent: bool) -> str:
    if is_important and is_urgent: return "Q1"
    if is_important: return "Q2"
    if is_urgent: return "Q3"
    return "Q4"
