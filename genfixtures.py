from django.contrib.auth.models import User
from tickets.models import Ticket, Comment, TicketType
from projects.models import Project
from fields.models import *
from workflows.models import *
from random import randint

admin = User.objects.create_superuser('testadmin', 'test@example.com', 'test',
                                      first_name='Test', last_name='Testerson II')
user = User.objects.create_user('testuser', 'test@example.com', 'test',
                                first_name='Test', last_name='Testerson')

admin.save()
user.save()

users = [admin, user]

p = Project(name='Dummy Project', lead=admin, key='TEST')

p.save()

high = FieldOption(name='High')
medium = FieldOption(name='Medium')
low = FieldOption(name='Low')

high.save()
medium.save()
low.save()

priorities = [high, medium, low]

story_points = Field(name='Story Points', data_type='INTEGER')
priority = Field(name='Priority', data_type='OPTION')
priority.save()
priority.options = priorities

story_points.save()
priority.save()

backlog = Status(name='Backlog')
in_progress = Status(name='In Progress')
done = Status(name='Done')

backlog.save()
in_progress.save()
done.save()

w = Workflow(name='Default Workflow')

w.save()

create = Transition(name='Create', to_status=backlog, workflow=w)
to_prog = Transition(name='In Progress', to_status=in_progress, from_status=backlog, workflow=w)
to_done = Transition(name='Done', to_status=done, from_status=in_progress, workflow=w)

to_done.save()
to_prog.save()
create.save()

bug = TicketType(name='Bug')
epic = TicketType(name='Epic')
feature = TicketType(name='Feature')

bug.save()
epic.save()
feature.save()

ticket_types = [bug, feature, epic]

for i in range(25):
    t = Ticket(key=p.key + '-' + str(i + 1),
               summary='This is ticket #' + str(i + 1),
               reporter=users[randint(0, 1)],
               assignee=users[randint(0, 1)],
               ticket_type=ticket_types[randint(0, 2)],
               project=p,
               status=backlog,
               workflow=w,
               description="""
# Utque erant et edentem suoque nox fertur

## Tegi aurum inridet flumine auras natas vulnus

Lorem markdownum misit sudor, sine eodem libratum munus aristis tutos, hac.
Longe mens vultus iurgia Iovem difficilis suus; ut erat mollis robore terga ei
perque! Quae quos sacrorum custodit quaecumque harena fallis et modo hinc
[recessu](http://venerat.com/), superorum Peleus, temptamenta. **Pudore** Sparte
lentisciferumque nataque inpulsos et ille novat haec sollicitare Plura, levis
vellet valuit, summo dum lutea viso. Solebat lintea ingentibus capillis dicta
Paridis seque quoquam [poposcit in](http://per.net/) Tempe vivacem.

1. Nate nulli
2. Coniunx hausi nunc Quirini Othrys
3. Caede nascuntur ubera congreditur vincula ubi regis
4. Spatium pectore amplexus ferunt ille instat cultores

Illo dolores voluit Achaemenias unde theatris paventem secum ineamus minacia
retro. Duplicataque siste suo recessit; opes albus moribunda referentem animam
nulloque domini et laborent hac?

## Senecta finita

Iovi nec aperire mihi mira respondit, qui exit vulnere aeterno dixerunt dat
corpus? Erit terrae, avidas; sola plenum, cauda edax et referre. Quater posuere:
facit mihi primaque remanet parte, eundo.
""")
    t.save()

    fvs = [
        FieldValue(field=story_points, int_value=randint(1, 20),
                   ticket=t),
        FieldValue(field=priority, opt_value=priorities[randint(0, 2)].name,
                   ticket=t)
    ]

    for fv in fvs:
        fv.save()




t = Ticket.objects.get(key='TEST-1')


for i in range(25):
    body = """"This is the %d th comment

# Yo Dawg

**I** *heard* you

> like markdown

so I put markdown in your comment"""
    c = Comment(body=body, author=users[randint(0,1)], ticket=t)
    c.save()
