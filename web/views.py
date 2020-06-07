from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .models import Activity, Source, Receptor, Ligand
import psycopg2
from django.template.defaultfilters import register
from django.http import HttpResponse
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import inchi
import os
from django import forms
from .forms import SearchForm
from .forms import DownloadForm
from django.forms import ModelForm
import ast
import csv
from django.http import HttpResponse
from datetime import datetime

#making dictionaries for lookup receptor, ligand and source
conn = psycopg2.connect('dbname=chembdb user=data host=/tmp/')
curs1 = conn.cursor()
curs1.execute("select ligand_id, inchi from ligand")
ligand_d = curs1.fetchall()
ligand_dict = dict(ligand_d)
curs2 = conn.cursor()
curs2.execute("select receptor_id, uniprot_name from receptor")
receptor_dict = dict(curs2.fetchall())
curs3 = conn.cursor()
curs3.execute("select source_id, article_doi from source")
source_dict = dict(curs3.fetchall())

global similar_dict
similar_dict = {}

#drawing and saving picture of ligand, if not exists
for i in ligand_d:
	exists = os.path.isfile('/home/adam/django_database/web/static/web/inchi/ligand_' + str(i[0]) + '.png')
	if not exists:
		m = inchi.MolFromInchi(i[1], sanitize=False)
		if m != None and m != '':
			Draw.MolToFile(m, '/home/adam/django_database/web/static/web/inchi/ligand_' + str(i[0]) + '.png')

class ActivityList(ListView):
	model = Activity
	def get_context_data(self, **kwargs):
		context = super(ActivityList, self).get_context_data(**kwargs)
		return context

class ReceptorList(ListView):
	model = Receptor
	def get_context_data(self, **kwargs):
		context = super(ReceptorList, self).get_context_data(**kwargs)
		return context

class ActivityDetail(DetailView):
	model = Activity
	def get_context_data(self, **kwargs):
		context = super(ActivityDetail, self).get_context_data(**kwargs)
		return context


class ReceptorDetail(DetailView):
        model = Receptor
        def get_context_data(self, **kwargs):
                context = super(ReceptorDetail, self).get_context_data(**kwargs)
                return context

class LigandDetail(DetailView):
	model = Ligand
	def get_context_data(self, **kwargs):
		context = super(LigandDetail, self).get_context_data(**kwargs)
		return context

class SourceDetail(DetailView):
	model = Source
	def get_context_data(self, **kwargs):
		context = super(SourceDetail, self).get_context_data(**kwargs)
		return context


#lookup for ligand, receptor, source and tanimoto, called from template "activity_list_search.html"  
@register.filter(name = 'lookup_ligand')
def getLigVal(ligand_dict, ligand_id):
	return ligand_dict.get(ligand_id)

@register.filter(name = 'lookup_receptor')
def getRecVal(receptor_dict, receptor_id):
	return receptor_dict.get(receptor_id)

@register.filter(name = 'lookup_source')
def getSourVal(source_dict, source_id):
	return source_dict.get(source_id)

@register.filter(name = 'lookup_similar')
def getSimilarityVal(similar_dict, ligand_id):
	return similar_dict.get(ligand_id)
	

