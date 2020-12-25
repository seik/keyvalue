import os

from pynamodb import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute


class KeyValue(Model):
    chat_id = NumberAttribute(hash_key=True)
    user = UnicodeAttribute()
    key = UnicodeAttribute()
    value = UnicodeAttribute()

    class Meta:
        table_name = os.environ["DYNAMODB_TABLE"]
        region = os.environ["REGION"]
        host = os.environ["DYNAMODB_HOST"]
