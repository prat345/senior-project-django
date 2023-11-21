import pymongo
from pymongo import MongoClient
import pandas as pd
import os

connect = 'mongodb+srv://kopkap:kopkap123@cluster0.agjmc4n.mongodb.net/?retryWrites=true&w=majority' # Atlas
# connect = 'mongodb://localhost:27017' # Compass 
cluster = MongoClient(connect)
db = cluster["Testdrive"]
db2 = cluster["Information"]
db3 = cluster['video']

incident_col = db2['Incident']
vid_col = db3['incidents']
info_col = db2['Testdrive_info']

def get_collection_names():
    collections = db.list_collection_names()
    return collections

def get_data(testdrive):
    collection = db[testdrive]
    df = collection.find()
    df = pd.DataFrame(df, dtype = 'float64')
    try:
        df.drop(columns = ['_id','Unnamed: 0'], inplace=True)
    except Exception as e:
        print(e)
    position = df.columns.get_loc('Time')
    starttime = df.iat[0, position]
    df['elasped_sec'] = (df.iloc[1:, position] - starttime)
    df['elasped_sec'].fillna(0.000,inplace = True)
    df['elasped_time'] = pd.to_datetime(df['elasped_sec'],unit = 's')
    df.iloc[:,1:] = df.iloc[:,1:].round(3)
    df['elasped_time'] = df['elasped_time'].apply(lambda dt: dt.strftime('%M:%S'))
    df['msg.mode'] = df['msg.mode'].map({'True': 'auto', 'False': 'manual'})
    df['msg.brake'] = df['msg.brake']/250*100
    return df

def get_incident():
    incident_dict = incident_col.find_one()
    return incident_dict

def get_stations():
    print(os.path.abspath(os.curdir))
    # os.chdir('..')
    # print(os.path.abspath(os.curdir))
    station_wp = pd.read_csv('static/csv/station.csv', index_col=['location','vehicle','index'], skipinitialspace=True)
    return station_wp

def get_video(labels=[],operation='AND'):
    key = 'tags'
    if 'all' in labels:
        query = vid_col.find({}) # default show all vids
    else:
        if operation == 'OR':
            query = vid_col.find({key:{"$in":labels}})
        else:
            query = vid_col.find({key:{"$all":labels}})
    # for dic in query:
    #     print(type(dic['tags']), ', '.join(list(dic['tags'])))
    #     dic['tags'] = ', '.join(list(dic['tags']))
    query = list(query)
    # print(query)
    return query

def get_all_video(query={}):
    query = vid_col.find(query)
    query = list(query)
    for dic in query:
        dic['tags'] = ', '.join(list(dic['tags']))
    return query

def update_label(stamp, newLabel):
    if newLabel == "" or len(newLabel) == 0:
        newLabel = None 
    query = {'stamp':stamp}
    print('Before: ',vid_col.find_one({'stamp': stamp}))
    vid_col.update_one(query, {'$set':{'tags':newLabel}})
    print('After: ',vid_col.find_one({'stamp': stamp}))

def delete_incident(stamp):
    print('Before: ',vid_col.find_one({'stamp': stamp}))
    query = {'stamp':stamp}
    vid_col.delete_one(query)
    print('After: ',vid_col.find_one({'stamp': stamp}))

def get_information():
    info = info_col.find()
    info = pd.DataFrame(info, dtype = 'float64') 
    # info.drop(columns = ['_id','Unnamed: 0'],inplace=True)
    # info['datetime'] = info['datetime'].astype('datetime64[ns]')
    info_sort = info.sort_values(by=['datetime'])
    return info_sort

def get_testdrive_info(testdrive):
    info = info_col.find()
    info = pd.DataFrame(info, dtype = 'float64').set_index('name')
    # info.drop(columns = ['_id','Unnamed: 0'],inplace=True)
    # print(info)
    dic = {}
    dic['Location'] = info.loc[testdrive]['location']
    dic['Date'] = info.loc[testdrive]['date']
    dic['Time'] = info.loc[testdrive]['time']
    dic['Duration'] = info.loc[testdrive]['duration']
    dic['Distance(m)'] = str(int(info.loc[testdrive]['mileages']))
    dic['Auto%'] = str(info.loc[testdrive]['p_auto'])
    # print(dic)
    return dic

if __name__ == '__main__':
    # db,collections = get_data()
    # incident_d = get_incident()
    # station_wp = get_stations()
    # print(collections)
    # print(incident_d)
    # print(station_wp)
    # collection = db['T2-B_SL_NBTC_20230125202407']
    # df = collection.find()
    # df = pd.DataFrame(df, dtype = 'float64')
    # # df.drop(columns = ['_id','Unnamed: 0'], inplace=True)
    # # print(df.head())

    # update_label('1', ['hello', 'bus','hi'])
    # query = get_all_video()
    # # print(query)
    # for dic in query:
    #     dic['tags'] = list(dic['tags'])
    #     if dic['tags'] != []:
    #         print(dic['tags'][0])
    testdrive = 'T2B_BS_Chula_20230206151254'
    get_testdrive_info(testdrive)