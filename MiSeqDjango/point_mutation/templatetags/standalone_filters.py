from os import name
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

@register.filter(name='table_cells')
def table_cells(base, rows):
    tmp_num = base
    result = dict()
    base_array = [ 1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89 ]
    for row in rows:
        array = [x + tmp_num for x in base_array]
        result[row] = array
        tmp_num += 1
    
    return result

@register.filter(name='get_prev_well')
def get_prev_well(str_num):
    if str_num == '':
        str_num = '0'
    val = int(str_num)
    val = val-1
    return val

@register.filter(name='get_next_well')
def get_next_well(str_num):
    if str_num == '':
        str_num = '0'
    val = int(str_num)
    val = val+1
    return val

@register.filter(name='get_gene')
def get_gene(overview_data, experiment):
    return overview_data['summary'].get(experiment, '')[0]
