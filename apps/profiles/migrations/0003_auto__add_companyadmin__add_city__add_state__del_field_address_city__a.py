# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CompanyAdmin'
        db.create_table('profiles_companyadmin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Address'], null=True, blank=True)),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.BillingAccount'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['CompanyAdmin'])

        # Adding M2M table for field clinics on 'CompanyAdmin'
        db.create_table('profiles_companyadmin_clinics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('companyadmin', models.ForeignKey(orm['profiles.companyadmin'], null=False)),
            ('clinic', models.ForeignKey(orm['profiles.clinic'], null=False))
        ))
        db.create_unique('profiles_companyadmin_clinics', ['companyadmin_id', 'clinic_id'])

        # Adding model 'City'
        db.create_table('profiles_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.State'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('profiles', ['City'])

        # Adding model 'State'
        db.create_table('profiles_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('uf', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('profiles', ['State'])

        # Deleting field 'Address.city'
        db.delete_column('profiles_address', 'city')

        # Adding field 'Address.zip'
        db.add_column('profiles_address', 'zip', self.gf('django.db.models.fields.CharField')(default=None, max_length=10), keep_default=False)

        # Adding field 'Address.state'
        db.add_column('profiles_address', 'state', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['profiles.State']), keep_default=False)

        # Adding field 'Clinic.cnpj'
        db.add_column('profiles_clinic', 'cnpj', self.gf('django.db.models.fields.CharField')(default=None, max_length=14), keep_default=False)

        # Changing field 'Clinic.owner'
        db.alter_column('profiles_clinic', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.CompanyAdmin']))


    def backwards(self, orm):
        
        # Deleting model 'CompanyAdmin'
        db.delete_table('profiles_companyadmin')

        # Removing M2M table for field clinics on 'CompanyAdmin'
        db.delete_table('profiles_companyadmin_clinics')

        # Deleting model 'City'
        db.delete_table('profiles_city')

        # Deleting model 'State'
        db.delete_table('profiles_state')

        # Adding field 'Address.city'
        db.add_column('profiles_address', 'city', self.gf('django.db.models.fields.CharField')(default=None, max_length=100), keep_default=False)

        # Deleting field 'Address.zip'
        db.delete_column('profiles_address', 'zip')

        # Deleting field 'Address.state'
        db.delete_column('profiles_address', 'state_id')

        # Deleting field 'Clinic.cnpj'
        db.delete_column('profiles_clinic', 'cnpj')

        # Changing field 'Clinic.owner'
        db.alter_column('profiles_clinic', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))


    models = {
        'appointments.medicalappointment': {
            'Meta': {'object_name': 'MedicalAppointment'},
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'diagnostic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_way': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'Forma de pagamento'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['payments.PaymentWay']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.TableService']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'payments.paymentway': {
            'Meta': {'object_name': 'PaymentWay'},
            'card_payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'check_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'check_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quant_parcels': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_payment': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'profiles.address': {
            'Meta': {'ordering': "('street',)", 'object_name': 'Address'},
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.State']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'profiles.bank': {
            'Meta': {'object_name': 'Bank'},
            'bank_code': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Banco'", 'null': 'True', 'to': "orm['profiles.Bank']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'profiles.city': {
            'Meta': {'object_name': 'City'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.State']"})
        },
        'profiles.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Address']", 'null': 'True', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'clients_rel_+'", 'to': "orm['profiles.Client']"}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medical_appointment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['appointments.MedicalAppointment']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.clinic': {
            'Meta': {'object_name': 'Clinic'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Address']"}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.CompanyAdmin']"})
        },
        'profiles.companyadmin': {
            'Meta': {'object_name': 'CompanyAdmin'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Address']", 'null': 'True', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'clinics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.Clinic']", 'symmetrical': 'False'}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Address']", 'null': 'True', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.Client']", 'symmetrical': 'False'}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'crm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Table']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.employees': {
            'Meta': {'object_name': 'Employees'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Address']", 'null': 'True', 'blank': 'True'}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Clinic']"}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.hostess': {
            'Meta': {'object_name': 'Hostess'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.phone': {
            'Meta': {'object_name': 'Phone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.state': {
            'Meta': {'object_name': 'State'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'profiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'service.service': {
            'Meta': {'object_name': 'Service'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'service.table': {
            'Meta': {'object_name': 'Table'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'service.tableservice': {
            'Meta': {'object_name': 'TableService'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Service']"}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Table']"})
        }
    }

    complete_apps = ['profiles']
