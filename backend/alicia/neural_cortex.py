"""
Alicia의 대뇌피질 - 연상 기억 네트워크
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, deque
import os
from .compressed_neuron import CompressedNeuron

class NeuralCortex:
    """Alicia의 뇌 - 압축 뉴런 네트워크 관리"""
    
    def __init__(self, storage_path: str = "data/alicia/cortex.json"):
        self.storage_path = storage_path
        self.neurons: Dict[int, CompressedNeuron] = {}
        self.concept_index: Dict[str, int] = {}  # {개념: 뉴런ID}
        self.topic_clusters: Dict[str, Set[int]] = defaultdict(set)
        self.next_id = 1
        
        self._ensure_directory()
        self._load_cortex()
    
    def _ensure_directory(self):
        """저장 디렉토리 생성"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    def learn_concept(self, concept: str, essence: str, topic: str, 
                     related_concepts: List[str] = None) -> CompressedNeuron:
        """새로운 개념 학습 또는 기존 개념 강화"""
        concept_key = concept.lower().strip()
        
        if concept_key in self.concept_index:
            # 기존 개념 강화
            neuron_id = self.concept_index[concept_key]
            neuron = self.neurons[neuron_id]
            neuron.activate()
            
            # 더 나은 설명이면 업데이트
            if len(essence) > len(neuron.essence) * 0.8 and len(essence) < len(neuron.essence) * 1.5:
                neuron.essence = essence
            
            print(f"🧠 [기억 강화] '{concept}' 개념이 더 선명해졌습니다.")
            return neuron
        else:
            # 새 뉴런 생성
            neuron = CompressedNeuron(
                neuron_id=self.next_id,
                concept=concept,
                essence=essence,
                topic=topic,
                knowledge_vector=self._create_knowledge_vector(essence)
            )
            
            self.neurons[self.next_id] = neuron
            self.concept_index[concept_key] = self.next_id
            self.topic_clusters[topic].add(self.next_id)
            self.next_id += 1
            
            print(f"✨ [새 개념] '{concept}' 뉴런 생성됨 (ID: {neuron.neuron_id})")
            
            # 연관 개념과 연결
            if related_concepts:
                self._create_synapses(neuron.neuron_id, related_concepts)
            
            return neuron
    
    def _create_knowledge_vector(self, text: str) -> np.ndarray:
        """텍스트를 64차원 지식 벡터로 변환"""
        words = text.lower().split()
        vector = np.zeros(64)
        
        for word in words:
            # 단어를 해시하여 차원에 매핑
            hash_val = hash(word) % 64
            vector[hash_val] += 1
        
        # 정규화
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def _create_synapses(self, neuron_id: int, related_concepts: List[str]):
        """관련 개념들과 시냅스 연결"""
        for concept in related_concepts:
            concept_key = concept.lower().strip()
            if concept_key in self.concept_index:
                target_id = self.concept_index[concept_key]
                
                # 양방향 연결 (시냅스 형성)
                self.neurons[neuron_id].connect_to(target_id, 0.6)
                self.neurons[target_id].connect_to(neuron_id, 0.6)
                
                print(f"   🔗 시냅스 연결: {self.neurons[neuron_id].concept} <-> {self.neurons[target_id].concept}")
    
    def think_offline(self, query: str, max_depth: int = 2) -> Tuple[List[CompressedNeuron], List[str]]:
        """인터넷 없이 연상 사고 (활성화 확산)"""
        print(f"🤔 [오프라인 사고] '{query}'에 대해 생각 중...")
        
        # 1. 쿼리와 관련된 시작 뉴런들 찾기
        start_neurons = self._find_relevant_neurons(query)
        if not start_neurons:
            return [], ["관련된 기억이 없어요..."]
        
        # 2. 활성화 확산 (Spreading Activation)
        activated = set()
        thought_process = []
        queue = deque([(nid, 0) for nid, _ in start_neurons[:3]])
        
        while queue:
            neuron_id, depth = queue.popleft()
            
            if neuron_id in activated or depth > max_depth:
                continue
            
            activated.add(neuron_id)
            neuron = self.neurons[neuron_id]
            neuron.activate()
            
            thought_process.append(f"'{neuron.concept}' 떠올림: {neuron.essence}")
            
            # 연결된 뉴런들 탐색
            if depth < max_depth:
                sorted_synapses = sorted(neuron.synapses.items(), 
                                       key=lambda x: x[1], reverse=True)
                for connected_id, weight in sorted_synapses[:2]:  # 강한 연결 2개
                    if connected_id in self.neurons and weight > 0.3:
                        queue.append((connected_id, depth + 1))
                        if connected_id not in activated:
                            connected = self.neurons[connected_id]
                            thought_process.append(f"  → '{connected.concept}' 연상됨")
        
        activated_neurons = [self.neurons[nid] for nid in activated]
        print(f"   💡 {len(activated_neurons)}개 개념 활성화됨")
        
        return activated_neurons, thought_process
    
    def _find_relevant_neurons(self, query: str) -> List[Tuple[int, float]]:
        """쿼리와 관련된 뉴런들 찾기"""
        query_vector = self._create_knowledge_vector(query)
        scores = []
        
        for neuron_id, neuron in self.neurons.items():
            # 키워드 매칭
            keyword_score = 0.0
            query_words = set(query.lower().split())
            concept_words = set(neuron.concept.lower().split())
            essence_words = set(neuron.essence.lower().split())
            
            # Jaccard 유사도
            if query_words & concept_words:
                keyword_score += 0.8
            if query_words & essence_words:
                keyword_score += 0.6
            
            # 벡터 유사도
            vector_score = np.dot(query_vector, neuron.knowledge_vector)
            
            total_score = keyword_score + vector_score
            if total_score > 0.2:
                scores.append((neuron_id, total_score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
    
    def compress_similar_neurons(self, similarity_threshold: float = 0.8):
        """유사한 뉴런들을 압축하여 메모리 절약"""
        print("🗜️ [뉴런 압축] 유사한 기억들을 통합 중...")
        
        compressed_count = 0
        processed = set()
        
        for neuron_id, neuron in list(self.neurons.items()):
            if neuron_id in processed:
                continue
            
            # 유사한 뉴런들 찾기
            similar_ids = []
            for other_id, other in self.neurons.items():
                if other_id != neuron_id and other_id not in processed:
                    similarity = self._calculate_similarity(neuron, other)
                    if similarity >= similarity_threshold:
                        similar_ids.append(other_id)
            
            if similar_ids:
                # 유사한 뉴런들과 병합
                self._merge_neurons(neuron_id, similar_ids)
                processed.update(similar_ids)
                compressed_count += len(similar_ids)
        
        print(f"   ✅ {compressed_count}개 뉴런 압축 완료")
        self._save_cortex()
    
    def _calculate_similarity(self, neuron1: CompressedNeuron, neuron2: CompressedNeuron) -> float:
        """두 뉴런의 유사도 계산"""
        # 개념 유사도
        concept_words1 = set(neuron1.concept.lower().split())
        concept_words2 = set(neuron2.concept.lower().split())
        concept_sim = len(concept_words1 & concept_words2) / len(concept_words1 | concept_words2) if concept_words1 | concept_words2 else 0
        
        # 벡터 유사도
        vector_sim = np.dot(neuron1.knowledge_vector, neuron2.knowledge_vector)
        
        # 주제 유사도
        topic_sim = 1.0 if neuron1.topic == neuron2.topic else 0.0
        
        return concept_sim * 0.5 + vector_sim * 0.3 + topic_sim * 0.2
    
    def _merge_neurons(self, main_id: int, merge_ids: List[int]):
        """여러 뉴런을 메인 뉴런으로 병합"""
        main_neuron = self.neurons[main_id]
        
        for merge_id in merge_ids:
            merge_neuron = self.neurons[merge_id]
            
            # 시냅스 연결 통합
            for syn_id, weight in merge_neuron.synapses.items():
                if syn_id in main_neuron.synapses:
                    main_neuron.synapses[syn_id] = max(main_neuron.synapses[syn_id], weight)
                else:
                    main_neuron.synapses[syn_id] = weight
            
            # 활성화 강도 통합
            main_neuron.activation_strength = max(main_neuron.activation_strength, merge_neuron.activation_strength)
            main_neuron.source_count += merge_neuron.source_count
            
            # 더 나은 설명으로 업데이트
            if len(merge_neuron.essence) > len(main_neuron.essence):
                main_neuron.essence = merge_neuron.essence
            
            # 병합된 뉴런 제거
            del self.neurons[merge_id]
            # 인덱스에서도 제거 (개념이 같다면)
            for concept, nid in list(self.concept_index.items()):
                if nid == merge_id:
                    self.concept_index[concept] = main_id
    
    def get_cortex_stats(self) -> Dict:
        """뇌 상태 통계"""
        total_synapses = sum(len(n.synapses) for n in self.neurons.values())
        total_memory = sum(len(str(n).encode('utf-8')) for n in self.neurons.values())
        
        return {
            'total_neurons': len(self.neurons),
            'total_synapses': total_synapses,
            'total_topics': len(self.topic_clusters),
            'memory_usage_bytes': total_memory,
            'avg_synapses_per_neuron': total_synapses / len(self.neurons) if self.neurons else 0,
            'compression_efficiency': sum(n.compression_ratio for n in self.neurons.values()) / len(self.neurons) if self.neurons else 1.0
        }
    
    def _save_cortex(self):
        """뇌 상태 저장"""
        data = {
            'neurons': {nid: neuron.to_dict() for nid, neuron in self.neurons.items()},
            'concept_index': self.concept_index,
            'topic_clusters': {topic: list(ids) for topic, ids in self.topic_clusters.items()},
            'next_id': self.next_id,
            'saved_at': datetime.now().isoformat()
        }
        
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_cortex(self):
        """저장된 뇌 상태 로드"""
        if not os.path.exists(self.storage_path):
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 뉴런 복원
            for nid_str, neuron_data in data.get('neurons', {}).items():
                neuron = CompressedNeuron.from_dict(neuron_data)
                self.neurons[int(nid_str)] = neuron
            
            self.concept_index = data.get('concept_index', {})
            
            # 토픽 클러스터 복원
            for topic, ids in data.get('topic_clusters', {}).items():
                self.topic_clusters[topic] = set(ids)
            
            self.next_id = data.get('next_id', 1)
            
            print(f"🧠 Alicia의 기억 복원: {len(self.neurons)}개 뉴런")
            
        except Exception as e:
            print(f"⚠️ 뇌 로드 실패: {e}")
