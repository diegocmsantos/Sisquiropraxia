# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Clinic'
        db.create_table('profiles_clinic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cnpj', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Address'])),
        ))
        db.send_create_signal('profiles', ['Clinic'])

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

        # Adding model 'Employees'
        db.create_table('profiles_employees', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Address'], null=True, blank=True)),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.BillingAccount'], null=True, blank=True)),
            ('clinic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Clinic'])),
        ))
        db.send_create_signal('profiles', ['Employees'])

        # Adding model 'Doctor'
        db.create_table('profiles_doctor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Address'], null=True, blank=True)),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.BillingAccount'], null=True, blank=True)),
            ('crm', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Table'])),
        ))
        db.send_create_signal('profiles', ['Doctor'])

        # Adding M2M table for field clients on 'Doctor'
        db.create_table('profiles_doctor_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm['profiles.doctor'], null=False)),
            ('client', models.ForeignKey(orm['profiles.client'], null=False))
        ))
        db.create_unique('profiles_doctor_clients', ['doctor_id', 'client_id'])

        # Adding model 'Client'
        db.create_table('profiles_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Address'], null=True, blank=True)),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.BillingAccount'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Client'])

        # Adding M2M table for field medical_appointment on 'Client'
        db.create_table('profiles_client_medical_appointment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['profiles.client'], null=False)),
            ('medicalappointment', models.ForeignKey(orm['appointments.medicalappointment'], null=False))
        ))
        db.create_unique('profiles_client_medical_appointment', ['client_id', 'medicalappointment_id'])

        # Adding M2M table for field clients on 'Client'
        db.create_table('profiles_client_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_client', models.ForeignKey(orm['profiles.client'], null=False)),
            ('to_client', models.ForeignKey(orm['profiles.client'], null=False))
        ))
        db.create_unique('profiles_client_clients', ['from_client_id', 'to_client_id'])

        # Adding model 'Hostess'
        db.create_table('profiles_hostess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('profiles', ['Hostess'])

        # Adding model 'Address'
        db.create_table('profiles_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('profiles', ['Address'])

        # Adding model 'BillingAccount'
        db.create_table('profiles_billingaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Banco', null=True, to=orm['profiles.Bank'])),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['BillingAccount'])

        # Adding model 'Bank'
        db.create_table('profiles_bank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_code', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('profiles', ['Bank'])

        # Adding model 'Phone'
        db.create_table('profiles_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phone_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=14)),
        ))
        db.send_create_signal('profiles', ['Phone'])

        # Adding model 'UserProfile'
        db.create_table('profiles_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('profiles', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'Clinic'
        db.delete_table('profiles_clinic')

        # Deleting model 'CompanyAdmin'
        db.delete_table('profiles_companyadmin')

        # Removing M2M table for field clinics on 'CompanyAdmin'
        db.delete_table('profiles_companyadmin_clinics')

        # Deleting model 'Employees'
        db.delete_table('profiles_employees')

        # Deleting model 'Doctor'
        db.delete_table('profiles_doctor')

        # Removing M2M table for field clients on 'Doctor'
        db.delete_table('profiles_doctor_clients')

        # Deleting model 'Client'
        db.delete_table('profiles_client')

        # Removing M2M table for field medical_appointment on 'Client'
        db.delete_table('profiles_client_medical_appointment')

        # Removing M2M table for field clients on 'Client'
        db.delete_table('profiles_client_clients')

        # Deleting model 'Hostess'
        db.delete_table('profiles_hostess')

        # Deleting model 'Address'
        db.delete_table('profiles_address')

        # Deleting model 'BillingAccount'
        db.delete_table('profiles_billingaccount')

        # Deleting model 'Bank'
        db.delete_table('profiles_bank')

        # Deleting model 'Phone'
        db.delete_table('profiles_phone')

        # Deleting model 'UserProfile'
        db.delete_table('profiles_userprofile')


    models = {
        'appointments.medicalappointment': {
            'Meta': {'object_name': 'MedicalAppointment'},
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'diagnostic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_way': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Forma de pagamento'", 'to': "orm['payments.PaymentWay']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['service.Service']", 'symmetrical': 'False'})
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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['profiles']