#sorting of results from teplate "activity_list.html"
#!!! it is NOT activity_list_search, sorting after search is down below, this is sorting of all activities
def activity(request):
	sort = request.GET.get('sort')
	objects = Activity.objects.all()
	if sort == 'uniprot_sort':
		objects = objects.order_by('receptor_id')
	elif sort == 'uniprot_reverse_sort':
		objects = objects.order_by('-receptor_id')
	elif sort == 'ligand_sort':
		objects = objects.order_by('ligand_id')
	elif sort == 'ligand_reverse_sort':
		objects = objects.order_by('-ligand_id')
	elif sort == 'doi_sort':
		objects = objects.order_by('source_id')
	elif sort == 'doi_reverse_sort':
		objects = objects.order_by('-source_id')
	elif sort == 'type_sort':
		objects = objects.order_by('type')
	elif sort == 'type_reverse_sort':
		objects = objects.order_by('-type')
	elif sort == 'relation_sort':
		objects = objects.order_by('relation')
	elif sort == 'relation_reverse_sort':
		objects = objects.order_by('-relation')
	elif sort == 'value_sort':
		objects = objects.order_by('value')
	elif sort == 'value_reverse_sort':
		objects = objects.order_by('-value')
	elif sort == 'unit_sort':
		objects = objects.order_by('unit')
	elif sort == 'unit_reverse_sort':
		objects = objects.order_by('-unit')
	elif sort == 'source_db_sort':
		objects = objects.order_by('source_db')
	elif sort == 'source_db_reverse_sort':
		objects = objects.order_by('-source_db')
	list_of_all = []
	total = len(objects)
	for k in objects:
		list_of_all.append(k.activity_id)
	paginator = Paginator(objects, 30)
	page = request.GET.get('page')
	act = paginator.get_page(page)
	context = {
		'page': page,
		'total': total,
		'sort': sort,
		'act': act,
		'title': 'Activities',
		'source_dict': source_dict,
		'receptor_dict': receptor_dict,
		'ligand_dict': ligand_dict,
		'list_of_all': list_of_all,
		'activate': 'web-activity',
	}

	return render(request, 'web/activity.html', context)


#detail of one activity
def activity_detail(request, activity_id):
	act = get_object_or_404(Activity, activity_id=activity_id)
	title = ('Activity: ' + activity_id)
	context = {
		'act': act,
		'title': title,
		'source_dict': source_dict,
		'receptor_dict': receptor_dict,
		'ligand_dict': ligand_dict,
	}
	return render(request, 'web/activity_detail.html', context)

#list of all receptors
def receptor(request):
	rec_objects = Receptor.objects.all()
	total = len(rec_objects)
	paginator = Paginator(rec_objects, 30)
	page = request.GET.get('page')
	rec = paginator.get_page(page)
	context = {
		'rec': rec,
		'title': 'Receptors',
		'total': total,
		'activate': 'web-receptor',
	}
	return render(request, 'web/receptor.html', context)

#detail of one receptor
def receptor_detail(request, receptor_id):
	rec = get_object_or_404(Receptor, receptor_id=receptor_id)
	title = ('Receptor: ' + receptor_id)
	context = {
		'rec': rec,
		'title': title 
	}
	return render(request, 'web/receptor_detail.html', context)

#detail of one ligand
def ligand_detail(request, ligand_id):
	lig = get_object_or_404(Ligand, ligand_id=ligand_id)
	title = ('Ligand: ' + ligand_id)
	context = {
		'lig': lig,
		'title': title
	}
	return render(request, 'web/ligand_detail.html', context)

#detail of one source
def source_detail(request, source_id):
	sour = get_object_or_404(Source, source_id=source_id)
	title = ('Source: ' + source_id)
	context = {
		'sour': sour,
		'title': title
	}
	return render(request, 'web/source_detail.html', context)

#home page
def home(request):
	return render(request, 'web/home.html', {'title': 'Home'})

#about page
def about(request):
	return render(request, 'web/about.html', {'title': 'About', 'activate': 'web-about'})

#help pages
def search_help(request):
	return render(request, 'web/search_help.html', {'title': 'Search help'})

def activity_list_help(request):
	return render(request, 'web/activity_list_help.html', {'title': 'Activity list help'})

def activity_detail_help(request):
	return render(request, 'web/activity_detail_help.html', {'title': 'Activity detail help'})

def receptor_list_help(request):
	return render(request, 'web/receptor_list_help.html', {'title': 'Receptor list help'})

def receptor_detail_help(request):
	return render(request, 'web/receptor_detail_help.html', {'title': 'Receptor detail help'})

def ligand_detail_help(request):
	return render(request, 'web/ligand_detail_help.html', {'title': 'Ligand detail help'})

def source_detail_help(request):
	return render(request, 'web/source_detail_help.html', {'title': 'Source detail help'})

#drawing of ligand page
def ketcher(request):
	return render(request, 'web/ketcher.html', {'title': 'Ketcher'})

#download of selected activities in "activity_list_search.html"
#returns list of chosen activity_IDs 
def export_selected(request):
	selected = request.GET.getlist('check[]')
	ligand = request.GET.get('ligand')
	if ligand == None:
		ligand = ''
	selected = list(map(int, selected))
	return make_export_file(selected, ligand)
	
