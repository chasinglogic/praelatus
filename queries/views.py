from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from guardian.shortcuts import get_objects_for_user

from tickets.models import Ticket

from .dsl import CompileException, compile_q
from .models import Query, QueryUse


def index(request):
    # Check if creating a new query model
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST['name']
        # The value in the html input escapes the quotes.
        # So we use replace calls to unescape them.
        query = request.POST['query'].\
            replace("\\'", "'").\
            replace('\\"', '"')
        qry = Query(owner=request.user, query=query, name=name)
        qry.save()

        qu = QueryUse(user=request.user, query=qry)
        qu.save()

        return redirect('/queries?query=' + query)

    query = request.GET.get('query')
    q = Q()
    error = None
    if query is not None:
        try:
            q = compile_q(query)
        except CompileException as e:
            error = str(e)

    users_projects = get_objects_for_user(request.user,
                                          'projects.view_project')
    tickets = Ticket.objects.filter(q).\
        filter(project__in=users_projects)

    if request.user.is_authenticated:
        recent_queries = QueryUse.objects.\
            filter(user=request.user).\
            order_by('-last_used')[:5]
        favorites = Query.favorites(request.user)
    else:
        recent_queries = []
        favorites = []

    return render(request, 'queries/index.html', {
        'tickets': tickets,
        'query': query,
        'error': error,
        'favorites': favorites,
        'recent_queries': recent_queries
    })


def query(request, id='0'):
    id = int(id)

    try:
        q = Query.objects.get(id=id)
    except Query.DoesNotExist:
        raise Http404()

    try:
        qu = QueryUse.objects.get(query=q, user=request.user)
        qu.last_used = datetime.now()
        qu.save()
    except QueryUse.DoesNotExist:
        qu = QueryUse(query=q, user=request.user)
        qu.save()

    return redirect('/queries?query=' + q.query)


@login_required
def mine(request):
    queries = Query.objects.filter(owner=request.user)
    return render(request, 'queries/mine.html', {'queries': queries})


def favorite(request, id='0'):
    id = int(id)

    try:
        q = Query.objects.get(id=id)
    except Query.DoesNotExist:
        raise Http404()

    if q.favorite:
        q.favorite = False
    else:
        q.favorite = True

    q.save()

    return redirect('/queries/mine')


def delete(request, id='0'):
    id = int(id)

    try:
        q = Query.objects.get(id=id)
    except Query.DoesNotExist:
        raise Http404()

    q.delete()
    return redirect('/queries/mine')
