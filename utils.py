#Import Modules
from random import Random

def generate_password(password_length=8, alternate_hands=True):
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

def html_email(subject, template, template_vars_dict, from_email, to):
    """
    Function to send email with html template
    """
    
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    
    html_content = render_to_string(template, template_vars_dict)
    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
    
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()