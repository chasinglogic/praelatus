from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render

from tickets.models import Ticket

from .dsl import CompileException, compile_q
from .models import Query


def index(request):
    # Check if creating a new query model
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST['name']
        # The value in the input escapes the quotes.
        # So we use replace calls to unescape them.
        query = request.POST['query'].\
            replace("\\'", "'").\
            replace('\\"', '"')
        qry = Query(owner=request.user, query=query, name=name)
        qry.save()
        return redirect('/queries?query=' + query)

    query = request.GET.get('query')
    q = Q()
    error = None
    if query is not None:
        try:
            q = compile_q(query)
        except CompileException as e:
            error = str(e)

    tickets = Ticket.objects.filter(q).all()
    return render(request, 'queries/index.html',
                  {
                      'tickets': tickets,
                      'query': query,
                      'error': error
                  })


def query(request, id='0'):
    id = int(id)

    try:
        q = Query.objects.get(id=id)
    except Query.DoesNotExist:
        raise Http404()

    q.last_used = datetime.now()
    q.save()

    return redirect('/queries?query=' + q.query)


@login_required
def mine(request):
    queries = Query.objects.filter(owner=request.user)
    return render(request, 'queries/mine.html',
                  {'queries': queries})
