Llama3 Container와 연결된 Python FastApi Server  

ollama Container 실행 ( GPU O, 없다면 --gpus all 옵션 제거 )
+ ollama Docker Container run : `docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama --memory=8g ollama/ollama` 




가상환경 활성화 : `.\.venv\Scripts\activate`  

API Server 실행 : `uvicorn Llama.api:app --reload --host 0.0.0.0 --port 8300`