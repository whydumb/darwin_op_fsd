"""
자가 성장형 신경망 + 지식 뉴런 브레인 + 오프라인 사고 능력
"""

import numpy as np
import pickle
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any

class KnowledgeNeuron:
    """개별 지식을 저장하는 뉴런"""
    
    def __init__(self, neuron_id: int, content: str, topic: str, 
                 source: str = "Hybrid", confidence: float = 0.8):
        self.id = neuron_id
        self.content = content
        self.topic = topic
        self.source = source
        self.confidence = confidence
        self.connections: Dict[str, float] = {}
        self.activation_count = 0
        self.created_at = datetime.now().isoformat()
        self.last_accessed: Optional[str] = None

    def connect_to(self, other_id: int, weight: float):
        """다른 뉴런과 연결 생성"""
        self.connections[str(other_id)] = max(0.0, min(1.0, weight))

    def activate(self):
        """뉴런 활성화"""
        self.activation_count += 1
        self.last_accessed = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'id': self.id, 'content': self.content, 'topic': self.topic,
            'source': self.source, 'confidence': self.confidence,
            'connections': self.connections, 'activation_count': self.activation_count,
            'created_at': self.created_at, 'last_accessed': self.last_accessed
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeNeuron':
        neuron = cls(
            neuron_id=data['id'],
            content=data['content'],
            topic=data['topic'],
            source=data.get('source', 'Hybrid'),
            confidence=data.get('confidence', 0.8)
        )
        neuron.connections = data.get('connections', {})
        neuron.activation_count = data.get('activation_count', 0)
        neuron.created_at = data.get('created_at', datetime.now().isoformat())
        neuron.last_accessed = data.get('last_accessed')
        return neuron

