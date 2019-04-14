""" Contains feedback knock warning class"""

class FeedbackKnockWarning(object):
    """Feedback knock warning class"""
    def __init__(self, knock_val, dam_val, throttle_pos_val, gear_num, rpm_val):
        self.knock = knock_val
        self.dam = dam_val
        self.throttle_pos = throttle_pos_val
        self.gear = gear_num
        self.rpm = rpm_val
