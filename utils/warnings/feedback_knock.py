""" Contains feedback knock warning class"""

class FeedbackKnockWarning(object):
    """Feedback knock warning class"""
    def __init__(self, knock_val, dam_val, gear_num, rpm_val):
        self.knock_value = knock_val
        self.dam = dam_val
        self.gear = gear_num
        self.rpm = rpm_val