class NeuralBrain:
    """지식 뉴런 네트워크 - 오프라인 사고 가능"""
    
    def __init__(self, storage_path: str = "data/knowledge/neural_brain.json"):
        self.storage_path = storage_path
        self.neurons: Dict[int, KnowledgeNeuron] = {}
        self.next_id = 1
        self.learning_mode = False
        self.growth_events = 0
        self.topics_learned = set()
        
        self._ensure_directory()
        self._load_neurons()

    def _ensure_directory(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def _load_neurons(self):
        """저장된 뉴런들 로드"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for neuron_data in data.get('neurons', []):
                    neuron = KnowledgeNeuron.from_dict(neuron_data)
                    self.neurons[neuron.id] = neuron
                if self.neurons:
                    self.next_id = max(self.neurons.keys()) + 1
                self.growth_events = data.get('growth_events', 0)
                self.topics_learned = set(data.get('topics_learned', []))
                print(f"🧠 지식 뉴런 로드: {len(self.neurons)}개")
        except Exception as e:
            print(f"⚠️ 지식 뉴런 로드 실패: {e}")

    def _save_neurons(self):
        """뉴런들을 파일에 저장"""
        try:
            data = {
                'neurons': [n.to_dict() for n in self.neurons.values()],
                'growth_events': self.growth_events,
                'topics_learned': list(self.topics_learned),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 뉴런 저장 실패: {e}")

    def toggle_learning_mode(self, enabled: bool):
        """학습 모드 ON/OFF"""
        self.learning_mode = enabled
        print(f"🎯 학습 모드: {'ON' if enabled else 'OFF'}")

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """텍스트 유사도 계산 (Jaccard Index)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2: return 0.0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0

    def create_neuron(self, content: str, topic: str, source: str = "Hybrid", confidence: float = 0.8) -> KnowledgeNeuron:
        """새로운 지식 뉴런 생성"""
        neuron_id = self.next_id
        self.next_id += 1
        neuron = KnowledgeNeuron(neuron_id, content, topic, source, confidence)
        
        # 기존 뉴런들과 연결 생성
        for existing_neuron in self.neurons.values():
            content_sim = self.calculate_similarity(content, existing_neuron.content)
            topic_sim = 0.5 if topic == existing_neuron.topic else 0.0
            total_sim = (content_sim * 0.7 + topic_sim * 0.3)
            if total_sim > 0.2:
                neuron.connect_to(existing_neuron.id, total_sim)
                existing_neuron.connect_to(neuron_id, total_sim)
        
        self.neurons[neuron_id] = neuron
        self.growth_events += 1
        self.topics_learned.add(topic)
        self._save_neurons()
        print(f"   🌱 뉴런 생성: ID-{neuron_id} (연결: {len(neuron.connections)}개)")
        return neuron

    def query_knowledge(self, query: str, top_k: int = 3) -> List[Tuple[KnowledgeNeuron, float]]:
        """관련 지식 검색"""
        scored_neurons = []
        for neuron in self.neurons.values():
            content_sim = self.calculate_similarity(query, neuron.content)
            topic_sim = self.calculate_similarity(query, neuron.topic)
            total_score = content_sim * 0.7 + topic_sim * 0.3
            
            if total_score > 0.15:
                neuron.activate()
                scored_neurons.append((neuron, total_score))
        
        scored_neurons.sort(key=lambda x: x[1], reverse=True)
        return scored_neurons[:top_k]

    def get_direct_answer(self, query: str) -> Tuple[Optional[str], float]:
        """🧠 Alicia 오프라인 사고: 뇌에서 직접 답변 찾기"""
        best_matches = self.query_knowledge(query, top_k=3)
        
        if not best_matches:
            return None, 0.0
        
        # 가장 유사도 높은 뉴런 선택
        best_neuron, similarity = best_matches[0]
        
        # 신뢰도 임계값 (0.3 이상이면 직접 답변)
        if similarity > 0.3:
            print(f"🧠 [Alicia 독립 사고] 내 기억에서 답을 찾았어! (정확도: {similarity:.2f})")
            
            # 여러 관련 기억 조합
            combined_knowledge = []
            for neuron, score in best_matches[:2]:
                combined_knowledge.append(f"• {neuron.content[:200]}...")
            
            response = (
                f"내가 기억하기로는:\n" + 
                "\n".join(combined_knowledge) + 
                f"\n\n이건 내가 직접 공부해서 아는 내용이야! (신뢰도: {similarity:.1%})"
            )
            
            return response, similarity
        
        return None, similarity

    def get_status(self) -> Dict:
        """브레인 상태"""
        total_connections = sum(len(n.connections) for n in self.neurons.values())
        return {
            'total_neurons': len(self.neurons),
            'total_connections': total_connections,
            'growth_events': self.growth_events,
            'topics_learned': len(self.topics_learned),
            'learning_mode': self.learning_mode,
            'avg_connections': total_connections / len(self.neurons) if self.neurons else 0
        }

class SelfGrowingNeuralNetwork:
    """자가 성장 분류 신경망 + 지식 브레인"""
    
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
        
        self.training_history = {
            'loss': [], 'accuracy': [], 'epochs': 0,
            'growth_events': [], 'total_conversations': 0, 'instant_growths': 0
        }
        
        self.knowledge_brain = NeuralBrain()
        print(f"🤖 신경망 초기화: 분류 {hidden_size}개 + 지식 {len(self.knowledge_brain.neurons)}개 뉴런")
    
    def relu(self, x): return np.maximum(0, x)
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    def check_instant_growth(self, features, confidence):
        """즉시 성장 필요성 확인"""
        should_grow = False
        reason = ""
        
        if confidence < 0.5:
            should_grow = True
            reason = f"매우 낮은 확신도 ({confidence*100:.1f}%)"
        elif confidence < 0.7:
            probs = self.forward(features)[0]
            entropy = -np.sum(probs * np.log(probs + 1e-10))
            if entropy > 0.85:
                should_grow = True
                reason = f"높은 불확실성 (엔트로피: {entropy:.2f})"
        
        if should_grow and self.hidden_size >= 100:
            return False, "최대 크기 도달"
        
        if should_grow:
            print(f"\n⚡ 즉시 성장 트리거: {reason}")
            self.grow_network(2)
            self.training_history['instant_growths'] += 1
            return True, reason
        return False, "성장 불필요"
    
    def grow_network(self, new_neurons=2):
        """신경망 확장"""
        print(f"🌱 신경망 성장: {self.hidden_size} → {self.hidden_size + new_neurons}개 뉴런")
        old_size = self.hidden_size
        self.hidden_size += new_neurons
        
        new_W1 = np.random.randn(self.input_size, self.hidden_size) * np.sqrt(2.0 / self.input_size)
        new_b1 = np.zeros((1, self.hidden_size))
        new_W2 = np.random.randn(self.hidden_size, self.output_size) * np.sqrt(2.0 / self.hidden_size)
        
        new_W1[:, :old_size] = self.W1
        new_b1[:, :old_size] = self.b1
        new_W2[:old_size, :] = self.W2
        
        self.W1, self.b1, self.W2 = new_W1, new_b1, new_W2
        self.training_history['growth_events'].append({
            'timestamp': datetime.now().isoformat(),
            'old_size': old_size, 'new_size': self.hidden_size,
            'added_neurons': new_neurons, 'trigger': 'instant_growth'
        })
        print("✅ 신경망 확장 완료! 🧠✨")
    
    def get_contextual_knowledge(self, query: str) -> str:
        """질문에 관련된 지식 뉴런 검색"""
        related_neurons = self.knowledge_brain.query_knowledge(query, top_k=3)
        if not related_neurons: return ""
        context_parts = []
        for neuron, score in related_neurons:
            context_parts.append(f"[관련도: {score:.2f}] {neuron.content[:200]}")
        return "📚 관련 기억:\n" + "\n".join(context_parts)
    
    def get_brain_status(self):
        """전체 뇌 상태"""
        base_status = {
            'neurons': self.hidden_size,
            'total_parameters': (self.input_size * self.hidden_size + self.hidden_size * self.output_size),
            'epochs_trained': self.training_history['epochs'],
            'growth_events': len(self.training_history['growth_events']),
            'instant_growths': self.training_history['instant_growths'],
            'conversations': self.training_history['total_conversations']
        }
        knowledge_status = self.knowledge_brain.get_status()
        base_status.update({
            'knowledge_neurons': knowledge_status['total_neurons'],
            'knowledge_connections': knowledge_status['total_connections'],
            'topics_learned': knowledge_status['topics_learned'],
            'learning_mode': knowledge_status['learning_mode']
        })
        return base_status
    
    def save(self, filepath):
        """모델 저장"""
        data = {
            'weights': {'W1': self.W1, 'b1': self.b1, 'W2': self.W2, 'b2': self.b2},
            'config': {'input_size': self.input_size, 'hidden_size': self.hidden_size, 
                       'output_size': self.output_size, 'learning_rate': self.learning_rate},
            'history': self.training_history,
            'metadata': {'saved_at': datetime.now().isoformat(), 'version': '6.0'}
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"💾 신경망 저장: {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """저장된 모델 로드"""
        if not os.path.exists(filepath): return None
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            nn = cls(**data['config'])
            weights = data['weights']
            nn.W1, nn.b1 = weights['W1'], weights['b1']
            nn.W2, nn.b2 = weights['W2'], weights['b2']
            nn.training_history = data['history']
            print(f"📂 신경망 로드: {nn.hidden_size}개 뉴런")
            return nn
        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            return None
