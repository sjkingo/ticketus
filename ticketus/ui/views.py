from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from ticketus.core.models import *
from ticketus.core.forms import CommentForm

def ticket_list(request, template='ui/ticket_list.html'):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, template, context)

def ticket_page(request, ticket_id, template='ui/ticket_page.html'):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {'ticket': ticket}
    return render(request, template, context)

@require_POST
def post_new_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = Comment(raw_text=form.cleaned_data['raw_text'], commenter=request.user)
        ticket.comment_set.add(c)
    return redirect(ticket)
