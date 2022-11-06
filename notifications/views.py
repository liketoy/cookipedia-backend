from notifications import models


def create_notification(creator, to, kind, food=None, recipe=None, preview=""):

    notice = models.Notification.objects.create(
        creator=creator,
        to=to,
        kind=kind,
        food=food,
        recipe=recipe,
        preview=preview,
    )

    notice.save()
