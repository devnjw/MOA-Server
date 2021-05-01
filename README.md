# MOA Flask Server Version 2.0

### 사용법
```
git clone https://github.com/HGUMOA/MOA_server_v2.git
cd MOA_server_v2
pip install -r requirements.txt
flask run
```

### 사용법 For MOA Developers
```
cd v2_moa_server
conda activate moav2
flask run -h "0.0.0.0"
```

+ 코드 수정하면서 서버 돌리고 싶으면 이 명령어도 실행 (=>코드가 수정되면 서버가 자동 reload 된다.)
```
export FLASK_ENV=development
```
