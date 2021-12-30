import logging
import azure.functions as func

from getSongLyric import getLyric
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        lyric, cover, title, artists = getLyric._musixmatch(name)

        if lyric is not None:
            return func.HttpResponse(
                json.dumps({
                    'success': True,
                    'message': 'Success',
                    'data': {
                        'name': title,
                        'artists': artists,
                        'cover': cover,
                        'lyric': lyric
                    }
                }),
                mimetype="application/json",
            )
        else:
            return func.HttpResponse(
                json.dumps({
                    'success': False,
                    'message': 'Song not found',
                }),
                mimetype="application/json",
            )
    else:
        return func.HttpResponse(
            json.dumps({
                'success': False,
                'message': 'Name is require'
            }),
            mimetype="application/json",
        )
