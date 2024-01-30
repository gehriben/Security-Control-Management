from django.db.models import Count

import numpy as np
import matplotlib.pyplot as plt
import os

from .models import Metric
from assets.models import AssetControlMatch
from tags.models import Tag
from properties.models import PropertyTag
from controls.models import Control
from assets.models import AssetControlMatch

GRAPH_PATH = "static/Graphs/"

class GraphController():
    def __init__(self):
        pass

    def create_graphs(self):
        self.create_controls_per_asset_distribution_graph()
        """self.create_keyword_per_security_control_tag_distribution_graph()
        self.create_keyword_per_property_tag_distribution_graph()
        self.create_control_per_security_control_tag_distribution_graph()
        self.create_property_per_property_tag_distribution_graph()
        self.create_matching_threshold_distribution()"""
        self.create_metrics_table()
        self.create_tfidf_matching_threshold_distribution()

    def create_controls_per_asset_distribution_graph(self):
        controls_per_assets = AssetControlMatch.objects.values('asset_id', 'asset__name').annotate(dcount=Count('asset_id')).order_by('-dcount')
        
        data = [controls_per_asset["dcount"] for controls_per_asset in controls_per_assets][:10]
        lables = [controls_per_asset["asset__name"] for controls_per_asset in controls_per_assets][:10]
    
        self.draw_pie_plot(data, lables, "Controls per Asset Distribution (Top 10)", "Assets", "controls_per_asset_distribution.png", sizeX=11, sizeH=13)

    def display_values_for_pie_chart(self, pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)
    
    def create_keyword_per_security_control_tag_distribution_graph(self):
        security_control_tags = Tag.objects.annotate(keywords_count=Count('keywords')).order_by('-keywords_count')[:30]
        data = [len(security_control_tag.keywords.all()) for security_control_tag in security_control_tags]
        labels =  [security_control_tag.name for security_control_tag in security_control_tags]

        self.draw_bar_plot(data, labels, "Keyword distribution per Security Control Tag (Top 30)", "security_control_tags_keyword_distribution.png", sizeH=12)
    
    def create_keyword_per_property_tag_distribution_graph(self):
        property_tags = PropertyTag.objects.all()
        property_tags_list = [{'name':property_tag.name, 'keyword_count': len(property_tag.property_keywords.split(";"))} for property_tag in property_tags]
        property_tags_list = sorted(property_tags_list, key=lambda k: k['keyword_count'], reverse=True) 

        data = [property_tag['keyword_count'] for property_tag in property_tags_list][:50]
        labels =  [property_tag['name'] for property_tag in property_tags_list][:50]

        self.draw_bar_plot(data, labels, "Keyword distribution per Property Tag", "property_tags_keyword_distribution.png", sizeH=12)

    def create_control_per_security_control_tag_distribution_graph(self):
        security_control_tags = Tag.objects.annotate(control_count=Count('control')).order_by('-control_count')[:50]
        data = [len(security_control_tag.control_set.all()) for security_control_tag in security_control_tags]
        labels =  [security_control_tag.name for security_control_tag in security_control_tags]

        self.draw_bar_plot(data, labels, "Control distribution per Security Control Tag (Top 50)", "security_control_tag_control_distribution.png", sizeH=10)
    
    def create_property_per_property_tag_distribution_graph(self):
        property_tags = PropertyTag.objects.annotate(property_count=Count('property')).order_by('-property_count')[:50]
        data = [len(property_tag.property_set.all()) for property_tag in property_tags]
        labels =  [property_tag.name for property_tag in property_tags]

        self.draw_bar_plot(data, labels, "Property distribution per Property Tag (Top 50)", "property_tag_property_distribution.png", sizeH=16)
    
    def create_matching_threshold_distribution(self):
        property_metric = Metric.objects.filter(name="Properties").first()
        matching_details = property_metric.other_metrics

        threshold_values = list()
        for matching_detail in matching_details:
            for property_tag in matching_detail["matched_tags"]:
                for property_tag_name, control_tags in property_tag.items():
                    for control_tag in control_tags:
                        for control_tag_name, value in control_tag.items():
                            threshold_values.append(round(value["matching_rate"]*100, 2))
        
        lables = list()
        data = list()

        splices_count = 10
        step_size = (max(threshold_values)-min(threshold_values))/splices_count
        min_value = min(threshold_values) + step_size
        max_value = max(threshold_values) + step_size
        for i in np.arange(min_value, max_value, step_size):
            threshold_count = 0
            for threshold_value in threshold_values:
                if threshold_value < round(i, 0) and threshold_value > round(i-step_size, 0):
                    threshold_count += 1
            if threshold_count != 0:
                data.append(threshold_count)
                lables.append(f"{round(i-step_size, 0)}% - {round(i, 0)}%")
        
        self.draw_pie_plot(data, lables, "Matching threshold distribution", "Thresholds", "matching_threshold_distribution.png")

    def create_tfidf_matching_threshold_distribution(self):
        tfidf_metric = Metric.objects.filter(name="TFIDF").first()
        matching_details = tfidf_metric.other_metrics

        threshold_values = list()
        for threshold_value, amount in matching_details.items():
            for i in range(amount):
                threshold_values.append(round(float(threshold_value)*100, 2))
        
        lables = list()
        data = list()

        splices_count = 10
        step_size = (max(threshold_values)-min(threshold_values))/splices_count
        min_value = min(threshold_values) + step_size
        max_value = max(threshold_values) + step_size
        for i in np.arange(min_value, max_value, step_size):
            threshold_count = 0
            for threshold_value in threshold_values:
                if threshold_value < round(i, 0) and threshold_value > round(i-step_size, 0):
                    threshold_count += 1
            if threshold_count != 0:
                data.append(threshold_count)
                lables.append(f"{round(i-step_size, 0)}% - {round(i, 0)}%")
        
        self.draw_bar_plot(data, lables, "TFIDF threshold distribution", "tfidf_threshold_distribution_bar.png", sizeX=13)
    
    def create_metrics_table(self):
        assets_with_controls = len(AssetControlMatch.objects.values('asset_id', 'asset__name').annotate(dcount=Count('asset_id')).order_by('-dcount'))
        column_header = ('Description', 'Value')

        for metric in Metric.objects.all():
            values = [['Name', metric.name],
                    ['Keywords', metric.keywords_counter],
                    ['Tags', metric.tags_counter],
                    ['Average Keywords per Tag', metric.average_keywords_per_tag],
                    ['Average Controls per Tag', metric.average_controls_per_tag],
                    ['Deleted Clusters', metric.deleted_clusters],
                    ['Matched Control Count', metric.matched_control_count],
                    ['Matched Tags', metric.matched_tags],
                    ['Assets with Controls', assets_with_controls]
            ]

            fig, ax = plt.subplots()
            # hide axes
            fig.patch.set_visible(False)
            ax.axis('off')
            ax.axis('tight')

            ax.table(cellText=values, colLabels=column_header)
            fig.tight_layout()
            plt.savefig(GRAPH_PATH+'/'+metric.name+'_metrics_table.png')

    def draw_bar_plot(self, data, lables, title, filename, sizeX=12, sizeH=6):
        plt.figure(figsize=(sizeX, sizeH))
        bar = plt.barh(lables, data)
        plt.title(title)
        plt.bar_label(bar, padding=10)
        plt.savefig(GRAPH_PATH+filename, bbox_inches='tight')
    
    def draw_pie_plot(self, data, lables, title, legend_title, filename, sizeX=10, sizeH=12):
        fig, ax = plt.subplots(figsize=(sizeX, sizeH), subplot_kw=dict(aspect="equal"))
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: self.display_values_for_pie_chart(pct, data),
                                  textprops=dict(color="w"))

        ax.legend(wedges, lables,
                title=legend_title,
                loc="lower center",
                bbox_to_anchor=(1.0, -0.2, -1, 1))

        plt.setp(autotexts, size=12, weight="bold")

        ax.set_title(title)

        plt.savefig(GRAPH_PATH+filename)
