from django import template
register = template.Library()

@register.filter(name='circle_css_class')
def circle_css_class(value):
    classmap = {
        '1': 'span_circle_green',
        '2': 'span_circle_blue',
        '3': 'span_circle_grey'
}
    try:
        return classmap[value]

    except:
        return 'Not found'

@register.filter
def text_css_class(value):
    classmap = {
        '1': 'span_text_green',
        '2': 'span_text_blue',
        '3': 'span_text_grey'
}
    try:
        return classmap[value]

    except:
        return 'Not found'
