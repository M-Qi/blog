from user.forms import LoginForm

def form_modal(request):
    content = {}
    content['form'] = LoginForm()

    return content
