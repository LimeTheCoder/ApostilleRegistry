from django.shortcuts import get_object_or_404, render, redirect

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from .models import Apostille

import datetime
import pdfkit

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

	if 'to_pdf_btn' in request.GET:
		apostille = get_object_or_404(Apostille, pk=id)
		context = {'apostille' : apostille, 'export_mode' : True}
		request.session['form_submitted'] = True
		return render_to_pdf('register/apostille_detail.html', context)


	if not request.user.is_staff and not request.session.get('form-submitted', False):
		return HttpResponse("No such page")

	apostille = get_object_or_404(Apostille, pk=id)
	context = {'apostille' : apostille, 'export_mode' : False}
	request.session['form-submitted'] = False
	return render(request, 'register/apostille_detail.html', context)


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    
    options = {
		'page-size': 'Letter',
		'margin-top': '0.75in',
		'margin-right': '0.75in',
		'margin-bottom': '0.75in',
		'margin-left': '0.75in',
		'encoding': "UTF-8"
	}

    pdf = pdfkit.from_string(html, False, options=options)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    
    return response