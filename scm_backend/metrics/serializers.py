from rest_framework import serializers
from .models import Metric


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('pk', 'name', 'keywords_counter', 'tags_counter', 'keyword_cluster_distributions', 
        'control_cluster_distributions', 'average_keywords_per_tag', 'average_controls_per_tag', 'matched_control_count', 'matched_tags', 'matching_tag_distribution')