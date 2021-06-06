#!/usr/bin/env python3.7
#Telethon 1.21.1

import asyncio
import aiosqlite
import os,sys
from telethon import TelegramClient
from telethon import events
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument
from datetime import datetime,timedelta 



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# User Data
#  

channel  = "https://t.me/"
phone    = ""
api_id   = ""
api_hash = ""
upday    = "2021-06-06"
percorso = "/home/"
client   = TelegramClient("hello", api_id, api_hash,flood_sleep_threshold =240) 


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



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# async workers 
#  

async def worker(queue):

    while True:
        queue_item = await queue.get()
        msg   = queue_item
        media = percorso + msg.file.name
        print (f"[{datetime.now().strftime('%H:%M')}] Download -> [{media}]")
        try:
            await takeout.download_media(msg,percorso)
        except errors.FileReferenceExpiredError:    
            print (f"[{datetime.now().strftime('%H:%M')}]",f"§Expired§ => {media} ")         
            await delete_file(media)
            db = await aiosqlite.connect(fileName)
            cursor = await db.execute("UPDATE  media SET downloaded ='---' WHERE msgId=?", (msg.id,))
            await db.commit()             
            await db.close()
        except errors.TimeoutError:
            print (f"[{datetime.now().strftime('%H:%M')}]",
                   f"§Incompleto§ => {media} ")
            await delete_file(media)
            db = await aiosqlite.connect(fileName)
            cursor = await db.execute("UPDATE media SET downloaded ='---' WHERE msgId=?", (msg.id,))
            await db.commit()             
            await db.close()
        else:
            db = await aiosqlite.connect(fileName)
            cursor = await db.execute("UPDATE media SET downloaded ='V' WHERE msgId=?", (msg.id,))
            await db.commit()             
            await db.close()
            print (f"[{datetime.now().strftime('%H:%M')}]",
                   f"Completato {media} ")            
        finally:    
            queue.task_done()



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Delete incomplete or expired downloaded file
#  

async def delete_file(fileName):
    result = os.remove(fileName)



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
            print ("step1 > Please check service notification in a few minutes. You must click the 'Allow' button")
            print ("step2 > Restart script")
            sys.exit()



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Open or Create database file
#  

async def openDB():
    
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

async def getLast ():

        db = await openDB()
        cursor = await db.execute("SELECT msgId FROM media ORDER BY msgId DESC")
        row    = await cursor.fetchone()
        if row is None:
           row = [0]
        await db.close()                                                
        return row[0]



#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Download the messages and save to db
#  

async def databaseUp(id_chat,last_id):
    
    msg_list = []
    db = await openDB()    
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



#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Prepara elenco per il download
#

async def getIds_byData():

        db     = await openDB()
        cursor = await db.execute("SELECT msgId FROM media WHERE data=? AND downloaded=?",(upday,'NO'))
        row = await cursor.fetchall()
        await db.close()
        if row:
            return [i for i in row]       
        else:
            print ("media not found.Please try with a different date")
            loop.stop()         
            print ("Quit.")



#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Downloader
#

async def downloader(id_ch,ids):

        queue = asyncio.Queue(1)
        workers = [asyncio.create_task(worker(queue)) for _ in range(10)]
        for msgId in ids:
            async for msg in takeout.iter_messages(id_ch, wait_time = 1, ids=msgId[0]):
                #msgId no more available
                if msg is None:
                        db = await aiosqlite.connect(fileName)
                        cursor = await db.execute("UPDATE media SET downloaded ='***' WHERE msgId=?", (msgId,))
                        await db.commit()             
                        await db.close()
                else: 
                    await queue.put(msg)                    
        await queue.join()
        #Delete every task
        for active_workers in workers:
            active_workers.cancel()



#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# START
#

async def start():

    id_ch = await takeout.get_entity(channel)
    print("Connected !", id_ch.title)
    last_id  = await getLast()    
    await databaseUp(id_ch,last_id)
    msgs_id = await getIds_byData()
    await downloader(id_ch,msgs_id)
    loop.stop()

loop = asyncio.get_event_loop()
task_login = loop.create_task(login(phone,channel))
loop.run_until_complete(task_login)
takeout = task_login.result()

fileName =  input('Enter a new db name: ')
try:
    task_start = loop.create_task(start())
    loop.run_forever()
except KeyboardInterrupt as keyint:
        print("bye !")