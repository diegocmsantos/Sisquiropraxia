# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Section'
        db.delete_table('appointments_section')

        # Adding field 'MedicalAppointment.services'
        db.add_column('appointments_medicalappointment', 'services', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['service.Service']), keep_default=False)

        # Adding field 'MedicalAppointment.appointment_done'
        db.add_column('appointments_medicalappointment', 'appointment_done', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Removing M2M table for field services on 'MedicalAppointment'
        db.delete_table('appointments_medicalappointment_services')

        # Changing field 'MedicalAppointment.appointment_date'
        db.alter_column('appointments_medicalappointment', 'appointment_date', self.gf('django.db.models.fields.DateTimeField')())


    def backwards(self, orm):
        
        # Adding model 'Section'
        db.create_table('appointments_section', (
            ('section_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('section_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medicalAppointment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appointments.MedicalAppointment'])),
        ))
        db.send_create_signal('appointments', ['Section'])

        # Deleting field 'MedicalAppointment.services'
        db.delete_column('appointments_medicalappointment', 'services_id')

        # Deleting field 'MedicalAppointment.appointment_done'
        db.delete_column('appointments_medicalappointment', 'appointment_done')

        # Adding M2M table for field services on 'MedicalAppointment'
        db.create_table('appointments_medicalappointment_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medicalappointment', models.ForeignKey(orm['appointments.medicalappointment'], null=False)),
            ('service', models.ForeignKey(orm['service.service'], null=False))
        ))
        db.create_unique('appointments_medicalappointment_services', ['medicalappointment_id', 'service_id'])

        # Changing field 'MedicalAppointment.appointment_date'
        db.alter_column('appointments_medicalappointment', 'appointment_date', self.gf('django.db.models.fields.DateField')())


    models = {
        'appointments.medicalappointment': {
            'Meta': {'object_name': 'MedicalAppointment'},
            'appointment_date': ('django.db.models.fields.DateTimeField', [], {}),
            'appointment_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'diagnostic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_way': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Forma de pagamento'", 'to': "orm['payments.PaymentWay']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'services': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Service']"})
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
        'service.service': {
            'Meta': {'object_name': 'Service'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['appointments']
