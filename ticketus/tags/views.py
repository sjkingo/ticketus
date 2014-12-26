from ticketus.core.models import Ticket
from ticketus.ui.utils import render_ticket_list

def filter_by_tag(request, tag_name):
    results = Ticket.objects.filter(tag__tag_name=tag_name).all()
    context = {'filter': tag_name,
               'filter_name': 'tag',
               'filter_label': 'tagged'}
    return render_ticket_list(request, results, context_to_add=context)
