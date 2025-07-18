from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from first_successful_RAG.restaurant_chatbot import RestaurantChatbot
import uvicorn

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = RestaurantChatbot()

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/chat", response_model=MessageResponse)
async def chat_endpoint(request: MessageRequest):
    try:
        response = chatbot.chat(request.message)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)