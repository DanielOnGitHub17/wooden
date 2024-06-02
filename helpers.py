def show_message(request):
    if "message" in request.session:
        message = request.session["message"]
        del request.session["message"]
    else:
        message = ""
    return message

