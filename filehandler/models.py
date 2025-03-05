from django.db import models

# Create your models here.


class CSVUpload(models.Model):
    file = models.FileField(upload_to='csv_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Uploaded on {self.uploaded_at}"
