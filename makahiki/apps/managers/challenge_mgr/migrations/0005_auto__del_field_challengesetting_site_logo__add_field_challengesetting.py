# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'ChallengeSetting.site_logo'
        db.delete_column('challenge_mgr_challengesetting', 'site_logo')

        # Adding field 'ChallengeSetting.challenge_logo'
        db.add_column('challenge_mgr_challengesetting', 'challenge_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'ChallengeSetting.site_logo'
        db.add_column('challenge_mgr_challengesetting', 'site_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'ChallengeSetting.challenge_logo'
        db.delete_column('challenge_mgr_challengesetting', 'challenge_logo')


    models = {
        'challenge_mgr.challengesetting': {
            'Meta': {'object_name': 'ChallengeSetting'},
            'about_page_text': ('django.db.models.fields.TextField', [], {'default': '"For more information, please go to <a href=\'http://kukuicup.org\'>kukuicup.org</a>."'}),
            'cas_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###I have a CAS email'", 'max_length': '255'}),
            'cas_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'challenge_domain': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '100'}),
            'challenge_location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'challenge_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'default': "'Kukui Cup'", 'max_length': '50'}),
            'competition_team_label': ('django.db.models.fields.CharField', [], {'default': "'Team'", 'max_length': '50'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'default': "'CHANGEME@example.com'", 'max_length': '100'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_port': ('django.db.models.fields.IntegerField', [], {'default': '587'}),
            'email_use_tls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###Others'", 'max_length': '255'}),
            'landing_introduction': ('django.db.models.fields.TextField', [], {'default': "'Aloha! Welcome to the Kukui Cup.'", 'max_length': '500'}),
            'landing_non_participant_text': ('django.db.models.fields.TextField', [], {'default': "'###I am not registered.'", 'max_length': '255'}),
            'landing_participant_text': ('django.db.models.fields.TextField', [], {'default': "'###I am registered'", 'max_length': '255'}),
            'landing_slogan': ('django.db.models.fields.TextField', [], {'default': "'The Kukui Cup: Lights off, game on!'", 'max_length': '255'}),
            'ldap_auth_text': ('django.db.models.fields.TextField', [], {'default': "'###I have a LDAP email'", 'max_length': '255'}),
            'ldap_search_base': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ldap_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'theme-forest'", 'max_length': '50'}),
            'use_cas_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_internal_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_ldap_auth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wattdepot_server_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'challenge_mgr.gameinfo': {
            'Meta': {'ordering': "['priority']", 'object_name': 'GameInfo'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'challenge_mgr.gamesetting': {
            'Meta': {'ordering': "['game', 'widget']", 'unique_together': "(('game', 'widget'),)", 'object_name': 'GameSetting'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.GameInfo']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'challenge_mgr.pageinfo': {
            'Meta': {'ordering': "['priority']", 'object_name': 'PageInfo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'unlock_condition': ('django.db.models.fields.CharField', [], {'default': "'True'", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "'/'", 'max_length': '255'})
        },
        'challenge_mgr.pagesetting': {
            'Meta': {'ordering': "['page', 'game', 'widget']", 'unique_together': "(('page', 'game', 'widget'),)", 'object_name': 'PageSetting'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.GameInfo']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.PageInfo']"}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'challenge_mgr.roundsetting': {
            'Meta': {'ordering': "['start']", 'object_name': 'RoundSetting'},
            'display_scoreboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 29, 8, 13, 12, 700611)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Round 1'", 'max_length': '50'}),
            'round_reset': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 22, 8, 13, 12, 700566)'})
        },
        'challenge_mgr.sponsor': {
            'Meta': {'ordering': "['priority', 'name']", 'object_name': 'Sponsor'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge_mgr.ChallengeSetting']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': "'1'"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'challenge_mgr.uploadimage': {
            'Meta': {'object_name': 'UploadImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['challenge_mgr']
