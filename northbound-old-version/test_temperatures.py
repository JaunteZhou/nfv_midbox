import nose
from temperatures import to_celsius

def test_freezing():
    '''Test freezing point'''
    assert to_celsius(32) == 0

def test_boiling():
    '''Test boiling point'''
    assert to_celsius(212) == 100

def test_roundoff():
    '''Test that roundoff works.'''
    assert to_celsius(100) == 38, 'Returning an unrounded result.'

if __name__ == '__main__':
    nose.runmodule()