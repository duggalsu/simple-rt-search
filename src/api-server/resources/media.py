from flask_restful import Resource, reqparse
import werkzeug
import json
from flask import jsonify, request
from send import add_job_to_queue

class Media(Resource):
    def __init__(self):
        self.post_request_parser = reqparse.RequestParser()
        self.post_request_parser.add_argument('file_url', type=str, help='file url is a mandatory field', required=True)
        self.post_request_parser.add_argument('media_type', type=str, choices=('video', 'audio', 'image'), help='The file type of media item. Acceptable values : video, image, audio', required=True)
        self.post_request_parser.add_argument('metadata', type=dict, help='Any metadata that you want to store in the search index. Use Judiciously')

    # TODO add validation for supported mimetypes : image/jpeg, image/png, audio/mpeg, audio/wav, video/mpeg
    def post(self):
        try:
            args = self.post_request_parser.parse_args(strict=True)
            print('POST /media file_url : ', args['file_url'])
            add_job_to_queue(args)
            return 'media enqueued', 200
        
        except Exception as e:
            print('error in finding indexing media : ', e)
            return 'Error indexing media : '+str(e), 500
        
        