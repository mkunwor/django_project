from django.db import models
import uuid

class BaseModel(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4,editable=False)
    created_ast=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True  #abstract doesn't make table

