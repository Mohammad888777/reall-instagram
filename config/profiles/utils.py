from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def handle_paginator(obj,per_page,page):

    paginator=Paginator(obj,per_page=per_page)
    try:
        result=paginator.page(page)
    except PageNotAnInteger:
        result=paginator.page(1)
    except EmptyPage:
        result=paginator.page(paginator.num_pages)
    
    return result


