# -*- encoding: utf-8 -*-

# Views for administration
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main.models import (
                                    Facture,
                                    Livre,
                                    Session,
                                    Vendeur,
                                    ETAT_LIVRE_CHOICES,
                                    Exemplaire,
                                    ISBN_DB_BASE_QUERY,
                                    COOP_UQAM_BASE_QUERY
                                   )
from datetime import datetime, timedelta, date

def index_admin(request):
    return redirect('/employee/')

@login_required()
def index_employee(request):
	return render(request, 'index.html')

def rapport(request):

	if 'date' in request.GET:
		date_init = request.GET['date']
		date = datetime.strptime(date_init,"%Y-%m-%d")
	else:
		date = datetime.today()
        date_init = date.today().strftime("%Y-%m-%d")

	lendemain = date + timedelta(days=1)

	# on met les deux dates a minuit
	date = date.replace(hour=0, minute=0, second=0)
	lendemain = lendemain.replace(hour=0, minute=0, second=0)

	ajoutes = Exemplaire.objects.all().filter(date_creation__gt=date,
		                                      date_creation__lt=lendemain)
	factures = Facture.objects.all().filter(date_creation__gt=date,
		                     date_creation__lt=lendemain)


	nb_ajoutes = ajoutes.count()

	nb_factures = factures.count()
	nb_vendus = sum([f.nb_livres() for f in factures])
	prix_total_vendu_avtaxes = sum([f.prix_avant_taxes() for f in factures])

	con_tax = {}

	# Si les taxes ne sont pas gérés, ces variables deviennent inutiles
	if settings.TAXABLES:
		prix_total_vendu_taxes = sum([f.prix_total() for f in factures])
		tps = sum([f.prix_tps() for f in factures])
		tvq = sum([f.prix_tvq() for f in factures])
		con_tax = {	'prix_total_taxes':prix_total_vendu_taxes or None,
		'prix_tps':tps or None,
		'prix_tvq':tvq or None
		}

	con_notax = {
		'date_init':date_init,
		'date':date.date(),
		'taxable':settings.TAXABLES,
		'nb_ajoutes':nb_ajoutes,
		'nb_factures':nb_factures,
		'nb_vendus':nb_vendus,
		'prix_total_avant_taxes':prix_total_vendu_avtaxes,
	}

	context = con_tax.copy()
	context.update(con_notax)

	return render(request, 'rapport.html', context)

