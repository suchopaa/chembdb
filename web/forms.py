
from django import forms

class SearchForm(forms.Form):
	#receptor has to be receptor_ID from database
	RECEPTORS = (('1','Thyroid hormone receptor alpha'),('2','Thyroid hormone receptor beta'),('3','Retinoic acid receptor alpha'),('4','Retinoic acid receptor beta'),('5','Retinoic acid receptor gamma'),('6','Peroxisome proliferator-activated receptor alpha'),('7','Peroxisome proliferator-activated receptor delta'),('8','Peroxisome proliferator-activated receptor gamma'),('9','Nuclear receptor subfamily 1 group D member 1'),('10','Nuclear receptor subfamily 1 group D member 2'),('11','Nuclear receptor ROR-alpha'),('12','Nuclear receptor ROR-beta'),('13','Nuclear receptor ROR-gamma'),('14','LXR-beta'),('15','LXR-alpha'),('16','Bile acid receptor FXR'),('17','Vitamin D receptor'),('18','Pregnane X receptor'),('19','Nuclear receptor subfamily 1 group I member 3'),('20','Hepatocyte nuclear factor 4-alpha'),('21','Hepatocyte nuclear factor 4-gamma'),('22','Retinoid X receptor alpha'),('23','Retinoid X receptor beta'),('24','Retinoid X receptor gamma'),('25','Nuclear receptor subfamily 2 group C member 1'),('26','Nuclear receptor subfamily 2 group C member 2'),('27','Nuclear receptor subfamily 2 group E member 1'),('28','Retina-specific nuclear receptor'),('29','COUP transcription factor 1'),('30','COUP transcription factor 2'),('31','Nuclear receptor subfamily 2 group F member 6'),('32','Estrogen receptor alpha'),('33','Estrogen receptor beta'),('34','Estrogen-related receptor alpha'),('35','Estrogen-related receptor beta'),('36','Estrogen-related receptor gamma'),('37','Glucocorticoid receptor'),('38','Mineralocorticoid receptor'),('39','Progesterone receptor'),('40','Androgen Receptor'),('41','Nuclear receptor subfamily 4 group A member 1'),('42','Nuclear receptor subfamily 4 group A member 2'),('43','Nuclear receptor subfamily 4 group A member 3'),('44','Steroidogenic factor 1'),('45','Orphan nuclear receptor LRH-1'),('46','Nuclear receptor subfamily 6 group A member 1'),('47','Nuclear receptor subfamily 0 group B member 1'),('48','Nuclear receptor subfamily 0 group B member 2'),)
	CONFIDENCE_SCORE = (('0','0 or Unknown'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),)
	TYPES = (('EC50','EC50 (nM)'),('IC50','IC50 (nM)'),('Ki','Ki (nM)'),('Kd','Kd (nM)'),)
	receptor = forms.MultipleChoiceField(choices=RECEPTORS, required=False, label='Receptor')
	inchi = forms.CharField(required=False, label='Ligand Inchi or Smiles', widget=forms.TextInput(attrs={'placeholder': 'InChI=...   |   C1=CC=CC...'}))
	ligand_type = forms.ChoiceField(choices=[('exact', 'Exact search of ligand'), ('similar', 'Similarity search of ligand')], label='', widget = forms.Select(attrs = {'onchange' : "Tanimoto();"}))
	tanimoto = forms.ChoiceField(choices=[('1','Tanimoto = 1'),('0.9','Tanimoto >= 0.9'),('0.8','Tanimoto >= 0.8'),('0.7','Tanimoto >= 0.7'),('0.6','Tanimoto >= 0.6'),('0.5','Tanimoto >= 0.5')], label='')
	types = forms.MultipleChoiceField(choices=TYPES, required=False, label='Physical quantity')
	relation = forms.ChoiceField(choices=[('noth', 'any'),('equal', 'equal to'),('smaller', 'less than'),('bigger', 'greater than'),('between', 'between')], label='Is', required=False, widget = forms.Select(attrs = {'onchange' : "Between();"}))
	value = forms.CharField(required=False, label='The following value:', widget=forms.TextInput(attrs={'placeholder': 'Number (nM)','type':'number','min':'0', 'step': '1'}))
	value_between_smaller = forms.CharField(required=False, label='This value:', widget=forms.TextInput(attrs={'placeholder': 'Number (nM)','type': 'number','min':'0','step': '1'}))
	value_between_bigger = forms.CharField(required=False, label='And this value:', widget=forms.TextInput(attrs={'placeholder': 'Number (nM)','type': 'number','min':'0','step': '1'}))
	confidence_score = forms.MultipleChoiceField(choices=CONFIDENCE_SCORE, required=False, label='')
	without_metals = forms.BooleanField(required=False, label='I would like to get ligands only with the following elements: C, H, O, N, S, P, F, Cl, Br, I')
	source_db = forms.ChoiceField(choices=[('everything', 'All data'), ('chembdb', 'Intersection of both databases'),('chembl', 'Chembl'),('bdb', 'BindingDB')], label='Source database(s)', required=False)

class DownloadForm(forms.Form):
	list_of_all = forms.CharField()
	ligand = forms.CharField(required=False)
