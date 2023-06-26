def add_variable_to_context(request):
    return {
        'authenticated': request.user.is_authenticated,
    }