from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(user_email, name):
    context = {
        "name": name
    }

    html_content = render_to_string("greeting.html", context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject="Xush kelibsiz",
        body=text_content,
        from_email=None,
        to=[user_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def send_code_email(user_email, code):
    context = {
        "email": user_email,
        "code": code,
    }

    html_content = render_to_string("code.html", context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject="Sizning tasdiqlash kodingiz",
        body=text_content,
        from_email=None,
        to=[user_email],        
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()