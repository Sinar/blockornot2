from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OONIRecord(models.Model):
    STATUS_CHOICES = (
            ("OPEN", "Accessible"),
            ("BLOCKED", "Blocked")
            )
    report_id = models.CharField(max_length=255)
    test_start_time = models.DateTimeField()
    input_url = models.URLField()
    software_name = models.CharField(max_length=20)
    test_name = models.CharField(max_length=20)
    probe_asn = models.CharField(max_length=10)
    probe_cc = models.CharField(max_length=3)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


class SubmissionIP(models.Model):
    STATUS_CHOICES = (
            ("OPEN", "Not Submitted"),
            ("SUBMITTED", "Submitted"),
            ("REJECTED", "Rejected")
            )

    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    

class ISP(models.Model):
    asn = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
