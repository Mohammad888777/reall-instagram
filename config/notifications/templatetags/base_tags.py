from django import template
from ..models import Notification

register=template.Library()


@register.inclusion_tag("notifications/notifications_count.html",takes_context=True)
def all_nots(context):

    user=context["request"].user
    notifications=Notification.objects.select_related("post","comment","sender","receiver").filter(
        receiver=user,is_seen=False
    )
    if notifications.count()>0:
        return {
            'notifications':notifications.count()
        }


