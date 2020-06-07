from django.contrib import admin
from .models import Activity, Ligand, Receptor, Source


class ActivityAdmin(admin.ModelAdmin):
	list_display = ('activity_id', 'ligand_id', 'receptor_id', 'source_id',)
	search_fields = ('activity_id', 'ligand_id', 'receptor_id', 'source_id',)

class LigandAdmin(admin.ModelAdmin):
	list_display = ('ligand_id', 'inchi', 'no_metal',)
	list_filter = ('no_metal',)
	search_fields = ('ligand_id', 'inchi', 'no_metal',)

class ReceptorAdmin(admin.ModelAdmin):
	list_display = ('receptor_id', 'uniprot_id', 'uniprot_name',)
	search_fields = ('receptor_id', 'uniprot_id', 'uniprot_name',)

class SourceAdmin(admin.ModelAdmin):
	list_display = ('source_id', 'article_doi',)
	search_fields = ('source_id', 'article_doi',)

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Ligand, LigandAdmin)
admin.site.register(Receptor, ReceptorAdmin)
admin.site.register(Source, SourceAdmin)


