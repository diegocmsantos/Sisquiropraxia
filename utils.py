#Import Modules
from random import Random

def generate_password(password_length=8, alternate_hands=False):
    """
    A simple script for making random passwords, WITHOUT 1,l,O,0.  Because
    those characters are hard to tell the difference between in some fonts. 
    """
    rng = Random()
    
    righthand = '23456qwertasdfgzxcvbQWERTASDFGZXCVB'
    lefthand = '789yuiophjknmYUIPHJKLNM'
    allchars = righthand + lefthand
    
    for i in range(password_length):
        if not alternate_hands:
            return rng.choice(allchars)
        else:
            if i%2:
                return rng.choice(lefthand)
            else:
                return rng.choice(righthand)
