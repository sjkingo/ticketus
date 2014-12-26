from ticketus.ui.views import ticket_list

def filter_by_tag(request, tag_name):
    return ticket_list(request, tag_filter=tag_name)
