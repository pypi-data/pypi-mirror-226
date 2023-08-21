from django.db import models


# Create your models here.

class NodeDetails(models.Model):
    nms_node_id = models.CharField(max_length=255, unique=True)


class SetupProjectDetails(models.Model):
    spd_node_id = models.CharField(max_length=50)
    spd_node_category = models.CharField(max_length=50)
    spd_ref_id = models.CharField(max_length=100)
    spd_download_location = models.CharField(max_length=255, blank=True)
    spd_download_start_time = models.DateTimeField(auto_now_add=True, blank=True)
    spd_download_end_time = models.DateTimeField(blank=True, null=True)
    spd_download_status = models.BooleanField(default=False)

