# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'MedicalAppointment.appointment_type'
        db.delete_column('appointments_medicalappointment', 'appointment_type')

        # Deleting field 'MedicalAppointment.section_times'
        db.delete_column('appointments_medicalappointment', 'section_times')

        # Adding field 'MedicalAppointment.quantity'
        db.add_column('appointments_medicalappointment', 'quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'MedicalAppointment.service'
        db.add_column('appointments_medicalappointment', 'service', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['service.TableService']), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'MedicalAppointment.appointment_type'
        db.add_column('appointments_medicalappointment', 'appointment_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=1), keep_default=False)

        # Adding field 'MedicalAppointment.section_times'
        db.add_column('appointments_medicalappointment', 'section_times', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Deleting field 'MedicalAppointment.quantity'
        db.delete_column('appointments_medicalappointment', 'quantity')

        # Deleting field 'MedicalAppointment.service'
        db.delete_column('appointments_medicalappointment', 'service_id')


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
        'appointments.section': {
            'Meta': {'ordering': "('-section_date',)", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicalAppointment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['appointments.MedicalAppointment']"}),
            'section_date': ('django.db.models.fields.DateTimeField', [], {}),
            'section_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['appointments']
