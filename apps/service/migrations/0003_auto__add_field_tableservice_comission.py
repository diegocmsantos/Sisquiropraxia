# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'TableService.comission'
        db.add_column('service_tableservice', 'comission', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=4, decimal_places=2), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'TableService.comission'
        db.delete_column('service_tableservice', 'comission')


    models = {
        'service.service': {
            'Meta': {'object_name': 'Service'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'comission': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Service']"}),
            'table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['service.Table']"})
        }
    }

    complete_apps = ['service']
