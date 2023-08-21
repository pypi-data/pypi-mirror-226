from django.contrib import admin

# Register your models here.
from django.contrib import admin
from nms_app.models import SetupProjectDetails, NodeDetails

# Register your models here.
admin.site.register(SetupProjectDetails)
admin.site.register(NodeDetails)
