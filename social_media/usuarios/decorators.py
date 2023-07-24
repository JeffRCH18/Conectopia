from django.shortcuts import redirect

def session_filter_required():

    session_var = 'userID'

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get(session_var):
                # User has the required session variable, allow access
                return view_func(request, *args, **kwargs)
            else:
                # User does not have the required session variable, redirect or deny access
                return redirect('/login/')
        return wrapper
    return decorator