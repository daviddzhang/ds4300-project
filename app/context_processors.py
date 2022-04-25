def user_initials(request):
    if request.user.is_authenticated:
        initials = request.user.first_name[0] + request.user.last_name[0]
    else:
        initials = None

    return {'user_initials': initials}
