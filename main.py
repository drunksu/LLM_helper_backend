import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from utils import lifespan, register_error, SuccessResponse
from services import answer
import asyncio
from fastapi.responses import StreamingResponse


# 使用lifespan函数来完成初始化和退出处理
app = FastAPI(lifespan=lifespan)

# 注册一些异常处理函数
register_error(app)

@app.get("/")
async def root():
    return "hello world!"

# 定义post JSON格式
class HelloRequest(BaseModel):
    name: str
    
@app.post("/hello")
async def hellowho(hello_request: HelloRequest):
    return "hello " + hello_request.name

class RequestQuestion(BaseModel):
    question: str

# 流式响应的生成器函数
async def stream_generator(question: str):
    response_text = answer(question)
    for word in response_text.split():
        yield word + " "
        await asyncio.sleep(0.5)  

# 修改路由以支持流式响应
@app.post("/api/response")
async def response(request_question: RequestQuestion):
    return StreamingResponse(stream_generator(request_question.question), media_type="text/plain")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    uvicorn.run(app, host=host, port=port)