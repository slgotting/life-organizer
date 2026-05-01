
def build_form_errors_string(form):
    errors_list = []
    for list_of_errors in form.errors.values():
        errors_list += list_of_errors
    return ", ".join(errors_list)
