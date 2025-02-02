Llama3 Container와 연결된 Python FastApi Server  

ollama Container 실행 ( GPU O, 없다면 --gpus all 옵션 제거 )  
 `docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama --memory=8g ollama/ollama` 

 (컨테이너 접속 후) Model 설치 (Deepseek R1:1.5b) : `ollama pull deepseek-r1:1.5b`

 Model 설치 확인 : `ollama ps`

가상환경 활성화 : `.\.venv\Scripts\activate`  

API Server 실행 : `uvicorn Llama.api:app --reload --host 0.0.0.0 --port 8300`