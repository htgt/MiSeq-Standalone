from django import template

register = template.Library()

def baseUrl():
    return 

@register.simple_tag
def update_base(val):
    val=val+1
    return val