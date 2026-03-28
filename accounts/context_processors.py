from .models import Notification, Message

def global_data(request):
    if request.user.is_authenticated:
        
        # ✅ Latest messages (FIXED: use sent_at instead of created_at)
        messages = Message.objects.filter(
            recipient=request.user
        ).order_by('-sent_at')[:5]

        # ✅ Unread messages count (FIXED: use is_read)
        unread_messages_count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        # ✅ Latest notifications (this one uses created_at correctly)
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

        # ✅ Unread notifications count (FIXED: use is_read)
        unread_notifications_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    else:
        messages = []
        notifications = []
        unread_messages_count = 0
        unread_notifications_count = 0

    return {
        'messages_list': messages,
        'notifications_list': notifications,
        'unread_messages_count': unread_messages_count,
        'unread_notifications_count': unread_notifications_count,
    }
