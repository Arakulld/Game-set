from django import template

register = template.Library()


@register.filter(name='first_letter')
def get_first_letter(word):
    return word[0]


@register.filter(name='without_first')
def get_without_first(word):
    return word[1:len(word)]
