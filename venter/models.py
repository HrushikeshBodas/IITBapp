from uuid import uuid4

from django.db import models

STATUS = (
    ('Reported', 'Reported'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Deleted', 'Deleted'),
)


class TagUris(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tag_uri = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Tag URI"
        verbose_name_plural = "Tag URIs"

    def __str__(self):
        return self.tag_uri


class Complaints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_by = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE,
                                   related_name="created_by")
    description = models.TextField(blank=True, null=True)
    report_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS, default='reported')
    latitude = models.FloatField(max_length=8, blank=True, null=True)
    longitude = models.FloatField(max_length=8, blank=True, null=True)
    location_description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(TagUris, related_name='tags', blank=True)
    users_up_voted = models.ManyToManyField('users.UserProfile', related_name='users_up_voted', blank=True)


    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ("-report_date",)

    def __str__(self):
        return self.description

class ComplaintMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    complaint = models.ForeignKey(Complaints, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    class Meta:
        verbose_name = "Complaint Medium"
        verbose_name_plural = "Complaint Media"

    def __str__(self):
        return str(self.image_url)
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    commented_by = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name="commented_by")
    complaint = models.ForeignKey(Complaints, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("-time",)

    def __str__(self):
        return self.text