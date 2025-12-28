"""
Alicia 압축 뉴런 시스템 - 지식의 압축 저장 및 연결
"""

import numpy as np
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

@dataclass
class CompressedNeuron:
    """압축된 지식 뉴런 - 개념 단위 저장"""
    
    neuron_id: int
    concept: str  # 핵심 개념 (예: "양자 중첩")
    essence: str  # 압축된 본질 (예: "0과 1이 동시 존재")
    topic: str    # 상위 주제
    
    # 연결 및 강도
    synapses: Dict[int, float] = field(default_factory=dict)  # {뉴런ID: 연결강도}
    activation_strength: float = 1.0  # 기억 강도 (사용할수록 강해짐)
    
    # 압축 정보
    source_count: int = 1  # 몇 개 정보가 압축되었는지
    compression_ratio: float = 1.0
    knowledge_vector: np.ndarray = field(default_factory=lambda: np.zeros(64))
    
    # 메타데이터
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_accessed: Optional[str] = None
    access_count: int = 0
    
    def activate(self):
        """뉴런 활성화 - 사용할 때마다 호출"""
        self.access_count += 1
        self.activation_strength = min(2.0, self.activation_strength + 0.1)
        self.last_accessed = datetime.now().isoformat()
    
    def connect_to(self, other_id: int, weight: float):
        """다른 뉴런과 시냅스 연결"""
        self.synapses[other_id] = max(0.0, min(1.0, weight))
    
    def decay(self):
        """시간에 따른 기억 감퇴 (망각 곡선)"""
        self.activation_strength *= 0.998
    
    def to_dict(self) -> Dict:
        """직렬화"""
        return {
            'neuron_id': self.neuron_id,
            'concept': self.concept,
            'essence': self.essence,
            'topic': self.topic,
            'synapses': self.synapses,
            'activation_strength': self.activation_strength,
            'source_count': self.source_count,
            'compression_ratio': self.compression_ratio,
            'knowledge_vector': self.knowledge_vector.tolist(),
            'created_at': self.created_at,
            'last_accessed': self.last_accessed,
            'access_count': self.access_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CompressedNeuron':
        """역직렬화"""
        neuron = cls(
            neuron_id=data['neuron_id'],
            concept=data['concept'],
            essence=data['essence'],
            topic=data['topic']
        )
        neuron.synapses = data.get('synapses', {})
        neuron.activation_strength = data.get('activation_strength', 1.0)
        neuron.source_count = data.get('source_count', 1)
        neuron.compression_ratio = data.get('compression_ratio', 1.0)
        neuron.knowledge_vector = np.array(data.get('knowledge_vector', np.zeros(64)))
        neuron.created_at = data.get('created_at', '')
        neuron.last_accessed = data.get('last_accessed')
        neuron.access_count = data.get('access_count', 0)
        return neuron