#download of all activites from search in "activity_list_search.html"
#returns list of chosen activity_IDs  
def export(request):
	list_of_all = ''
	ligand = ''
	form = DownloadForm(request.POST)
	if form.is_valid():
		list_of_all = form.cleaned_data['list_of_all']
		ligand = form.cleaned_data['ligand']
	print ("List:" + list_of_all)
	print ("Ligand:" + ligand)
	list_of_all = ast.literal_eval(list_of_all)
	return make_export_file(list_of_all, ligand)

#making export file 
def make_export_file(data, ligand):
	from datetime import datetime
	now = datetime.now() # current date and time
	date_time = now.strftime("__%Y_%m_%d__%H_%M_%S")
	name = "export_data" + date_time + ".csv"
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = ('attachment; filename=' + name)
	writer = csv.writer(response, delimiter=";")
	#first line of csv file
	first = ["Activity id", "Source", "Receptor", "Ligand Inchi", "Tanimoto", "Type", "Relation", "Value", "Unit", "p_chembl", "Confidence score", "pH", "Temperature", "Source database(s)"]
	writer.writerow(first)
	#creating new similar dictionary
	curs_tanimoto = conn.cursor()
	curs_tanimoto.execute("select cid, similarity from get_mfp2_neighbors2('" + str(ligand) + "');")
	tanimoto_help = curs_tanimoto.fetchall()
	for a in tanimoto_help:
		similar_dict[a[0]] = round(a[1], 2)
	#inserting data
	for p in data:
		curs_export = conn.cursor()
		curs_export.execute("select * from activity where activity_id=" + str(p) + ";")
		line = curs_export.fetchone()
		line = list(line) #one line of csv file
		if ligand != 'None' and ligand != '':
			line.insert(4,  similar_dict[int(line[3])])
		else:
			line.insert(4, '')
		line[1] = source_dict[int(line[1])] #replace source_id for source (making dict in the beginning of this file)
		line[2] = receptor_dict[int(line[2])] #replace receptor_id for its name (making dict in the beginning of this file)
		line[3] = ligand_dict[int(line[3])] #replace ligand_id for inchi (making dict in the beginning of this file)
		writer.writerow(line)
	return response

