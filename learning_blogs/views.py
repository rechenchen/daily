from django.shortcuts import render
from .models import Topic,Entry
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

# Create your views here.
def index(request):
    """  首页 """
    return render(request, 'learning_blogs/index.html')

@login_required
def topics(request):
    '''显示所有的主题'''
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'learning_blogs/topics.html',context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    # minus sign indicates descending sort
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_blogs/topic.html', context)

@login_required
def new_topic(request):
    """添加主题"""
    if request.method != 'POST':
        # didn't submit data: create a new form
        form = TopicForm # TopicForm is imported from ./form.py
    else:
        # data submitted through post: process the data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #form.save()
            # redirect user to topics page 将用户重定向到主题页
            return HttpResponseRedirect(reverse('learning_blogs:topics'))

    context = {'form': form}
    return render(request, 'learning_blogs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add a new entry in a specific topic 在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # no data submitted; create a new form
        form = EntryForm()
    else:
        # data submitted through post; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # create a new entry instance,
            # and store it in new_entry, but not in database yet(commit=False)
            new_entry = form.save(commit=False)
            # add topic attr & set it
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse('learning_blogs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_blogs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # first request; fill the form with old info
        form = EntryForm(instance=entry)
    else:
        # POST request; process the data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('learning_blogs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_blogs/edit_entry.html', context)

