# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    source = models.ForeignKey('Source', models.DO_NOTHING)
    receptor = models.ForeignKey('Receptor', models.DO_NOTHING)
    ligand = models.ForeignKey('Ligand', models.DO_NOTHING)
    type = models.TextField(blank=True, null=True)
    relation = models.CharField(max_length=10, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    p_chembl = models.FloatField(blank=True, null=True)
    confidence_score = models.IntegerField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    temperature = models.TextField(blank=True, null=True)
    source_db = models.TextField()

    class Meta:
        managed = False
        db_table = 'activity'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Ligand(models.Model):
    ligand_id = models.IntegerField(primary_key=True)
    inchi = models.TextField()
    inchi_key = models.TextField()
    inchi_bdb = models.TextField(blank=True, null=True)
    inchi_chembl = models.TextField(blank=True, null=True)
    smiles = models.TextField(blank=True, null=True)
    no_metal = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ligand'


class Receptor(models.Model):
    receptor_id = models.IntegerField(primary_key=True)
    uniprot_id = models.TextField()
    uniprot_name = models.TextField()
    uniprot_short_name = models.TextField()
    trivial_names = models.TextField(blank=True, null=True)
    full_names = models.TextField(blank=True, null=True)
    short_nr = models.TextField(blank=True, null=True)
    chembl_number = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receptor'


class Source(models.Model):
    source_id = models.IntegerField(primary_key=True)
    article_doi = models.TextField()
    pmid = models.IntegerField(blank=True, null=True)
    pubchem_id = models.TextField(blank=True, null=True)
    patent_number = models.TextField(blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    institution = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'

def __str__(self):
	return self.title
