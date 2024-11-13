from django import template

register = template.Library()


@register.filter
def mask_email(email):
    if not isinstance(email, str) or "@" not in email:
        return email

    username, domain = email.split("@")
    if len(username) > 3:
        username = username[:3] + "****"
    else:
        username = username + "****"
    return f"{username}@{domain}"
