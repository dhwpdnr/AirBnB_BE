from django.db import models
from common.models import CommonModel


class ChattingRoom(CommonModel):
    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
    )


class Messages(CommonModel):
    """Messages Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL
    )
    room = models.ForeignKey("direct_messages.ChattingRoom", on_delete=models.CASCADE)
