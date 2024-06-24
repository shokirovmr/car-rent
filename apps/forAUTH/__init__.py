def exclude_user(queryset, username="shokirov"):
    return queryset.exclude(username=username)


