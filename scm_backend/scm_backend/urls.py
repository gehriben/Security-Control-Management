"""scm_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from assets import views as views_assets
from properties import views as views_properties
from controls import views as views_controls
from tags import views as views_tags
from nlp import views as views_nlp
from metrics import views as views_metrics
from constraints import views as views_constraints

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/assets/$', views_assets.assets),
    path('api/asset/<int:pk>/', views_assets.asset),
    re_path(r'^api/assettypes/$', views_assets.assettypes),
    re_path(r'^api/asset_control_matches/$', views_assets.asset_control_matches),
    re_path(r'^api/import_assets/$', views_assets.import_assets),
    re_path(r'^api/properties/$', views_properties.properties),
    path('api/property/<int:pk>/', views_properties.property),
    re_path(r'^api/property_tags/$', views_properties.property_tags),
    re_path(r'^api/controls/$', views_controls.controls),
    path('api/control/<int:pk>/', views_controls.control),
    re_path(r'^api/parent_controls/$', views_controls.parent_controls),
    path('api/child_controls/<int:parent_pk>/', views_controls.child_controls),
    re_path(r'^api/tags/$', views_tags.tags),
    path('api/tag/<int:pk>/', views_tags.tag),
    re_path(r'^api/keywords/$', views_tags.keywords),
    path('api/keyword/<int:pk>/', views_tags.keyword),
    re_path(r'^api/importControls/$', views_nlp.import_controls),
    re_path(r'^api/analyseControls/$', views_nlp.analyse_controls),
    re_path(r'^api/matchControls/$', views_nlp.match_controls),
    re_path(r'^api/tfidf_matching/$', views_nlp.tfidf_matching),
    re_path(r'^api/matching_controls_with_assets/$', views_nlp.matching_controls_with_assets),
    path('api/matching_controls_with_asset/<int:asset_id>/', views_nlp.matching_controls_with_asset),
    re_path(r'^api/metrics/$', views_metrics.metrics),
    re_path(r'^api/create_graphs/$', views_metrics.create_graphs),
    re_path(r'^api/constraints/$', views_constraints.constraints),
    path('api/constraint/<int:pk>/', views_constraints.constraint),
    re_path(r'^api/constraint_type/$', views_constraints.constraint_type),
    path('api/constraint_for_asset/<int:pk>/', views_constraints.constraint_for_asset),
    path('api/constraint_association/<int:pk>/', views_constraints.constraint_association)   
]
