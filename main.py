from fastapi import FastAPI
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")

supabase: Client = create_client(supabase_url, supabase_key)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def welcome():
    return "HI"


@app.get("/get_all_messages")
def get_messages():
    allChats = []

    # get all chats for user 23
    response = supabase.table("chats").select("*").eq("user_id", 23).execute()
    chats = response.data

    for chat in chats:
        chat_id = chat["id"]

        res = supabase.table("messages").select("*").eq("user_id", chat_id).execute()
        sorted_chat = sorted(res.data, key=lambda x: x["id"])
        allChats.append({"chat": chat, "messages": sorted_chat})

    # single_chat = allChats[0]["messages"]
    # sorted_chat = sorted(single_chat, key=lambda x: x["id"])

    return allChats


@app.get("/chats")
def get_chats():
    res = supabase.table("chats").select("*").eq("user_id",23).execute()

    return res.data


@app.get("/messages/{id}")
def get_chats(id:int):
    res = supabase.table("messages").select("*").eq("user_id", id).execute()

    single_chat = res.data
    sorted_chat = sorted(single_chat, key=lambda x: x["id"])
    return sorted_chat
