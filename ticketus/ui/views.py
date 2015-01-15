from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .utils import render_ticket_list
from ticketus.core.models import *
from ticketus.core.forms import *
from ticketus.tags.models import tags_by_occurence_count

def ticket_list_all(request):
    results = Ticket.objects.exclude(tag__tag_name='closed').all()
    context = {'filter': '!= closed',
               'filter_name': 'status',
               'filter_label': 'with status'}
    return render_ticket_list(request, results, context_to_add=context)

def ticket_list_by_user(request, username):
    results = Ticket.objects.filter(requester__username=username).all()
    context = {'filter': username,
               'filter_name': 'user',
               'filter_label': 'by user'}
    return render_ticket_list(request, results, context_to_add=context)

def ticket_page(request, ticket_id, template='ui/ticket_page.html'):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {'ticket': ticket}
    return render(request, template, context)

@require_POST
@login_required
def post_new_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = Comment(raw_text=form.cleaned_data['raw_text'], commenter=request.user)
        ticket.comment_set.add(c)
    return redirect(ticket)

@login_required
def new_ticket(request, template='ui/new_ticket.html'):
    """
    Post a new ticket (and comment).
    """
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            t = Ticket(title=form.cleaned_data['title'], requester=request.user,
                    imported_key=None)
            t.save()
            t.add_tags(form.cleaned_data['tags'])
            if form.cleaned_data['raw_text']:
                c = Comment(raw_text=form.cleaned_data['raw_text'], commenter=request.user)
                t.comment_set.add(c)
            return redirect(t)

    # don't pass the form instance in as we are manually creating it in the template
    context = {'top_tags': tags_by_occurence_count()}
    return render(request, template, context)
