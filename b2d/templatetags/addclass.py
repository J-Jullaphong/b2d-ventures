from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(field, values):
    css_class = values.split("|")[0]
    placeholder = values.split("|")[1]
    return field.as_widget(attrs={"class": css_class, "placeholder": placeholder})