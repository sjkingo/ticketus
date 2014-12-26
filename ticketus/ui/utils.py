from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def render_ticket_list(request, results, context_to_add={}, template='ui/ticket_list.html'):
    paginator = Paginator(results, settings.TICKETS_PER_PAGE)
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
               'pages': range(1, paginator.num_pages + 1),
               'previous_page': page - 1,
               'next_page': page + 1,
               'filter': None,
               'filter_label': None,
               'filter_name': None}
    for k, v in context_to_add.items():
        context[k] = v
    return render(request, template, context)
