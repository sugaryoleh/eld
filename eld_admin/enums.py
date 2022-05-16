from enum import Enum


class Status(Enum):
    OFF_DUTY = 'Off Duty'
    ON_DUTY = 'On Duty'
    SLEEPER = 'Sleeper'
    DRIVING = 'Driving'
    PC = 'PC'   # Personal Convenience
    ADC = 'ADC' # ADC - Adverse Driving Condition
