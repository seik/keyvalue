from src.models import KeyValue


def set_value(message_text: str, chat_id: str, user_id: str):
    if len(message_text.split()) < 2:
        return "I need a key and a value"

    key, value = message_text.split(" ", 1)

    if not value.strip():
        return "Value cannot be empty"

    results = KeyValue.query(chat_id, KeyValue.subject == key)

    if results:
        obj = results[0]
        obj.user_id = user_id
        obj.key = key
        obj.value = value
        obj.save()
    else:
        obj = KeyValue(chat_id, user_id, key, value)
        obj.save()

    return f"Value {key} has been assigned"


def get_value(message_text: str, chat_id: str, user_id: str):
    key = message_text.strip()

    if not key:
        return "Send a key to search"

    results = KeyValue.query(chat_id, KeyValue.subject == key)

    if results:
        return results[0].value
    else:
        return "Key does not exists"


def delete_value(message_text: str, chat_id: str, user_id: str):
    key = message_text.strip()

    if not key:
        return "Send a key to delete"

    results = KeyValue.query(chat_id, KeyValue.subject == key)

    if results:
        results[0].delete()
        return f"Key {key} has been deleted"
    else:
        return "Key does not exist"


def get_list(chat_id: str):
    keyvalues = KeyValue.objects.filter(chat_id=chat_id).order_by("pk")

    if keyvalues.exists():
        return ", ".join(str(keyvalue.key) for keyvalue in keyvalues)
    else:
        return "There are no objects"
