from django.shortcuts import get_object_or_404, render

from ticketus.core.models import Ticket

def ticket_page(request, ticket_id, template='ui/ticket_page.html'):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    context = {'ticket': ticket}
    return render(request, template, context)
