"""
IRO AI 핵심 모듈 자동 생성 스크립트
"""

import os

def create_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 생성: {filepath}")

print("🚀 IRO AI 모듈 자동 생성...")

# 1. 신경망 모듈
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
        return np.maximum(0, x)
    
    def softmax(self, x):
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
        
        # 그래디언트 계산
        dz2 = y_pred - y_true
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * (self.z1 > 0)
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
        """신경망 확장"""
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
        
        self.W1, self.b1, self.W2 = new_W1, new_b1, new_W2
        
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
        return np.argmax(self.forward(X), axis=1)
    
    def get_brain_status(self):
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
        print(f"💾 신경망 저장: {filepath}")
    
    @classmethod
    def load(cls, filepath):
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
            print(f"📂 신경망 로드: {nn.hidden_size}개 뉴런")
            return nn
        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            return None
'''

# 2. 특징 추출기
feature_extractor_code = '''"""
IRO 특화 특징 추출기
"""

import numpy as np

class IRORobotFeatureExtractor:
    def __init__(self):
        self.tech_keywords = ['아두이노', 'arduino', '센서', '모터', '코딩', 'c++']
        self.iro_keywords = ['iro', '로봇', '대회', '우주', '미션']
        self.creative_keywords = ['아이디어', '디자인', '창의', '설계']
        print("🔍 특징 추출기 초기화 완료")
    
    def extract_features(self, text):
        """텍스트를 10차원 벡터로 변환"""
        if not text:
            return np.zeros((1, 10))
        
        features = []
        text_lower = text.lower()
        words = text.split()
        
        # 1-2. 길이 특징
        features.append(min(len(text) / 100.0, 1.0))
        features.append(min(len(words) / 30.0, 1.0))
        
        # 3. 질문 여부
        features.append(1.0 if '?' in text or '어떻게' in text else 0.0)
        
        # 4-6. 키워드 매칭
        for keywords in [self.tech_keywords, self.iro_keywords, self.creative_keywords]:
            score = sum(1 for k in keywords if k in text_lower)
            features.append(min(score / max(len(keywords), 1), 1.0))
        
        # 7. 명령어
        commands = ['해줘', '알려줘', '설명해']
        features.append(1.0 if any(c in text for c in commands) else 0.0)
        
        # 8. 감정 표현
        emotions = ['!', 'ㅋ', 'ㅎ', '좋아']
        features.append(min(sum(1 for e in emotions if e in text) / 3.0, 1.0))
        
        # 9. 숫자 포함
        features.append(1.0 if any(c.isdigit() for c in text) else 0.0)
        
        # 10. 복잡도
        if words:
            avg_len = sum(len(w) for w in words) / len(words)
            features.append(min(avg_len / 8.0, 1.0))
        else:
            features.append(0.0)
        
        return np.array(features).reshape(1, -1)
'''

# 3. 데이터베이스
database_code = '''"""
지식 데이터베이스
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
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"📚 DB 로드: {len(data.get('conversations', []))}개 대화")
                return data
            except:
                print("⚠️ DB 손상, 새로 생성")
        
        print("📚 새 DB 생성")
        return {'conversations': [], 'feedback': []}
    
    def save(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_conversation(self, user_input, features, category, confidence, response=""):
        conv_id = len(self.data['conversations'])
        self.data['conversations'].append({
            'id': conv_id, 'timestamp': datetime.now().isoformat(),
            'user_input': user_input, 'features': features.flatten().tolist(),
            'predicted_category': int(category), 'confidence': float(confidence),
            'response': response, 'feedback_given': False
        })
        self.save()
        return conv_id
    
    def add_feedback(self, conv_id, correct_category, rating=5):
        if conv_id < len(self.data['conversations']):
            self.data['conversations'][conv_id]['feedback_given'] = True
            self.data['feedback'].append({
                'conversation_id': conv_id, 'correct_category': int(correct_category),
                'rating': int(rating), 'timestamp': datetime.now().isoformat()
            })
            self.save()
            return True
        return False
    
    def get_training_data(self):
        feedback_dict = {f['conversation_id']: f for f in self.data['feedback']}
        X_list, y_list = [], []
        
        for conv in self.data['conversations']:
            if conv['id'] in feedback_dict:
                X_list.append(conv['features'])
                y_list.append(feedback_dict[conv['id']]['correct_category'])
        
        if len(X_list) < 3:
            return None, None
        
        X = np.array(X_list)
        y = np.array(y_list)
        y_onehot = np.zeros((y.size, 3))
        y_onehot[np.arange(y.size), y] = 1
        return X, y_onehot
    
    def get_statistics(self):
        total = len(self.data['conversations'])
        feedback = len(self.data['feedback'])
        return {
            'total_conversations': total,
            'total_feedback': feedback,
            'feedback_rate': (feedback / max(total, 1)) * 100
        }
'''

# 파일 생성
create_file('backend/neural_network/growing_network.py', growing_network_code)
create_file('backend/neural_network/feature_extractor.py', feature_extractor_code)
create_file('backend/knowledge_base/database.py', database_code)

# __init__.py 파일들
init_files = [
    'backend/__init__.py',
    'backend/neural_network/__init__.py', 
    'backend/knowledge_base/__init__.py',
    'backend/api_integration/__init__.py'
]

for init_file in init_files:
    create_file(init_file, f'"""{os.path.dirname(init_file)} 패키지"""\n')

print("\n🎉 모든 모듈 생성 완료!")
print("📋 다음 단계:")
print("1. python tests/test_integration.py")
print("2. python backend/main.py")