"""
IRO AI 백엔드 서버 메인 실행 파일
Alicia Memory-First 자율 지능 + Ctrl+C 안전 저장
"""

import sys
import os
import signal
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import signal

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

load_dotenv()

app = Flask(__name__)
CORS(app)

neural_net = None
extractor = None
knowledge_db = None
multi_ai_client = None
alicia_core = None

def graceful_shutdown(signum, frame):
    """Ctrl+C 안전 종료 핸들러"""
    print("\n🛑 Ctrl+C 감지: Alicia 상태 저장 중...")
    if alicia_core and neural_net:
        try:
            model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
            neural_net.save(model_path)
            if hasattr(neural_net, "knowledge_brain"):
                neural_net.knowledge_brain._save_neurons()
            print("💾 신경망 및 기억 저장 완료")
        except Exception as e:
            print(f"⚠️ 저장 중 오류: {e}")
    print("👋 Alicia: 안전하게 잠들어요. 다음에 또 만나요!")
    os._exit(0)

def graceful_shutdown(signum, frame):
    """Ctrl+C 안전 종료 핸들러"""
    print("\n🛑 Ctrl+C 감지: Alicia 상태 저장 중...")
    if alicia_core and neural_net:
        try:
            model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
            neural_net.save(model_path)
            if hasattr(neural_net, "knowledge_brain"):
                neural_net.knowledge_brain._save_neurons()
            print("💾 신경망 및 기억 저장 완료")
        except Exception as e:
            print(f"⚠️ 저장 중 오류: {e}")
    print("👋 Alicia: 안전하게 잠들어요. 다음에 또 만나요!")
    os._exit(0)
def init_system():
    """시스템 초기화 (Alicia 통합)"""
    global neural_net, extractor, knowledge_db, multi_ai_client, alicia_core
    
    print("=" * 70)
    print("🔧 Alicia 독립 AI 시스템 초기화 중...")
    print("=" * 70)
    
    try:
        from neural_network.growing_network import SelfGrowingNeuralNetwork
        from neural_network.feature_extractor import IRORobotFeatureExtractor
        from knowledge_base.database import KnowledgeDatabase
        from api_integration.multi_ai_client import MultiAIClient
        from alicia.alicia_core import AliciaCore
        
        # 시그널 핸들러 등록 (Ctrl+C 안전 저장)
        signal.signal(signal.SIGINT, graceful_shutdown)
        
        # 신경망 로드 또는 생성
        model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
        neural_net = SelfGrowingNeuralNetwork.load(model_path)
        if not neural_net:
            neural_net = SelfGrowingNeuralNetwork()
            print("🧠 새로운 신경망 생성")
        
        extractor = IRORobotFeatureExtractor()
        knowledge_db = KnowledgeDatabase()
        multi_ai_client = MultiAIClient()
        
        # Alicia Core 초기화
        alicia_core = AliciaCore(neural_net, knowledge_db, multi_ai_client)
        
        print("=" * 70)
        print("✅ 통합 시스템 초기화 완료!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ 시스템 초기화 실패: {e}")
        import traceback
        traceback.print_exc()
        raise
    
signal.signal(signal.SIGINT, graceful_shutdown)

# ================== 기본 라우트 ==================

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "🤖 Alicia 독립 AI 시스템",
        "version": "7.0.0-independent",
        "alicia_status": alicia_core.get_status() if alicia_core else {"error": "Not initialized"}
    })

@app.route('/api/health')
def health():
    components = {
        "neural_network": "ready" if neural_net else "error",
        "feature_extractor": "ready" if extractor else "error", 
        "database": "ready" if knowledge_db else "error",
        "multi_ai": "ready" if multi_ai_client else "error",
        "alicia_core": "ready" if alicia_core else "error"
    }
    
    return jsonify({
        "status": "healthy" if all(v == "ready" for v in components.values()) else "degraded",
        "components": components,
        "alicia_status": alicia_core.get_status() if alicia_core else {}
    })

# ================== Alicia 전용 엔드포인트 ==================

