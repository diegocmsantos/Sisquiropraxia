# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Service'
        db.create_table('service_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('service', ['Service'])

        # Adding model 'Table'
        db.create_table('service_table', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('service', ['Table'])

        # Adding model 'TableService'
        db.create_table('service_tableservice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Table'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Service'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('service', ['TableService'])


    def backwards(self, orm):
        
        # Deleting model 'Service'
        db.delete_table('service_service')

        # Deleting model 'Table'
        db.delete_table('service_table')

        # Deleting model 'TableService'
        db.delete_table('service_tableservice')


    models = {
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

    complete_apps = ['service']
