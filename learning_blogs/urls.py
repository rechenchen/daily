"""define url mode of learning_logs"""

from django.urls import path,re_path
# . indicates Django imports views from the current directory
from . import views

urlpatterns = [
    # home
    path('', views.index, name='index'),
    # topics
    path('topics/', views.topics, name='topics'),
    # specified topic detail
    re_path('topics/(?P<topic_id>\d+)/', views.topic, name='topic'),
    # web page used to add new topics
    path('new_topic/', views.new_topic, name='new_topic'),
    # web page used to add new entries
    re_path('new_entry/(?P<topic_id>\d+)/', views.new_entry, name='new_entry'),
    re_path('edit_entry/(?P<entry_id>\d+)/', views.edit_entry, name='edit_entry'),
]
app_name = 'learning_blogs'