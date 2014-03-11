from django.conf.urls import patterns, include, url
from heatmap.views import getHeatMap

urlpatterns = patterns('',

    url(r'^getHeatMap/', getHeatMap),
)
