"""
IRO AI API 라우트 통합
"""

from flask import request, jsonify
import numpy as np
import os

# 전역 변수 (시스템 구성 요소들)
neural_net = None
extractor = None
knowledge_db = None
openai_client = None

def register_routes(app):
    """Flask 앱에 API 라우트 등록"""
    
    # 시스템 초기화
    init_system()
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            user_input = data.get('message', '').strip()
            
            if not user_input:
                return jsonify({'error': 'Empty message'}), 400
            
            # 1. 특징 추출
            features = extractor.extract_features(user_input)
            
            # 2. 신경망 분석
            probabilities = neural_net.forward(features)[0]
            category = int(np.argmax(probabilities))
            confidence = float(probabilities[category])
            
            # 3. OpenAI 응답 생성
            response_text = openai_client.generate_response(user_input, category)
            
            # 4. 대화 저장
            conv_id = knowledge_db.add_conversation(
                user_input, features, category, confidence, response_text
            )
            
            # 5. 신경망 대화 카운터 증가
            neural_net.training_history['total_conversations'] += 1
            
            return jsonify({
                'response': response_text,
                'category': category,
                'confidence': confidence,
                'conversation_id': conv_id,
                'brain_status': neural_net.get_brain_status()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/feedback', methods=['POST'])
    def feedback():
        try:
            data = request.get_json()
            conv_id = data.get('conversation_id')
            correct_category = data.get('correct_category')
            rating = data.get('rating', 5)
            
            success = knowledge_db.add_feedback(conv_id, correct_category, rating)
            
            return jsonify({
                'success': success,
                'message': '피드백이 저장되었습니다!'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/train', methods=['POST'])
    def train():
        try:
            # 학습 데이터 준비
            X, y = knowledge_db.get_training_data()
            
            if X is None:
                return jsonify({
                    'error': 'Insufficient training data',
                    'message': '최소 3개의 피드백이 필요합니다.'
                }), 400
            
            # 학습 실행
            accuracy = neural_net.train(X, y, epochs=30)
            
            # 자동 성장 판단
            should_grow, reason = neural_net.should_grow(
                accuracy, 
                knowledge_db.get_statistics()['total_feedback']
            )
            
            grown = False
            if should_grow:
                neural_net.grow_network()
                accuracy = neural_net.train(X, y, epochs=15)  # 재학습
                grown = True
            
            # 모델 저장
            neural_net.save(os.getenv('MODEL_PATH', '../data/models/iro_brain.pkl'))
            
            return jsonify({
                'success': True,
                'accuracy': float(accuracy),
                'grown': grown,
                'neurons': neural_net.hidden_size,
                'reason': reason if grown else 'No growth needed'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/status', methods=['GET'])
    def status():
        try:
            brain_status = neural_net.get_brain_status()
            db_stats = knowledge_db.get_statistics()
            
            return jsonify({
                'neural_network': brain_status,
                'knowledge_base': db_stats,
                'system_ready': True
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def init_system():
    """시스템 구성 요소 초기화"""
    global neural_net, extractor, knowledge_db, openai_client
    
    if neural_net is not None:  # 이미 초기화됨
        return
    
    print("🔧 시스템 구성 요소 초기화 중...")
    
    try:
        # 모듈 임포트
        from neural_network.growing_network import SelfGrowingNeuralNetwork
        from neural_network.feature_extractor import IRORobotFeatureExtractor
        from knowledge_base.database import KnowledgeDatabase
        from api_integration.openai_client import OpenAIClient
        
        # 신경망 로드 또는 생성
        model_path = os.getenv('MODEL_PATH', '../data/models/iro_brain.pkl')
        if os.path.exists(model_path):
            neural_net = SelfGrowingNeuralNetwork.load(model_path)
            print(f"📂 저장된 신경망 로드: {neural_net.hidden_size}개 뉴런")
        else:
            neural_net = SelfGrowingNeuralNetwork()
            print("🧠 새로운 신경망 생성")
        
        # 다른 구성 요소들
        extractor = IRORobotFeatureExtractor()
        knowledge_db = KnowledgeDatabase()
        openai_client = OpenAIClient()
        
        print("✅ 시스템 구성 요소 초기화 완료!")
        
    except ImportError as e:
        print(f"❌ 모듈 임포트 실패: {e}")
        print("💡 아직 구현되지 않은 모듈이 있습니다.")
        raise
    except Exception as e:
        print(f"❌ 시스템 초기화 실패: {e}")
        raise