def search(request):
	#every variable in context HAS to be created here, because rest of function "search" is in "if" part and the first page (before searching) wouldn't load properly
	receptor = ''
	ligand_type = ''
	inchi = ''
	tanimoto = ''
	without_metals = ''
	confidence_score = ''
	source_db = ''
	source = ''
	relation = ''
	types = ''
	value = ''
	total = ''
	#global similar_dict #similar_dict must be global, because it is used in functions up here
	similar_dict = {}
	value_between_smaller = ''
	value_between_bigger = ''
	sort = request.GET.get('sort')
	page = request.GET.get('page')
	if request.method == 'POST' or page != None:
		form = SearchForm(request.POST)
		if request.method == 'POST': #if from form
			if form.is_valid():
				receptor = form.cleaned_data['receptor']
				source_db = form.cleaned_data['source_db']
				inchi = form.cleaned_data['inchi']
				ligand_type = form.cleaned_data['ligand_type']
				tanimoto = form.cleaned_data['tanimoto']
				without_metals = form.cleaned_data['without_metals']
				relation = form.cleaned_data['relation']
				types = form.cleaned_data['types']
				value = form.cleaned_data['value']
				value_between_smaller = form.cleaned_data['value_between_smaller']
				value_between_bigger = form.cleaned_data['value_between_bigger']
				confidence_score = form.cleaned_data['confidence_score']
		else: #if from html page (for example "next page" or sorting, it is used as method GET, not form)
			receptor = request.GET.get('receptor')
			receptor = ast.literal_eval(receptor)
			source_db = request.GET.get('source_db')
			inchi = request.GET.get('inchi')
			ligand_type = request.GET.get('ligand_type')
			tanimoto = request.GET.get('tanimoto')
			without_metals = request.GET.get('without_metals')
			relation = request.GET.get('relation')
			types = request.GET.get('types')
			types = ast.literal_eval(types)
			value = request.GET.get('value')
			value_between_smaller = request.GET.get('value_between_smaller')
			value_between_bigger = request.GET.get('value_between_bigger')
			confidence_score = request.GET.get('confidence_score')
			confidence_score = ast.literal_eval(confidence_score)
		if not page:
			page = 1

		#getting gid of commas
		if "," in str(value):
			value = str(value).replace(",",".")
		if "," in str(value_between_smaller):
			value_between_smaller = str(value_between_smaller).replace(",",".")
		if "," in str(value_between_bigger):
			value_between_bigger = str(value_between_bigger).replace(",",".")
		#confidence score query, if empty in form
		if not confidence_score:
			confidence_score = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		#types query, if empty in form
		if not types:
			types = ['EC50', 'IC50', 'Ki', 'Kd']


		#receptor query
		if receptor: #if some receptor is chosen
			rec_list = []
			rec_list = receptor
		else: #if not, choose every receptor
			curs_rec = conn.cursor()
			curs_rec.execute("select receptor_id from receptor;")
			rec_help = curs_rec.fetchall()
			rec_list = []
			for i in rec_help:
				rec_list.append(i[0])


		#ligand query
		curs_inchi = conn.cursor()
		if inchi != '': #if some ligand is written
			if ligand_type == 'exact': #exact search
				e = ("select ligand_id, 0 as help from ligand where (inchi ILIKE '" + str(inchi) + "') or (inchi_bdb ILIKE '" + str(inchi) + "') or (inchi_chembl ILIKE '" + str(inchi) + "') or (smiles ILIKE '" + str(inchi) + "');")
				curs_inchi.execute(e)
			else: #for now similarity search, it could be "if ligand_type == 'similar':" as well, but now I have only two options
				small_inchi = inchi.lower() 
				if small_inchi.startswith('inchi'): #check, if user wrote inchi
					inchi = "InChI" + inchi[5:] #replace every weird formulations, like "INCHI" or "inCHI" for "InChI"
					inchi = Chem.MolToSmiles(Chem.MolFromInchi(inchi)) #replace InChI for Smiles
				if ',' in str(tanimoto):
					tanimoto = str(tanimoto).replace(",",".")
				if str(tanimoto) == '':
					tanimoto = 0.8
				s = ("select cid, similarity from get_mfp2_neighbors2('" + str(inchi) + "') where similarity >= " + str(tanimoto) + ";")
				curs_inchi.execute(s)
		else:
			curs_inchi.execute("select ligand_id, 0 as help from ligand;") #if there's no ligand written, selected every ligand... and "0" instead of tanimoto
		lig_help = curs_inchi.fetchall()
		lig_inchi = []
		for i in lig_help:
			lig_inchi.append(i[0])
		for a in lig_help:
			if a[1] != 0: #if some ligand is chosen
				similar_dict[a[0]] = round(a[1], 2) #tanimoto rounded for 2 decimals
			else: #if not
				similar_dict[a[0]] = '' #tanimoto is ''
		
		#metal query, if user wants all elements, or just chosen 
		curs_metal = conn.cursor()
		if without_metals == True: #wants just chosen
			curs_metal.execute("select ligand_id from ligand where no_metal=true")
		else: #wants everything
			curs_metal.execute("select ligand_id from ligand;")
		lig_metal_help = curs_metal.fetchall()
		lig_metal = []
		for i in lig_metal_help:
			lig_metal.append(i[0])

		#ligands together (metal query and ligand query joining together)
		lig_list = list(set(lig_inchi) & set(lig_metal)) 


		#source query
		if source_db == 'chembdb':
			source = 'Chembl, BDB'
		if source_db == 'chembl':
			source = 'Chembl'
		if source_db == 'bdb':
			source = 'BDB'

		#value query, check, if value is really a number
		if (not value.replace('.','').isdigit()) and ((not value_between_smaller.replace('.','',1).isdigit()) or (not value_between_bigger.replace('.','',1).isdigit())):
			relation = 'noth'

		#query itself, searching in table of activity and choosing only correct results
		#query works like a tree
		if relation != 'noth': #user chose "=, <, >, between"
			if source_db != 'everything': #user chose some source database
				if relation == 'equal':
					results = Activity.objects.filter(Q(value=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(source_db=source) & Q(confidence_score__in=confidence_score))
				elif relation == 'smaller':
					results = Activity.objects.filter(Q(value__lt=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(source_db=source) & Q(confidence_score__in=confidence_score))
				elif relation == 'bigger':
					results = Activity.objects.filter(Q(value__gt=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(source_db=source) & Q(confidence_score__in=confidence_score))
				elif relation == 'between':
					results = Activity.objects.filter(Q(value__gt=value_between_smaller) & Q(value__lt=value_between_bigger) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(source_db=source) & Q(confidence_score__in=confidence_score))
			else: #wants in all databases, Q(source_db=source) is missing
				if relation == 'equal':
					results = Activity.objects.filter(Q(value=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(confidence_score__in=confidence_score))
				elif relation == 'smaller':
					results = Activity.objects.filter(Q(value__lt=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(confidence_score__in=confidence_score))
				elif relation == 'bigger':
					results = Activity.objects.filter(Q(value__gt=value) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(confidence_score__in=confidence_score))
				elif relation == 'between':
					results = Activity.objects.filter(Q(value__gt=value_between_smaller) & Q(value__lt=value_between_bigger) & Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(confidence_score__in=confidence_score))
		elif relation =='noth': #wants every relation, Q(value...=value )is missing and now there's Q(value__icontains=value)
			if source_db != 'everything': #the same as before, chose some source database
				results = Activity.objects.filter(Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(value__icontains=value) & Q(source_db=source) & Q(confidence_score__in=confidence_score))
			else: #user did not choose either relation and source database
				results = Activity.objects.filter(Q(receptor_id__in=rec_list) & Q(ligand_id__in=lig_list) & Q(type__in=types) & Q(value__icontains=value) & Q(confidence_score__in=confidence_score))

		list_of_all = []
		total = len(results)
		for k in results:
			list_of_all.append(k.activity_id)
		#sorting
		if sort == 'uniprot_sort':
			results = results.order_by('receptor_id')
		elif sort == 'uniprot_reverse_sort':
			results = results.order_by('-receptor_id') #opposite sorting of receptor
		elif sort == 'ligand_sort':
			results = results.order_by('ligand_id')
		elif sort == 'ligand_reverse_sort':
			results = results.order_by('-ligand_id')
		elif sort == 'doi_sort':
			results = results.order_by('source_id')
		elif sort == 'doi_reverse_sort':
			results = results.order_by('-source_id')
		elif sort == 'type_sort':
			results = results.order_by('type')
		elif sort == 'type_reverse_sort':
			results = results.order_by('-type')
		elif sort == 'relation_sort':
			results = results.order_by('relation')
		elif sort == 'relation_reverse_sort':
			results = results.order_by('-relation')
		elif sort == 'value_sort':
			results = results.order_by('value')
		elif sort == 'value_reverse_sort':
			results = results.order_by('-value')
		elif sort == 'unit_sort':
			results = results.order_by('unit')
		elif sort == 'unit_reverse_sort':
			results = results.order_by('-unit')
		elif sort == 'source_db_sort':
			results = results.order_by('source_db')
		elif sort == 'source_db_reverse_sort':
			results = results.order_by('-source_db')
		paginator = Paginator(results, 30)
		act = paginator.get_page(page)
				
	else: #possibility of some error
		act = ''
		page = ''
		list_of_all = []
		form = SearchForm()
	context = { 
		'sort': sort,
		'form': form,
		'page': page,
		'receptor': receptor,
		'source_db': source_db,
		'ligand_type': ligand_type,
		'tanimoto': tanimoto,
		'inchi': inchi,
		'without_metals': without_metals,
		'relation': relation,
		'types': types,
		'value': value,
		'value_between_smaller': value_between_smaller,
		'value_between_bigger': value_between_bigger,
		'act': act,
		'total': total,
		'list_of_all': list_of_all,
		'source_dict': source_dict,
		'receptor_dict': receptor_dict,
		'ligand_dict': ligand_dict,
		'similar_dict': similar_dict,
		'confidence_score': confidence_score,
		'activate': 'web-search',
	}

	return render(request, 'web/search.html', context)


