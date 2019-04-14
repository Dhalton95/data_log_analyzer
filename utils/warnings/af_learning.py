""" Contains AF Learning warning class"""

class AFLearningWarning(object):
    """AF Learning warning class"""
    def __init__(self, af_learning_val, throttle_pos_val, gear_num, rpm_val):
        self.af_learning = af_learning_val
        self.throttle_pos = throttle_pos_val
        self.gear = gear_num
        self.rpm = rpm_val
