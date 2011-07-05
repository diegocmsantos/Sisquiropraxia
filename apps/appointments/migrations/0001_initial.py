# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MedicalAppointment'
        db.create_table('appointments_medicalappointment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('appointment_date', self.gf('django.db.models.fields.DateField')()),
            ('diagnostic', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('section_times', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('appointment_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('appointments', ['MedicalAppointment'])

        # Adding M2M table for field payment_way on 'MedicalAppointment'
        db.create_table('appointments_medicalappointment_payment_way', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medicalappointment', models.ForeignKey(orm['appointments.medicalappointment'], null=False)),
            ('paymentway', models.ForeignKey(orm['payments.paymentway'], null=False))
        ))
        db.create_unique('appointments_medicalappointment_payment_way', ['medicalappointment_id', 'paymentway_id'])

        # Adding model 'Section'
        db.create_table('appointments_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medicalAppointment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['appointments.MedicalAppointment'])),
            ('section_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('section_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('appointments', ['Section'])


    def backwards(self, orm):
        
        # Deleting model 'MedicalAppointment'
        db.delete_table('appointments_medicalappointment')

        # Removing M2M table for field payment_way on 'MedicalAppointment'
        db.delete_table('appointments_medicalappointment_payment_way')

        # Deleting model 'Section'
        db.delete_table('appointments_section')


    models = {
        'appointments.medicalappointment': {
            'Meta': {'object_name': 'MedicalAppointment'},
            'appointment_date': ('django.db.models.fields.DateField', [], {}),
            'appointment_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'diagnostic': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_way': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'Forma de pagamento'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['payments.PaymentWay']"}),
            'section_times': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['appointments']
