from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from ticketus.core.models import *
from ticketus.core.forms import *
from ticketus.tags.models import tags_by_occurence_count

def ticket_list(request, tag_filter=None, template='ui/ticket_list.html'):
    if tag_filter is None:
        tickets_list = Ticket.objects.all()
    else:
        tickets_list = Ticket.objects.filter(tag__tag_name=tag_filter).all()
    
    paginator = Paginator(tickets_list, settings.TICKETS_PER_PAGE)
    try:
        page = int(request.GET.get('page'))
    except TypeError:
        page = 1

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    context = {'tickets': tickets,
               'tag_filter': tag_filter,
               'pages': range(1, paginator.num_pages + 1),
               'previous_page': page - 1,
               'next_page': page + 1}
    return render(request, template, context)

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
            t = Ticket(title=form.cleaned_data['title'], requester=request.user)
            t.save()
            t.add_tags(form.cleaned_data['tags'])
            if form.cleaned_data['raw_text']:
                c = Comment(raw_text=form.cleaned_data['raw_text'], commenter=request.user)
                t.comment_set.add(c)
            return redirect(t)

    # don't pass the form instance in as we are manually creating it in the template
    context = {'top_tags': tags_by_occurence_count()}
    return render(request, template, context)
