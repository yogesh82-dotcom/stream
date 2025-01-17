from flask import Flask, Response, jsonify, url_for, abort
from functools import wraps
import os

MANIFEST = {
    'id': 'org.stremio.helloworldPython',
    'version': '1.0.0',

    'name': 'Hello World Python Addon',
    'description': 'Sample addon made with Flask providing a few public domain movies',

    'types': ['movie', 'series'],

    'catalogs': [],

    'resources': [
        {'name': 'stream', 'types': [
            'movie', 'series'], 'idPrefixes': ['tt', 'hpy']}
    ]
}

STREAMS = {
    'movie': {
        'tt0032138': [
            {'title': 'Torrent',
                'infoHash': '24c8802e2624e17d46cd555f364debd949f2c81e', 'fileIdx': 0}
        ],
        'tt0017136': [
            {'title': 'Torrent',
                'infoHash': 'dca926c0328bb54d209d82dc8a2f391617b47d7a', 'fileIdx': 1}
        ],
        'tt0051744': [
            {'title': 'Torrent', 'infoHash': '9f86563ce2ed86bbfedd5d3e9f4e55aedd660960'}
        ],
        'tt1254207': [
            {'title': 'HTTP URL', 'url': 'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4'}
        ],
        'tt0031051': [
            {'title': 'YouTube', 'ytId': 'm3BKVSpP80s'}
        ],
        'tt0137523': [
            {'title': 'External URL',
                'externalUrl': 'https://www.netflix.com/watch/26004747'}
        ]
    },

    'series': {
        'tt1748166:1:1': [
            {'title': 'Torrent', 'infoHash': '07a9de9750158471c3302e4e95edb1107f980fa6'}
        ],

        'hpytt0147753:1:1': [
            {'title': 'YouTube', 'ytId': '5EQw5NYlbyE'}
        ],
        'hpytt0147753:1:2': [
            {'title': 'YouTube', 'ytId': 'ZzdBKcVzx9Y'}
        ]
    }
}

app = Flask(__name__)


def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)

@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    streams = {'streams': []}
    if type in STREAMS and id in STREAMS[type]:
        streams['streams'] = STREAMS[type][id]
    return respond_with(streams)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  
    app.run(debug=True, port=port, host='0.0.0.0')