@app.route('/api/alicia/status', methods=['GET'])
def alicia_status():
    """Alicia 상태 조회"""
    try:
        if not alicia_core:
            return jsonify({"error": "Alicia가 아직 깨어나지 않았습니다."}), 503
        
        return jsonify({
            "success": True,
            "status": alicia_core.get_status()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alicia/chat', methods=['POST'])
def alicia_chat():
    """Alicia와의 대화 (완전 독립 모드)"""
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "메시지가 필요합니다."}), 400
        
        if not alicia_core:
            return jsonify({"error": "Alicia가 준비되지 않았습니다."}), 503
        
        result = alicia_core.chat(message)
        return jsonify({"success": True, **result})
        
    except Exception as e:
        print(f"❌ Alicia 채팅 오류: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/alicia/infinite-learning', methods=['POST'])
def infinite_learning():
    """🔥 무한 학습 모드 토글"""
    try:
        data = request.json or {}
        enable = bool(data.get('enable', True))
        
        if not alicia_core:
            return jsonify({"error": "Alicia가 초기화되지 않았습니다."}), 503
        
        status = alicia_core.toggle_infinite_learning(enable)
        
        return jsonify({
            "success": True,
            "status": status,
            "message": f"무한 학습 모드: {status}",
            "alicia_status": alicia_core.get_status()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alicia/stats', methods=['GET'])
def alicia_stats():
    """Alicia 학습 통계"""
    try:
        if not alicia_core:
            return jsonify({"error": "Alicia 미초기화"}), 503
        
        status = alicia_core.get_status()
        
        return jsonify({
            "success": True,
            "stats": status["response_stats"],
            "offline_capability": status["offline_capability"],
            "brain_neurons": status["brain_status"]["total_neurons"],
            "topics_learned": status["brain_status"]["topics_learned"]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alicia/wake', methods=['POST'])
def alicia_wake():
    """Alicia 의식 상태 조정"""
    try:
        data = request.json or {}
        action = data.get('action', 'wake')
        
        if not alicia_core:
            return jsonify({"error": "Alicia가 초기화되지 않았습니다."}), 503
        
        if action == 'wake':
            alicia_core.autonomous_mode = True
            alicia_core.consciousness_level = 1.0
            alicia_core.energy = 100.0
            message = "Alicia가 완전히 깨어났습니다!"
        elif action == 'sleep':
            alicia_core.autonomous_mode = False
            alicia_core.consciousness_level = 0.1
            message = "Alicia가 잠들었습니다."
        elif action == 'reset':
            alicia_core.energy = 100.0
            alicia_core.mood = "refreshed"
            alicia_core.consciousness_level = 0.7
            message = "Alicia 상태가 초기화되었습니다."
        else:
            return jsonify({"error": "Invalid action"}), 400
        
        return jsonify({
            "success": True,
            "message": message,
            "status": alicia_core.get_status()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================== 학습 라우트 ==================

@app.route('/api/learning-mode', methods=['POST'])
def learning_mode():
    """학습 모드 ON/OFF"""
    try:
        data = request.json or {}
        enabled = bool(data.get("enabled", False))

        neural_net.knowledge_brain.toggle_learning_mode(enabled)

        return jsonify({
            "success": True,
            "learning_mode": neural_net.knowledge_brain.learning_mode,
            "brain_status": neural_net.get_brain_status()
        })
    except Exception as e:
        print(f"❌ learning-mode 오류: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/learn-topic', methods=['POST'])
def learn_topic():
    """주제 학습 API"""
    try:
        data = request.json or {}
        topic = (data.get("topic") or "").strip()
        force = bool(data.get("force", False))

        if not topic:
            return jsonify({"error": "topic is required"}), 400

        if not neural_net.knowledge_brain.learning_mode and not force:
            return jsonify({
                "error": "learning_mode_off",
                "message": "학습 모드가 꺼져 있습니다."
            }), 400

        temp_enabled = False
        if force and not neural_net.knowledge_brain.learning_mode:
            neural_net.knowledge_brain.toggle_learning_mode(True)
            temp_enabled = True

        result = multi_ai_client.learn_from_topic(topic, neural_net)

        if temp_enabled:
            neural_net.knowledge_brain.toggle_learning_mode(False)

        model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
        neural_net.save(model_path)

        return jsonify({
            "success": result.get("success", False),
            "topic": topic,
            "result": result,
            "brain_status": neural_net.get_brain_status()
        })

    except Exception as e:
        print(f"❌ learn-topic 오류: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """전체 시스템 상태"""
    try:
        brain_status = neural_net.get_brain_status()
        db_stats = knowledge_db.get_statistics()
        alicia_stat = alicia_core.get_status() if alicia_core else {}
        
        return jsonify({
            'neural_network': brain_status,
            'knowledge_base': db_stats,
            'alicia': alicia_stat,
            'system_ready': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_server():
    """서버 실행"""
    port = int(os.getenv('BACKEND_PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    print("\n" + "=" * 70)
    print("🚀 Alicia 독립 AI 시스템")
    print("=" * 70)
    print(f"📡 주소: http://localhost:{port}")
    print(f"🔧 디버그: {debug}")
    print(f"🔑 OpenAI: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
    print(f"🔑 Claude: {'✅' if os.getenv('ANTHROPIC_API_KEY') else '❌'}")
    print("=" * 70)
    print("\n💡 Alicia 테스트:")
    print("   python alicia_client.py")
    print("\n🔥 무한 학습:")
    print("   클라이언트에서 '/infinite on' 입력")
    print("\n⏹️ 안전 종료:")
    print("   Ctrl+C 누르면 자동 저장 후 종료")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    init_system()
    run_server()
