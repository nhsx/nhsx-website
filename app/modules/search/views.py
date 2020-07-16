from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):

    EXCLUDE = []

    search_query = request.GET.get("query", "")
    page = request.GET.get("page", 1)

    # Promoted searches
    promoted = Query.get(search_query).editors_picks.all()

    # Ensure promoted pages don't show up twice
    if len(promoted) > 0:
        EXCLUDE += [_.page.id for _ in promoted]

    # Search
    if search_query:
        search_results = (
            Page.objects.exclude(id__in=EXCLUDE).live().search(search_query)
        )
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    objects = [r.page for r in promoted] + [r for r in search_results]

    # Pagination
    paginator = Paginator(objects, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search.html",
        {"search_query": search_query, "search_results": search_results,},
    )
