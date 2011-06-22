# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Doctor'
        db.create_table('crm_doctor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Address'])),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.BillingAccount'], null=True, blank=True)),
            ('crm', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('crm', ['Doctor'])

        # Adding M2M table for field clients on 'Doctor'
        db.create_table('crm_doctor_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('doctor', models.ForeignKey(orm['crm.doctor'], null=False)),
            ('client', models.ForeignKey(orm['crm.client'], null=False))
        ))
        db.create_unique('crm_doctor_clients', ['doctor_id', 'client_id'])

        # Adding model 'Client'
        db.create_table('crm_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cnpf', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Address'])),
            ('billing_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.BillingAccount'], null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['Client'])

        # Adding M2M table for field medical_appointment on 'Client'
        db.create_table('crm_client_medical_appointment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['crm.client'], null=False)),
            ('medicalappointment', models.ForeignKey(orm['crm.medicalappointment'], null=False))
        ))
        db.create_unique('crm_client_medical_appointment', ['client_id', 'medicalappointment_id'])

        # Adding M2M table for field clients on 'Client'
        db.create_table('crm_client_clients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_client', models.ForeignKey(orm['crm.client'], null=False)),
            ('to_client', models.ForeignKey(orm['crm.client'], null=False))
        ))
        db.create_unique('crm_client_clients', ['from_client_id', 'to_client_id'])

        # Adding model 'Address'
        db.create_table('crm_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('crm', ['Address'])

        # Adding model 'BillingAccount'
        db.create_table('crm_billingaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('bank', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='Banco', null=True, to=orm['crm.Bank'])),
            ('account_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['BillingAccount'])

        # Adding model 'Bank'
        db.create_table('crm_bank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_code', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('crm', ['Bank'])

        # Adding model 'Phone'
        db.create_table('crm_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Client'])),
            ('phone_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=14)),
        ))
        db.send_create_signal('crm', ['Phone'])

        # Adding model 'MedicalAppointment'
        db.create_table('crm_medicalappointment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')()),
            ('diagnostic', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('section_times', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('appointment_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['MedicalAppointment'])

        # Adding M2M table for field payment_way on 'MedicalAppointment'
        db.create_table('crm_medicalappointment_payment_way', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medicalappointment', models.ForeignKey(orm['crm.medicalappointment'], null=False)),
            ('paymentway', models.ForeignKey(orm['crm.paymentway'], null=False))
        ))
        db.create_unique('crm_medicalappointment_payment_way', ['medicalappointment_id', 'paymentway_id'])

        # Adding model 'Section'
        db.create_table('crm_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medicalAppointment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.MedicalAppointment'])),
            ('section_date', self.gf('django.db.models.fields.DateField')()),
            ('section_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('crm', ['Section'])

        # Adding model 'PaymentWay'
        db.create_table('crm_paymentway', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_payment', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('quant_parcels', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('check_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('check_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('card_payment_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('crm', ['PaymentWay'])


    def backwards(self, orm):
        
        # Deleting model 'Doctor'
        db.delete_table('crm_doctor')

        # Removing M2M table for field clients on 'Doctor'
        db.delete_table('crm_doctor_clients')

        # Deleting model 'Client'
        db.delete_table('crm_client')

        # Removing M2M table for field medical_appointment on 'Client'
        db.delete_table('crm_client_medical_appointment')

        # Removing M2M table for field clients on 'Client'
        db.delete_table('crm_client_clients')

        # Deleting model 'Address'
        db.delete_table('crm_address')

        # Deleting model 'BillingAccount'
        db.delete_table('crm_billingaccount')

        # Deleting model 'Bank'
        db.delete_table('crm_bank')

        # Deleting model 'Phone'
        db.delete_table('crm_phone')

        # Deleting model 'MedicalAppointment'
        db.delete_table('crm_medicalappointment')

        # Removing M2M table for field payment_way on 'MedicalAppointment'
        db.delete_table('crm_medicalappointment_payment_way')

        # Deleting model 'Section'
        db.delete_table('crm_section')

        # Deleting model 'PaymentWay'
        db.delete_table('crm_paymentway')


    models = {
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
        'crm.address': {
            'Meta': {'ordering': "('street',)", 'object_name': 'Address'},
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'crm.bank': {
            'Meta': {'object_name': 'Bank'},
            'bank_code': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'crm.billingaccount': {
            'Meta': {'object_name': 'BillingAccount'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'account_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'bank': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Banco'", 'null': 'True', 'to': "orm['crm.Bank']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crm.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Address']"}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'clients_rel_+'", 'to': "orm['crm.Client']"}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medical_appointment': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['crm.MedicalAppointment']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'crm.doctor': {
            'Meta': {'object_name': 'Doctor'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Address']"}),
            'billing_account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.BillingAccount']", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['crm.Client']", 'symmetrical': 'False'}),
            'cnpf': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'crm': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'crm.medicalappointment': {
            'Meta': {'object_name': 'MedicalAppointment'},
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'appointment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'diagnostic': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_way': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'Forma de pagamento'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['crm.PaymentWay']"}),
            'section_times': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'crm.paymentway': {
            'Meta': {'object_name': 'PaymentWay'},
            'card_payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'check_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'check_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quant_parcels': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_payment': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'crm.phone': {
            'Meta': {'object_name': 'Phone'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'crm.section': {
            'Meta': {'ordering': "('-section_date',)", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicalAppointment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.MedicalAppointment']"}),
            'section_date': ('django.db.models.fields.DateField', [], {}),
            'section_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['crm']
