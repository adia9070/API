from datetime import datetime
from curd_api_package import api
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse, inputs
from curd_api_package.model import FetchDataFromDb, CreateDataInDb, UpdateDataInDb, DeleteFromDb

#Validate the song JSON data
class SongValidation(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True, validate=Length(min=1, max=100))
    duration = fields.Int(required=True, validate=Range(min=1))
    uploaded_time = fields.DateTime(required=True)
    
    @validates('uploaded_time')
    def is_not_in_future(self, value):
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create notes in the future!")


#Validate the podcast JSON data
class PodcastValidation(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True, validate=Length(min=1, max=100))
    duration = fields.Int(required=True, validate=Range(min=1))
    uploaded_time = fields.DateTime(required=True)
    host = fields.Str(required=True, validate=Length(min=1, max=100))
    participants = fields.List(fields.Str(validate=Length(min=1, max=100)), required=False, validate=Length(min=0, max=100))
    
    @validates('uploaded_time')
    def is_not_in_future(self, value):
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create notes in the future!")

#Validate the audiobook JSON data
class AudioBookValidation(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True, validate=Length(min=1, max=100))
    author = fields.Str(required=True, validate=Length(min=1, max=100))
    narrator = fields.Str(required=True, validate=Length(min=1, max=100))
    duration = fields.Int(required=True, validate=Range(min=1))
    uploaded_time = fields.DateTime(required=True)
   
    @validates('uploaded_time')
    def is_not_in_future(self, value):
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create notes in the future!")

#CREATE Data
class Create(Resource):
    def post(self, audioFileType):
        audioFileMetadata = request.get_json()
        if audioFileMetadata == None:
            return make_response({'msg':'no Data'}, 400)
        if audioFileType.lower().strip() == 'song':
            ERROR = SongValidation().validate(audioFileMetadata)
            if len(audioFileMetadata.keys()) == 4 and not(ERROR):
                response = CreateDataInDb().CREATE('song', audioFileMetadata)
                return response
            else:
               return make_response({'msg':'Seems you are having wrong data'}, 400)
        elif audioFileType.lower().strip() == 'podcast':
            ERROR = PodcastValidation().validate(audioFileMetadata)
            if len(audioFileMetadata.keys()) in [5, 6] and not(ERROR):
                response = CreateDataInDb().CREATE('podcast', audioFileMetadata)
                return response
            else:
               return make_response({'msg':'Seems you are having  wrong data'}, 400)    
        elif audioFileType.lower().strip() == 'audiobook':
            ERROR = AudioBookValidation().validate(audioFileMetadata)
            if len(audioFileMetadata.keys()) == 6 and not(ERROR):
                response = CreateDataInDb().CREATE('audiobook', audioFileMetadata)
                return response
            else:
                return make_response({'msg':'Seems you are having  wrong data'}, 400)
        else:
            return make_response({'msg':'Currently We Support Song/Podcast/Audiobook Only'}, 400)         

#UPDATE Data
class Update(Resource):
    def put(self, audioFileType, audioFileID):
        audioFileMetadata = request.get_json()
        if audioFileMetadata == None:
            return make_response({'msg':'no Data'}, 400)
        if audioFileType.lower().strip() == 'song':
            ERROR = SongValidation().validate(audioFileMetadata)
            if audioFileID == audioFileMetadata['id'] and not(ERROR) and len(audioFileMetadata) == 4:
                response = UpdateDataInDb().UPDATE(audioFileType, audioFileID, audioFileMetadata)
                return response
            else:
                return make_response({'message':'Seems you are having  wrong data'}, 400)
        elif audioFileType.lower().strip() == 'podcast':
            ERROR = PodcastValidation().validate(audioFileMetadata)
            if audioFileID == audioFileMetadata['id'] and not(ERROR) and len(audioFileMetadata) in [5, 6]:
                response = UpdateDataInDb().UPDATE(audioFileType, audioFileID, audioFileMetadata)
                return response
            else:
                return make_response({'message':'Seems you are having  wrong data'}, 400)            
        elif audioFileType.lower().strip() == 'audiobook':
            ERROR = AudioBookValidation().validate(audioFileMetadata)
            if audioFileID == audioFileMetadata['id'] and not(ERROR) and len(audioFileMetadata) == 6:
                response = UpdateDataInDb().UPDATE(audioFileType, audioFileID, audioFileMetadata)
                return response
            else:
                return make_response({'message':'Seems you are having  wrong data'}, 400)
        else:
            return make_response({'msg':'Currently We Support Song/Podcast/Audiobook Only'}, 400)



class Delete(Resource):
    def delete(self, audioFileType, audioFileID):
        if audioFileType.lower().strip() in ['song', 'podcast', 'audiobook']:
            response = DeleteFromDb().DELETE(audioFileType, audioFileID)
            return response
        else:
            return make_response({'msg':'Currently We Support Song/Podcast/Audiobook Only'}, 400)

#GET Single Data 
class GetSingle(Resource):
    def get(self, audioFileType, audioFileID):
        if audioFileType.lower().strip() in ['song', 'podcast', 'audiobook']:
            response = FetchDataFromDb().GET(audioFileType, audioFileID)
            return response
        else:
            return make_response({'msg':'Currently We Support Song/Podcast/Audiobook Only'}, 400)

#GET All Data 
class GetAll(Resource):
    def get(self, audioFileType):
        if audioFileType.lower().strip() in ['song', 'podcast', 'audiobook']:
            response = FetchDataFromDb().GET(audioFileType)
            return response
        else:
            return make_response({'msg':'Currently We Support Song/Podcast/Audiobook Only'}, 400) 

api.add_resource(Create, '/create/<string:audioFileType>')
api.add_resource(Update, '/update/<string:audioFileType>/<int:audioFileID>')
api.add_resource(Delete, '/delete/<string:audioFileType>/<int:audioFileID>')
api.add_resource(GetSingle, '/get/<string:audioFileType>/<int:audioFileID>')
api.add_resource(GetAll, '/get/<string:audioFileType>')

