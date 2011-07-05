# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TableService'
        db.create_table('service_tableservice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Table'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Service'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('service', ['TableService'])

        # Deleting field 'Table.price'
        db.delete_column('service_table', 'price')

        # Deleting field 'Table.service'
        db.delete_column('service_table', 'service_id')


    def backwards(self, orm):
        
        # Deleting model 'TableService'
        db.delete_table('service_tableservice')

        # Adding field 'Table.price'
        db.add_column('service_table', 'price', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=8, decimal_places=2), keep_default=False)

        # Adding field 'Table.service'
        db.add_column('service_table', 'service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Service'], null=True, blank=True), keep_default=False)


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
