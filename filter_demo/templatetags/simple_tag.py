from django import template

register=template.Library()

@register.simple_tag
def greet_user(message,user_name):
    return "{},{}!!!".format(message,user_name)

@register.simple_tag(takes_context=True)
def contextual_greet_user(context,message):
    return "{}, {}!!!".format(message,context['username'])
