from src.models import KeyValue


def set_value(message_text: str, chat_id: str, user_id: str):
    if len(message_text.split()) < 2:
        return "I need a key and a value"

    key, value = message_text.split(" ", 1)

    if not value.strip():
        return "Value cannot be empty"

    try:
        obj = KeyValue.get(chat_id + key)
        obj.user, obj.key, obj.value = user_id, key, value
        obj.save()
    except KeyValue.DoesNotExist:
        obj = KeyValue(chat_id + key, user=user_id, value=value)
        obj.save()

    return f"Value `{key}` has been assigned"


def get_value(message_text: str, chat_id: str, user_id: str):
    key = message_text.strip()

    if not key:
        return f"Send a key to search, ex: `/get key`"

    exists = KeyValue.count(chat_id + key)

    try:
        obj = KeyValue.get(chat_id + key)
        return obj.value
    except KeyValue.DoesNotExist:
        return "Key does not exists"


def delete_value(message_text: str, chat_id: str, user_id: str):
    key = message_text.strip()

    if not key:
        return "Send a key to delete"

    try:
        obj = KeyValue.get(chat_id + key)
        obj.delete()
        return f"Key `{key}` has been deleted"
    except KeyValue.DoesNotExist:
        return "Key does not exist"


def get_list(chat_id: str):
    results = list(KeyValue.scan(KeyValue.id.startswith(chat_id), limit=1))
    if results:
        return ", ".join(str(obj.id.replace(chat_id, "")) for obj in results)
    else:
        return "There are no objects"
