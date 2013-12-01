#!/usr/bin/python3.2
# -*- coding: UTF-8 -*-

import requests
import json

class Broadcast:

    channel_id  = 0
    title       = '#TITLE#'
    description = '#DESCRIPTION#'

    create_url  = 'https://alpha-api.app.net/stream/0/channels'
    message_url = 'https://alpha-api.app.net/stream/0/channels/{channel_id}/messages'
    delete_url  = 'https://alpha-api.app.net/stream/0/channels/{channel_id}'

    headers = { 'content-type': 'application/json',
                'Authorization': '#AUTH_TOKEN#'
              }

    create_payload = { 'type': 'net.app.core.broadcast',
                       'annotations': [{ 'type': 'net.app.core.broadcast.metadata',
                                         'value': {
                                                    'title': '#TITILE#',
                                                    'description': '#DESCRIPTION#'
                                                  }
                                        }],
                       'editors': {
                                    'user_ids': ['@lbenedix'],
                                    'immutable': False
                                  },
                       'readers': {
                                    'public': True,
                                    'immutable': True
                                  }
                     }

    message_payload = { 'machine_only': True,
                        'annotations': [{ 'type': 'net.app.core.broadcast.message.metadata',
                                          'value': { 'subject': '#MESSAGE#' }
                                       }]
                      }

    def __init__( self, auth_token, title, description ):
        self.title = title
        self.description = description
        self.headers['Authorization']                                 = auth_token
        self.create_payload['annotations'][0]['value']['title']       = self.title
        self.create_payload['annotations'][0]['value']['description'] = self.description

    def __str__(self):
        return 'id: {channel_id}\ntitle: {title}\ndescription: {description}'.format(
                                                                                     channel_id  = self.channel_id,
                                                                                     title       = self.title,
                                                                                     description = self.description,
                                                                                   )

    def create_channel( self ):
        r                = requests.post( self.create_url, data = json.dumps( self.create_payload ), headers=self.headers )
        # print( json.dumps( json.loads( r.text ), sort_keys=True, indent=4 ) )
        response         = json.loads( r.text )
        self.channel_id  = response['data']['id']
        self.message_url = self.message_url.format( channel_id=self.channel_id )
        self.delete_url  = self.delete_url.format( channel_id=self.channel_id)

    def delete_channel( self ):
        r = requests.delete( self.delete_url, headers=self.headers )
        # print( json.dumps( json.loads( r.text ), sort_keys=True, indent=4 ) )

    def send_message( self, message ):
        self.message_payload['annotations'][0]['value']['subject'] = message
        r = requests.post( self.message_url, data = json.dumps( self.message_payload ), headers=self.headers )
        # print( json.dumps( json.loads( r.text ), sort_keys=True, indent=4 ) )
