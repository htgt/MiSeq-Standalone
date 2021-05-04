from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='cell_base')
def cell_base(val):
    num_val = int(val)
    base_array = [ "1", "9", "17", "25", "33", "41", "49", "57", "65", "73", "81", "89" ]
    for str_num in base_array:
        tmp_num = int(str_num)
        tmp_num += num_val
        str_num = str(tmp_num)
    return base_array
