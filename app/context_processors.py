def custom_context(request):
    try:
        event = request.session.pop("event")
    except KeyError:
        event = {}

    return {
        "event": event
    }