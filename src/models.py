import os

from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


class KeyValue(Model):
    id = UnicodeAttribute(hash_key=True)
    user = UnicodeAttribute()
    value = UnicodeAttribute()

    class Meta:
        table_name = os.environ["DYNAMODB_TABLE"]
        region = os.environ["REGION"]
        host = os.environ["DYNAMODB_HOST"]
