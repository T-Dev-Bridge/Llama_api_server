from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from Llama.LlamaResponseModel import LlamaResponse, Message
import requests
import markdown2

app = FastAPI()

# Llama 컨테이너의 URL 및 포트 설정
LLAMA_API_URL = "http://localhost:11434/api/chat"

@app.get("/", response_class=JSONResponse) 
def read_root():
    return {"message": "Hello, World!"}

@app.post("/ask", response_class=HTMLResponse)
async def ask_llama(question: Message, lang: str = Query("en")):
    """
    Llama 컨테이너에 질문을 보내고 Markdown 형식으로 응답을 반환합니다.
    """
    # Llama API에 요청 보내기
    try:
        payload = {
            "model": "llama3",
            "messages": [{"role": question.role, "content": question.content + "MarkDown 문법의 파일 형식으로 결과를"}]
        }
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Llama API 호출 실패: {e}")

    # NDJSON 응답 처리 (스트리밍 방식)
    try:
        html_content_list = []

        for line in response.iter_lines(decode_unicode=True):
            if line.strip():  # 빈 줄 무시
                # 각 줄을 JSON으로 파싱하여 Pydantic 모델로 변환
                llama_response = LlamaResponse.parse_raw(line)
                html_content_list.append(markdown2.markdown(llama_response.message.content))

        # 여러 응답을 HTML로 결합 (구분선 추가)
        html_content = "".join(html_content_list)

        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NDJSON 처리 중 오류 발생: {e}")