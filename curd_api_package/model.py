import pandas as pd
import json
from flask import make_response, jsonify
from curd_api_package import engine, Base
from sqlalchemy import Column, Integer, String, DateTime, select
from sqlalchemy.exc import IntegrityError

class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime, nullable=False)


class Podcast(Base):
    __tablename__ = 'podcast'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime, nullable=False)
    host = Column(String(100), nullable=False)
    participant1 = Column(String(100), nullable=True)
    participant2 = Column(String(100), nullable=True)
    participant3 = Column(String(100), nullable=True)
    participant4 = Column(String(100), nullable=True)
    participant5 = Column(String(100), nullable=True)
    participant6 = Column(String(100), nullable=True)
    participant7 = Column(String(100), nullable=True)
    participant8 = Column(String(100), nullable=True)
    participant9 = Column(String(100), nullable=True)
    participant10 = Column(String(100), nullable=True)


class AudioBook(Base):
    __tablename__ = 'audiobook'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    narrator = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    uploaded_time = Column(DateTime, nullable=False)


class FetchDataFromDb():
    def __init__(self):
        self.connection = engine.connect()

    def GET(self, audioFileType, audioFileID=None):
        try:
            if audioFileID is None:
                result = self.connection.execute(f"SELECT * FROM {audioFileType}").fetchall()
            else:
                result = self.connection.execute(f"SELECT * FROM {audioFileType} WHERE ID = {audioFileID}").fetchall()
            if len(result) > 0:
                df = pd.DataFrame(result)
                df.columns = result[0].keys()
                json_response = df.to_json(orient='records')
                return make_response(json_response, 200)
            else:
                return make_response({}, 204)
        except Exception as e:
            return make_response({'message': str(e)}, 500)

    def __del__(self):
        self.connection.close()


class CreateDataInDb():
    def CREATE(self, audioFileType, audioFileMetadata):
        try:
            if audioFileType != 'podcast':
                df = pd.read_json(json.dumps([audioFileMetadata]), orient='records')
                df.to_sql(audioFileType, con=engine, index=False, if_exists='append')
                return make_response({'msg':'Created'}, 200)
            else:
                df = pd.read_json(json.dumps([audioFileMetadata]), orient='records')
                if audioFileMetadata.get('participants'):
                    for index, participant in enumerate(audioFileMetadata['participants']):
                        df['participant'+str(index+1)] = participant
                    df.drop(['participants'], axis=1, inplace=True)
                df.to_sql(audioFileType, con=engine, index=False, if_exists='append')
                return make_response({'msg':'Created'}, 200)
        except IntegrityError:
                return make_response({'message':'Key Already Exists'}, 400)
        except Exception as e:
            return make_response({'message': str(e)}, 500)


class UpdateDataInDb():
    def __init__(self):
        self.connection = engine.connect()

    def UPDATE(self, audioFileType, audioFileID, audioFileMetadata):
        try:
            if audioFileType.lower().strip() == 'song':
                query = f'''
                UPDATE SONG
                SET 
                name='{audioFileMetadata['name']}',
                duration={audioFileMetadata['duration']}, 
                uploaded_time='{audioFileMetadata['uploaded_time']}' 
                WHERE ID={audioFileMetadata['id']}
                '''
                self.connection.execute(query)
                return make_response({'msg':'Updated'}, 200)
            elif audioFileType.lower().strip() == 'podcast':
                queryP1 = f'''
                UPDATE PODCAST
                SET 
                name='{audioFileMetadata['name']}',
                duration={audioFileMetadata['duration']}, 
                uploaded_time='{audioFileMetadata['uploaded_time']}',
                host='{audioFileMetadata['host']}'
                ''' 
                if audioFileMetadata.get('participants'):
                    queryP2 = ''
                    for index, i in enumerate(audioFileMetadata['participants']):
                        if index == 0:
                            queryP2 = queryP2 + ", participant"+str(index+1)+f"='{i}', "
                        if (index+1) == len(audioFileMetadata['participants']):
                            queryP2 = queryP2 + "participant"+str(index+1)+f"='{i}'"
                        else:
                            queryP2 = queryP2 + "participant"+str(index+1)+f"='{i}', "
                queryP3 = f'''
                WHERE ID={audioFileMetadata['id']}
                '''
                if audioFileMetadata.get('participants'):
                    query = queryP1 + queryP2 + queryP3
                else:
                    query = queryP1 + queryP3
                self.connection.execute(query)
                return make_response({'msg':'Updated'}, 200)
            elif audioFileType.lower().strip() == 'audiobook':
                query = f'''
                UPDATE PODCAST
                SET 
                title='{audioFileMetadata['title']}',
                author='{audioFileMetadata['author']}',
                narrator='{audioFileMetadata['narrator']}',
                duration={audioFileMetadata['duration']}, 
                uploaded_time='{audioFileMetadata['uploaded_time']}'
                WHERE ID={audioFileMetadata['id']}
                '''
                self.connection.execute(query)
                return make_response({'msg':'Updated'}, 200)
            else:
                return make_response({}, 400)
        except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 500)
    
    def __del__(self):
        self.connection.close()


class DeleteFromDb():
    def __init__(self):
        self.connection = engine.connect()

    def DELETE(self, audioFileType, audioFileID):
        try:
            self.connection.execute(f"DELETE FROM {audioFileType} WHERE ID = {audioFileID}")
            return make_response({'msg':'Deleted'}, 200)
        except Exception as e:
            return make_response({'message':str(e)}, 500)   

    def __del__(self):
        self.connection.close()