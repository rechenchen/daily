from django import forms
# 从models.py导入Topic类
from .models import Topic, Entry

class TopicForm(forms.ModelForm): # TopicForm继承forms.ModelForm
    class Meta:
        model = Topic # 根据模型Topic创建表单model
        fields = ['text'] # 表单只包含text字段
        labels = {'text': ''} # 不要为labels生成标签

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

