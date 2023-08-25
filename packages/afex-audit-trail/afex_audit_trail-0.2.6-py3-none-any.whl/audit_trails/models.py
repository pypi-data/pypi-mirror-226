from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from django.utils.timesince import timesince as timesince_


# Create your models here.


class NotificationQuerySet(QuerySet):

    def unread(self):
        return self.filter(is_read=False)

    def read(self):
        return self.filter(read=False)

    def mark_all_as_read(self):
        queryset = self.unread()
        return queryset.update(is_read=True)

    def mark_all_as_unread(self):
        queryset = self.read()
        return queryset.update(is_read=False)


class ActivityLog(models.Model):
    endpoint = models.CharField(max_length=256, null=True)
    request_method = models.CharField(max_length=10)
    exec_time = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    remote_address = models.CharField(max_length=30)
    request_body = models.TextField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    response_code = models.PositiveSmallIntegerField()
    error_message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activity_logs'
    )


LEVEL_CHOICES = (
    ('info', 'info'),
    ('success', 'success'),
    ('warning', 'warning'),
    ('error', 'error'),
)


class Notification(models.Model):
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='notifications',
        null=True,
        blank=True
    )
    actor = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=255)
    action_object = models.CharField(max_length=255, null=True, blank=True)
    action_target_object = models.CharField(max_length=255, null=True, blank=True)
    detail = models.TextField()
    meta_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = NotificationQuerySet.as_manager()

    @property
    def timesince(self, time=None):
        return timesince_(self.timestamp, time)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()

    def mark_as_unread(self):
        if self.is_read:
            self.is_read = False
            self.save()

    @property
    def description(self):
        return f"{self.actor} {self.action} {str(self.action_object)}"
