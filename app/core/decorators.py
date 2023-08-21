from django.http import HttpResponse


def is_executor(user):
    return user.groups.filter(name='executor').exists()


def is_inspector(user):
    return user.groups.filter(name='inspector').exists()



# def access_permissions(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):

#             group = None
#             if request.user.group.exists():
#                 group = request.user.groups.all()[0]

#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse()
#         return wrapper_func
#     return decorator