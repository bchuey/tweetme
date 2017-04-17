from django import template
from django.contrib.auth import get_user_model

from accounts.models import UserProfile

register = template.Library()

User = get_user_model()

# decorator function
@register.inclusion_tag("accounts/snippets/recommend.html")
def recommended(user):
    if isinstance(user, User):
        qs = UserProfile.objects.recommended(user)
        return {"recommended": qs}

# below code is equivalent to above code
# above codoe is much shorter though

# from django.template.loader import get_template
# from django.utils.safestring import mark_safe
#
# @register.simple_tag
# def recommended(user):
#     if isinstance(user, User):
#         template = get_template("accounts/snippets/recommend.html")
#         context = {"recommend": UserProfile.objects.recommended(user)}
#         data = template.render(context=context)
#         content = mark_safe(data)
#         # qs = UserProfile.objects.recommended(user)
#         # return {"recommended": qs}
#         return content
