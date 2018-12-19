'''Functions for working with temperatures.'''

def above_freezing(t):
    '''Convert Fahrenheit to Celsius.'''
    return t > 0

def to_celsius(t):
    '''True if temperature in Celsius is above freezing. False otherwise.'''
    return (t - 32.0) * 5.0 / 9.0
