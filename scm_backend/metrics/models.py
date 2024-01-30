from django.db import models

class Metric(models.Model):
    name = models.CharField(max_length=50)
    keywords_counter = models.IntegerField()
    tags_counter = models.IntegerField()
    keyword_cluster_distributions = models.JSONField()
    control_cluster_distributions = models.JSONField()
    average_keywords_per_tag = models.IntegerField()
    average_controls_per_tag = models.IntegerField()
    deleted_clusters = models.IntegerField(default=0)
    matched_control_count = models.IntegerField(default=0)
    matched_tags = models.IntegerField(default=0)
    matching_tag_distribution = models.JSONField()
    other_metrics = models.JSONField()

    def __str__(self):
        return self.name
