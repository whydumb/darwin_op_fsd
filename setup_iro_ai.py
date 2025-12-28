"""
IRO AI 프로젝트 자동 설정 스크립트
모든 폴더 구조와 기본 파일들을 자동으로 생성합니다.
"""

import os
import sys

def create_project_structure():
    print("🏗️ IRO AI 프로젝트 구조 생성 중...")
    print("=" * 50)
    
    # 폴더 구조 정의
    directories = [
        # 백엔드 구조
        'backend/neural_network',
        'backend/knowledge_base', 
        'backend/api_integration',
        'backend/api',
        'backend/utils',
        
        # 프론트엔드 구조
        'frontend/src/components',
        'frontend/src/services',
        'frontend/src/styles',
        'frontend/public',
        
        # 데이터 및 설정
        'data/models',
        'data/knowledge',
        'data/logs',
        'config',
        'scripts',
        'tests'
    ]
    
    # 폴더 생성
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Python 패키지용 __init__.py 생성
        if directory.startswith('backend/'):
            init_file = os.path.join(directory, '__init__.py')
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f'"""{directory} 모듈"""\n')
        
        print(f"✅ 생성: {directory}")
    
    # 환경 설정 파일 생성
    create_config_files()
    
    # 필수 Python 파일 생성
    create_python_files()
    
    print("\n🎉 프로젝트 구조 생성 완료!")
    print("📋 다음 단계:")
    print("   1. .env 파일에 API 키 입력")
    print("   2. pip install -r requirements.txt")
    print("   3. python backend/main.py 실행")

def create_config_files():
    """설정 파일들 생성"""
    
    # .env 파일
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here

# 서버 설정
BACKEND_PORT=5000
FRONTEND_PORT=3000

# 데이터 경로
DB_PATH=data/knowledge/database.json
MODEL_PATH=data/models/iro_brain.pkl

# 로그 설정
LOG_LEVEL=INFO
LOG_DIR=data/logs

# 개발 모드
DEBUG=true
""")
        print("✅ .env 파일 생성 (API 키를 입력하세요!)")
    
    # requirements.txt
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write("""# 핵심 라이브러리
openai==1.12.0
python-dotenv==1.0.0
numpy==1.24.3

# 웹 프레임워크
flask==3.0.0
flask-cors==4.0.0

# 데이터 처리
pandas==2.0.3
scikit-learn==1.3.0

# 유틸리티
pyyaml==6.0.1
requests==2.31.0
""")
        print("✅ requirements.txt 생성")

def create_python_files():
    """핵심 Python 파일들 생성"""
    
    # 백엔드 메인 실행 파일
    main_content = '''"""
IRO AI 백엔드 서버 메인 실행 파일
"""

import sys
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 환경변수 로드
load_dotenv()

# Flask 앱 생성
app = Flask(__name__)
CORS(app)

# 기본 라우트
@app.route('/')
def home():
    return {
        'status': 'running',
        'message': 'IRO AI Backend Server',
        'version': '2.0.0'
    }

@app.route('/api/health')
def health():
    return {
        'status': 'healthy',
        'components': {
            'neural_network': 'ready',
            'database': 'ready',
            'openai': 'ready' if os.getenv('OPENAI_API_KEY') else 'not configured'
        }
    }

# API 라우트 임포트 시도
try:
    from api.routes import register_routes
    register_routes(app)
    print("✅ API 라우트 로드 성공")
except ImportError as e:
    print(f"⚠️ API 라우트 로드 실패: {e}")
    print("   기본 라우트만 사용합니다")

def run_server():
    """서버 실행"""
    port = int(os.getenv('BACKEND_PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    print("="*60)
    print("🚀 IRO AI 백엔드 서버 시작")
    print("="*60)
    print(f"📡 주소: http://localhost:{port}")
    print(f"🔧 디버그 모드: {debug}")
    print(f"🔑 OpenAI API: {'설정됨' if os.getenv('OPENAI_API_KEY') else '미설정'}")
    print("="*60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    run_server()
'''
    
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("✅ backend/main.py 생성")
    
    # 테스트 스크립트
    test_content = '''"""
시스템 통합 테스트 스크립트
"""

import sys
import os
sys.path.append('backend')

def test_imports():
    """모든 모듈 임포트 테스트"""
    print("🧪 모듈 임포트 테스트 시작...")
    
    tests = []
    
    # 신경망 모듈 테스트
    try:
        from neural_network.growing_network import SelfGrowingNeuralNetwork
        print("✅ 신경망 모듈")
        tests.append(True)
    except Exception as e:
        print(f"❌ 신경망 모듈: {e}")
        tests.append(False)
    
    # 특징 추출기 테스트
    try:
        from neural_network.feature_extractor import IRORobotFeatureExtractor
        print("✅ 특징 추출기")
        tests.append(True)
    except Exception as e:
        print(f"❌ 특징 추출기: {e}")
        tests.append(False)
    
    # 데이터베이스 테스트
    try:
        from knowledge_base.database import KnowledgeDatabase
        print("✅ 데이터베이스")
        tests.append(True)
    except Exception as e:
        print(f"❌ 데이터베이스: {e}")
        tests.append(False)
    
    success_rate = sum(tests) / len(tests) * 100
    print(f"\\n📊 테스트 결과: {sum(tests)}/{len(tests)} 성공 ({success_rate:.1f}%)")
    
    return all(tests)

if __name__ == "__main__":
    if test_imports():
        print("🎉 모든 모듈이 정상적으로 로드되었습니다!")
    else:
        print("⚠️ 일부 모듈에 문제가 있습니다. 개별 구현이 필요합니다.")
'''
    
    with open('tests/test_integration.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    print("✅ tests/test_integration.py 생성")

if __name__ == "__main__":
    create_project_structure()
