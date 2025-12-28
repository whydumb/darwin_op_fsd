"""
IRO AI 모듈 완전 생성 및 테스트 스크립트
"""

import os
import sys

print("🔧 IRO AI 모듈 문제 완전 해결")
print("=" * 60)

# 프로젝트 루트 경로 설정
project_root = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(project_root, 'backend')

print(f"📂 프로젝트 루트: {project_root}")
print(f"📂 백엔드 경로: {backend_path}")

def create_file(filepath, content):
    """파일 생성 헬퍼 함수"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✅ 생성: {filepath}")

# 1단계: 필수 디렉토리 생성
print("\n📁 1단계: 디렉토리 구조 생성...")
directories = [
    'backend/neural_network',
    'backend/knowledge_base', 
    'backend/api_integration',
    'backend/api',
    'backend/utils',
    'data/models',
    'data/knowledge',
    'data/logs'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"   ✅ {directory}")

# 2단계: __init__.py 파일들 생성
print("\n📝 2단계: 패키지 초기화 파일 생성...")
init_files = [
    'backend/__init__.py',
    'backend/neural_network/__init__.py',
    'backend/knowledge_base/__init__.py',
    'backend/api_integration/__init__.py',
    'backend/api/__init__.py',
    'backend/utils/__init__.py'
]

for init_file in init_files:
    package_name = os.path.dirname(init_file).replace('/', '.').replace('\\', '.')
    content = f'"""{package_name} 패키지"""\n'
    create_file(init_file, content)

# 3단계: 핵심 모듈 파일 생성
print("\n🧠 3단계: 신경망 모듈 생성...")

growing_network_code = '''"""
자가 성장형 신경망 - 실제 학습하고 성장하는 AI
"""

import numpy as np
import pickle
import os
from datetime import datetime

class SelfGrowingNeuralNetwork:
    def __init__(self, input_size=10, hidden_size=8, output_size=3, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Xavier 초기화
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))
        
        # 학습 이력
        self.training_history = {
            'loss': [], 'accuracy': [], 'epochs': 0,
            'growth_events': [], 'total_conversations': 0
        }
        
        print(f"🧠 신경망 초기화: {hidden_size}개 뉴런")
    
    def relu(self, x):
        """ReLU 활성화 함수"""
        return np.maximum(0, x)
    
    def softmax(self, x):
        """Softmax 활성화 함수"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        """순전파"""
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    def backward(self, X, y_true, y_pred):
        """역전파 - 실제 학습"""
        m = X.shape[0]
        
        # 출력층 그래디언트
        dz2 = y_pred - y_true
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        # 은닉층 그래디언트
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * (self.z1 > 0)  # ReLU 미분
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # 가중치 업데이트
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def train(self, X, y, epochs=50, verbose=True):
        """신경망 학습"""
        if verbose:
            print(f"\\n🎓 학습 시작: {X.shape[0]}개 샘플, {epochs} 에포크")
        
        for epoch in range(epochs):
            output = self.forward(X)
            loss = -np.sum(y * np.log(np.clip(output, 1e-15, 1-1e-15))) / X.shape[0]
            self.backward(X, y, output)
            
            accuracy = np.mean(np.argmax(output, axis=1) == np.argmax(y, axis=1))
            self.training_history['loss'].append(loss)
            self.training_history['accuracy'].append(accuracy)
            
            if verbose and (epoch + 1) % 10 == 0:
                print(f"   에포크 {epoch+1}/{epochs} - 손실: {loss:.4f}, 정확도: {accuracy*100:.1f}%")
        
        self.training_history['epochs'] += epochs
        return accuracy
    
    def grow_network(self, new_neurons=2):
        """신경망 확장 - 뇌 용량 증가"""
        print(f"\\n🌱 신경망 성장: {self.hidden_size} → {self.hidden_size + new_neurons}개 뉴런")
        
        old_size = self.hidden_size
        self.hidden_size += new_neurons
        
        # 새로운 가중치 생성
        new_W1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0 / self.input_size)
        new_b1 = np.zeros((1, self.hidden_size))
        new_W2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0 / self.hidden_size)
        
        # 기존 지식 보존
        new_W1[:, :old_size] = self.W1
        new_b1[:, :old_size] = self.b1
        new_W2[:old_size, :] = self.W2
        
        # 가중치 교체
        self.W1, self.b1, self.W2 = new_W1, new_b1, new_W2
        
        # 성장 이벤트 기록
        self.training_history['growth_events'].append({
            'timestamp': datetime.now().isoformat(),
            'old_size': old_size, 'new_size': self.hidden_size
        })
        
        print("✅ 신경망 확장 완료! 🧠✨")
    
    def should_grow(self, accuracy, data_count):
        """자동 성장 판단"""
        if self.hidden_size >= 30:
            return False, "최대 크기 도달"
        if accuracy < 0.7:
            return True, f"낮은 정확도 ({accuracy*100:.1f}%)"
        if data_count > 20 and self.hidden_size < 15:
            return True, f"충분한 데이터 ({data_count}개)"
        return False, "현재 크기로 충분"
    
    def predict(self, X):
        """예측"""
        return np.argmax(self.forward(X), axis=1)
    
    def get_brain_status(self):
        """뇌 상태 정보"""
        return {
            'neurons': self.hidden_size,
            'total_parameters': (self.input_size * self.hidden_size + 
                               self.hidden_size * self.output_size + 
                               self.hidden_size + self.output_size),
            'epochs_trained': self.training_history['epochs'],
            'growth_events': len(self.training_history['growth_events']),
            'conversations': self.training_history['total_conversations']
        }
    
    def save(self, filepath):
        """모델 저장"""
        data = {
            'weights': {'W1': self.W1, 'b1': self.b1, 'W2': self.W2, 'b2': self.b2},
            'config': {'input_size': self.input_size, 'hidden_size': self.hidden_size,
                      'output_size': self.output_size, 'learning_rate': self.learning_rate},
            'history': self.training_history
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"💾 저장: {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """모델 로드"""
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            config = data['config']
            nn = cls(**config)
            weights = data['weights']
            nn.W1, nn.b1, nn.W2, nn.b2 = weights['W1'], weights['b1'], weights['W2'], weights['b2']
            nn.training_history = data['history']
            print(f"📂 로드: {nn.hidden_size}개 뉴런")
            return nn
        except Exception as e:
            print(f"❌ 로드 실패: {e}")
            return None
'''

create_file('backend/neural_network/growing_network.py', growing_network_code)

print("\n🔍 4단계: 특징 추출기 생성...")

feature_extractor_code = '''"""
IRO 로봇 대회 특화 특징 추출기
"""

import numpy as np

class IRORobotFeatureExtractor:
    def __init__(self):
        # IRO 관련 키워드 사전
        self.tech_keywords = ['아두이노', 'arduino', '센서', 'sensor', '모터', 'motor',
                             '코딩', '프로그래밍', 'c++', 'c언어', '라인트레이싱']
        self.iro_keywords = ['iro', '로봇', 'robot', '올림피아드', '대회', '우주', '미션']
        self.creative_keywords = ['아이디어', '디자인', '창의', '설계', '개발']
        
        print("🔍 IRO 특화 특징 추출기 초기화 완료")
    
    def extract_features(self, text):
        """텍스트를 10차원 특징 벡터로 변환"""
        if not text or not text.strip():
            return np.zeros((1, 10))
        
        features = []
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # 1. 텍스트 길이 (정규화)
        features.append(min(len(text) / 100.0, 1.0))
        
        # 2. 단어 수 (정규화)
        features.append(min(word_count / 30.0, 1.0))
        
        # 3. 질문 표현
        question_indicators = ['어떻게', '무엇', '왜', '?', '방법']
        has_question = any(indicator in text for indicator in question_indicators)
        features.append(1.0 if has_question else 0.0)
        
        # 4. 기술 키워드 밀도
        tech_count = sum(1 for keyword in self.tech_keywords if keyword in text_lower)
        features.append(min(tech_count / 3.0, 1.0))
        
        # 5. IRO 대회 관련도
        iro_count = sum(1 for keyword in self.iro_keywords if keyword in text_lower)
        features.append(min(iro_count / 2.0, 1.0))
        
        # 6. 창의적 표현
        creative_count = sum(1 for keyword in self.creative_keywords if keyword in text_lower)
        features.append(min(creative_count / 2.0, 1.0))
        
        # 7. 명령/요청 표현
        command_keywords = ['해줘', '알려줘', '설명해', '도와줘']
        is_command = any(keyword in text for keyword in command_keywords)
        features.append(1.0 if is_command else 0.0)
        
        # 8. 감정 표현
        emotion_indicators = ['!', 'ㅋ', 'ㅎ', '좋아', '감사']
        emotion_count = sum(1 for indicator in emotion_indicators if indicator in text)
        features.append(min(emotion_count / 3.0, 1.0))
        
        # 9. 숫자 포함 여부
        has_numbers = any(char.isdigit() for char in text)
        features.append(1.0 if has_numbers else 0.0)
        
        # 10. 문장 복잡도
        if word_count > 0:
            avg_word_length = sum(len(word) for word in words) / word_count
            features.append(min(avg_word_length / 8.0, 1.0))
        else:
            features.append(0.0)
        
        return np.array(features).reshape(1, -1)
'''

create_file('backend/neural_network/feature_extractor.py', feature_extractor_code)

print("\n📚 5단계: 지식 데이터베이스 생성...")

database_code = '''"""
지식 데이터베이스 - 대화 및 피드백 관리
"""

import json
import os
from datetime import datetime
import numpy as np

class KnowledgeDatabase:
    def __init__(self, db_path='data/knowledge/database.json'):
        self.db_path = db_path
        self.data = self._load_database()
    
    def _load_database(self):
        """데이터베이스 로드 또는 생성"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"📚 기존 DB 로드: {len(data.get('conversations', []))}개 대화")
                return data
            except Exception as e:
                print(f"⚠️ DB 로드 실패: {e}, 새로 생성")
        
        print("📚 새로운 지식 데이터베이스 생성")
        return {'conversations': [], 'feedback': []}
    
    def save(self):
        """데이터베이스 저장"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_conversation(self, user_input, features, category, confidence, response=""):
        """대화 기록 추가"""
        conv_id = len(self.data['conversations'])
        self.data['conversations'].append({
            'id': conv_id,
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'features': features.flatten().tolist(),
            'predicted_category': int(category),
            'confidence': float(confidence),
            'response': response,
            'feedback_given': False
        })
        self.save()
        return conv_id
    
    def add_feedback(self, conv_id, correct_category, rating=5):
        """사용자 피드백 추가"""
        if conv_id < len(self.data['conversations']):
            self.data['conversations'][conv_id]['feedback_given'] = True
            
            self.data['feedback'].append({
                'conversation_id': conv_id,
                'correct_category': int(correct_category),
                'rating': int(rating),
                'timestamp': datetime.now().isoformat()
            })
            self.save()
            return True
        return False
    
    def get_training_data(self):
        """학습용 데이터셋 생성"""
        feedback_dict = {f['conversation_id']: f for f in self.data['feedback']}
        
        X_list = []
        y_list = []
        
        for conv in self.data['conversations']:
            if conv['id'] in feedback_dict:
                X_list.append(conv['features'])
                y_list.append(feedback_dict[conv['id']]['correct_category'])
        
        if len(X_list) < 3:  # 최소 3개 필요
            return None, None
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        # One-hot encoding
        y_onehot = np.zeros((y.size, 3))
        y_onehot[np.arange(y.size), y] = 1
        
        return X, y_onehot
    
    def get_statistics(self):
        """통계 정보 반환"""
        total_conversations = len(self.data['conversations'])
        total_feedback = len(self.data['feedback'])
        
        feedback_rate = (total_feedback / max(total_conversations, 1)) * 100
        
        return {
            'total_conversations': total_conversations,
            'total_feedback': total_feedback,
            'feedback_rate': feedback_rate
        }
'''

create_file('backend/knowledge_base/database.py', database_code)

# 6단계: 테스트 파일 수정
print("\n🧪 6단계: 테스트 파일 업데이트...")

test_integration_code = '''"""
시스템 통합 테스트 스크립트 - 경로 문제 해결 포함
"""

import sys
import os

# 경로 문제 해결
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_path = os.path.join(project_root, 'backend')

print(f"🔍 프로젝트 루트: {project_root}")
print(f"🔍 백엔드 경로 추가: {backend_path}")

# Python 경로에 추가
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

def test_imports():
    """모든 모듈 임포트 테스트"""
    print("\\n🧪 모듈 임포트 테스트 시작...")
    
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
        print("⚠️ 일부 모듈에 문제가 있습니다.")
'''

create_file('tests/test_integration.py', test_integration_code)

# 7단계: 즉시 테스트 실행
print("\n🚀 7단계: 즉시 테스트 실행...")

# Python 경로에 백엔드 추가
sys.path.insert(0, backend_path)

test_results = []

try:
    from neural_network.growing_network import SelfGrowingNeuralNetwork
    print("   ✅ 신경망 모듈 로드 성공")
    test_results.append(True)
except Exception as e:
    print(f"   ❌ 신경망 모듈 실패: {e}")
    test_results.append(False)

try:
    from neural_network.feature_extractor import IRORobotFeatureExtractor
    print("   ✅ 특징 추출기 로드 성공")
    test_results.append(True)
except Exception as e:
    print(f"   ❌ 특징 추출기 실패: {e}")
    test_results.append(False)

try:
    from knowledge_base.database import KnowledgeDatabase
    print("   ✅ 데이터베이스 로드 성공")
    test_results.append(True)
except Exception as e:
    print(f"   ❌ 데이터베이스 실패: {e}")
    test_results.append(False)

# 최종 결과
success_count = sum(test_results)
total_count = len(test_results)

print("\n" + "=" * 60)
print(f"📊 최종 테스트 결과: {success_count}/{total_count} 성공")
print("=" * 60)

if success_count == total_count:
    print("🎉 모든 모듈이 성공적으로 생성되고 테스트되었습니다!")
    print("\\n📋 다음 단계:")
    print("   1. .env 파일에 OpenAI API 키 설정")
    print("   2. python backend/main.py 실행")
    print("   3. 브라우저에서 http://localhost:5000 접속")
else:
    print("⚠️ 일부 모듈에 문제가 있습니다.")
    print("💡 오류 메시지를 확인하고 필요한 패키지를 설치하세요:")
    print("   pip install numpy")
