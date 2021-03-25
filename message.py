# Questo modulo implementa una semplice versione di un database per i messaggi in memoria.

import uuid
from datetime import datetime
from result import Result
import user

messages = []
# Messaggi sono memorizzati come dizionari.
# messaggio = {
#    'id': '123'
#    'sender': 'sender@test.it',
#    'recipient': 'recipient@test.it',
#    'content': 'Testo del messaggio',
#    'created': '5-03-2024'
# }

#Metodo di utilità per cercare una conversazione dati in ingresso il mittente e il destinatario. Se non esistono messaggi viene ritornata una lista vuota
def findConversation(sender_id: str, recipient_id:str) -> list:
    conversation = []
    messagesSortedbyDate = sorted(messages, key=lambda m: m['created'], reverse=True)

    for message in messagesSortedbyDate:
        if message['sender'] == sender_id and message['recipient'] == recipient_id:
            conversation.append(message)

    return conversation

def findMessages(reader_id: str) -> list:
    inbox = []
    messagesSortedbyDate = sorted(messages, key=lambda m: m['created'], reverse=True)

    for message in messagesSortedbyDate:
        if message['recipient'] == reader_id:
            inbox.append(message)

    return inbox

#Metodo di utilità per cercare un messaggio dato in ingresso un ID. Se non esiste viene ritornato None
def findMessageByID(id: str) -> dict:
    bID = uuid.UUID(id)
    for message in messages:
        if message['id'] == bID:
            return message
    return None

#SaveMessage memorizza un messaggio nel sistema
def SaveMessage(sender: str, recipient: str, content: str) -> (Result, dict):
    id = uuid.uuid4()
    
    senderData = user.findUserByEmail(sender)
    if senderData is None:
        return Result.NOT_FOUND, None

    recipientData = user.findUserByEmail(recipient)
    if recipientData is None:
        return Result.NOT_FOUND, None

    senderID = senderData['id']
    recipientID = recipientData['id']

    message = {
        'id': id,
        'sender': senderID,
        'recipient': recipientID,
        'content': content,
        'created': datetime.utcnow().isoformat()
    }
    
    messages.append(message.copy())

    response = {
        'id': message['id'],
        'sender': sender,
        'recipient': recipient,
        'content': message['content'],
        'created': message['created']
    }
    
    return Result.OK, response

def GetMessages(reader: str) -> (Result, list):
    readerData = user.findUserByEmail(reader)
    if readerData is None:
        return Result.NOT_FOUND, None

    inbox = findMessages(readerData['id'])

    return Result.OK, inbox