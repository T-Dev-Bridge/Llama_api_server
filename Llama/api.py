from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from Llama.LlamaResponseModel import LlamaResponse, Message
import requests
import os

from dotenv import load_dotenv
from database.connect.deps import get_db
from database.models.markdown_result import MarkeDownResult, create_mark_down_result
from sqlalchemy.orm import Session

app = FastAPI()

load_dotenv()

# Llama 컨테이너의 URL 및 포트 설정
LLAMA_API_URL = f"http://{os.getenv('LLAMA_HOST')}:{os.getenv('LLAMA_PORT')}/api/chat"

@app.get("/", response_class=JSONResponse) 
def read_root():
    return {"message": "Hello, World!"}

@app.post("/ask", response_class=PlainTextResponse)
async def ask_llama(question: Message, lang: str = Query("en"), db: Session = Depends(get_db)):
    """
    Llama 컨테이너에 질문을 보내고 Markdown 형식으로 응답을 반환합니다.
    """
    try:
        payload = {
            "model": "llama3",
            "messages": [{"role": question.role, "content": question.content + "MarkDown 문법의 파일 형식으로 결과를"}]
        }
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Llama API 호출 실패: {e}")

    try:
        markdown_content_list = []

        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                llama_response = LlamaResponse.parse_raw(line)
                markdown_content_list.append(llama_response.message.content)

        # 마크다운 응답들을 하나로 결합
        markdown_content = "".join(markdown_content_list)
        create_mark_down_result(db, MarkeDownResult(markdown=markdown_content))

        return PlainTextResponse(content=markdown_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NDJSON 처리 중 오류 발생: {e}")
