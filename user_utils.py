# coding=utf-8

from django.shortcuts import RequestContext
from django.template import loader
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def render_to_local(request, template, local_data):
    t = loader.get_template(template)
    ctx = RequestContext(request, local_data)
    return unicode(t.render(ctx))

def send_mail(to_emails, from_email, subject,
              text_template='mail/html/message.html',
              html_template='mail/text/message.txt',
              data={}):
    """
    Function for sending email both in HTML and text formats.

    to_emails - list of emails for sending
    from_email - sender address
    subject - the subject of message
    text_template - template for text mail
    html_template - template for html mail
    data - dictionary with data for templates
    """
    html_content = render_to_string(html_template, data)
    text_content = render_to_string(text_template, data)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()