from fastapi import FastAPI

app = FastAPI()
'''
agent/create
agent/delete
agent/stop
agent/start
agent/chat
'''

@app.post("/agent/create")
def create_agent():
    return {"Hello": "World"}

@app.post("/agent/delete")
def delete_agent():
    return {"Hello": "World"}

@app.post("/agent/stop")
def start_agent():
    return {"Hello": "World"}

@app.post("/agent/stop")
def stop_agent():
    return {"Hello": "World"}

@app.post("/agent/chat")
def chat_with_agent():
    return {"Hello": "World"}