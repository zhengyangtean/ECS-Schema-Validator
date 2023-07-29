
pip install -r requirements.txt
docker compose up -d && echo "sleep for 30sec for ES to startup" && sleep 30
python tools/upload.py
cd app 
uvicorn main:app
