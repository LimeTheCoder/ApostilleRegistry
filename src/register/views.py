from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import Apostille

import datetime

def search(request):
	if request.method == 'POST':
		apostille_id = request.POST['id']
		date = request.POST['placing_date']

		try:
			apostille = Apostille.objects.get(id=apostille_id, placing_date=date)
		except Apostille.DoesNotExist:
			return render(request, 'register/search_page.html', {'error_msg' : "Apostille does not exist"})
		except:
			return render(request, 'register/search_page.html', {'error_msg' : "Incorrect data. Provide valid data."})

		request.session['form-submitted'] = True
		return redirect('apostille_detail', apostille.id)
	
	return render(request, 'register/search_page.html')


def apostille_detail(request, id):
	if not request.session.get('form-submitted', False):
		return HttpResponse("No such page")

	apostille = get_object_or_404(Apostille, pk=id)
	context = {'apostille' : apostille }
	request.session['form-submitted'] = False
	return render(request, 'register/apostille_detail.html', context)