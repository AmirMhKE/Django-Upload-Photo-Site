import json

def custom_context(request):
    try:
        event = request.session.pop("event")
    except KeyError:
        event = json.dumps({"type": None, "content": None})

    return {
        "event": event
    }