# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentWay'
        db.create_table('payments_paymentway', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_payment', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('quant_parcels', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('check_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('check_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('card_payment_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('payments', ['PaymentWay'])


    def backwards(self, orm):
        
        # Deleting model 'PaymentWay'
        db.delete_table('payments_paymentway')


    models = {
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

    complete_apps = ['payments']
