#!/usr/bin/env python3.7
#Telethon 1.21.1

import asyncio
import aiosqlite
import os
from telethon import TelegramClient
from telethon import events
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# User Data
#  


canale = "https://t.me/"
phone    = ""
api_id   = ""
api_hash = ""
client  = TelegramClient("hello", api_id, api_hash,flood_sleep_threshold =240) 


#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# SQL query
#  

sql = """CREATE TABLE media (
        [index]    INTEGER NOT NULL
                       PRIMARY KEY AUTOINCREMENT
                       UNIQUE,
        title      TEXT,
        msgId      INTEGER UNIQUE,
        data       TEXT,
        downloaded TEXT,
        size       INT
);"""



#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# mime_type list
#

def mime_type(mime_msg):
    mime_list = [
    "video/x-matroska",            #.mkv .mk3d .mka .mks
    "video/x-msvideo",             #.avi
    "application/x-troff-msvideo", #.avi
    "video/avi",                   #.avi  
    "video/msvideo",               #.avi   
    "video/mpeg",                  #.mpg, .mpeg, .mp2, .mp3
    "video/x-mpeg",                # 
    "video/mp4",                   #.mp4, .m4a, .m4p, .m4b, .m4r .m4v
    ]
    return mime_msg in mime_list



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LOGIN
#  
async def login(phone,canale):
    
    print ("Connecting...")
    await client.connect()
    if not await client.is_user_authorized():
        print("Auth requests..")
        await client.send_code_request(phone)
        await client.sign_in(phone, int(input('Enter code: ')))
    try:
        async with client.takeout(finalize=False) as takeout: 
            return takeout    
    except errors.TakeoutInitDelayError:                
            print ("step1 > Please check service notification in a few minutes. You must answer 'yes'")
            print ("step2 > Restart script")



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Open or Create database file
#  

async def openDB(fileName):
    
    if os.path.exists (fileName):
        return await aiosqlite.connect(fileName)
    else:
        db = await aiosqlite.connect(fileName)
        cursor = await db.execute(sql)        
        await db.commit()
        return db


#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Get last message id
#  

async def last (fileName):

        db = await openDB(fileName)
        cursor = await db.execute("SELECT msgId FROM media ORDER BY msgId DESC")
        row    = await cursor.fetchone()
        if row is None:
           row = [0]
        await db.close()                                                
        return row[0]



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Download the messages and save to db
#  

async def databaseUp(id_chat,takeout,last_id,fileName):
    
    msg_list = []
    db = await openDB(fileName)    
    async for message in takeout.iter_messages(id_chat, reverse=True, filter=InputMessagesFilterDocument, min_id=last_id, wait_time=1):
        if message.media is not None:
            if mime_type(message.media.document.mime_type) is True:
                message.date = message.date.strftime('%Y-%m-%d')
                print(f"Title --> {message.file.name} {[message.date]}")                        
                msg_list.append((message.file.name,message.id,message.date,'NO',message.file.size))
    sql = "INSERT INTO media (title,msgId,data,downloaded,size) VALUES (?,?,?,?,?)"
    await db.executemany(sql,(msg_list))                        
    await db.commit() 
    await db.close()                                     
    print("Database updated.")



async def start():

    takeout = await login(phone,canale)
    if takeout:
        id_ch = await takeout.get_entity(canale)
        print("Connected !", id_ch.title)
        fileName =  input('Enter new db name: ')
        last_id  = await last(fileName)    
        await databaseUp(id_ch,takeout,last_id,fileName)

loop = asyncio.get_event_loop()
task_start = loop.create_task(start())
loop.run_until_complete(task_start)
