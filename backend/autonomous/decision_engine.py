"""
자율 의사결정 엔진 - AI의 독립적 판단 시스템
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from enum import Enum

class AutonomyLevel(Enum):
    """자율성 레벨"""
    LEARNING = 1    # 학습 중 (외부 도움 많이 필요)
    GROWING = 2     # 성장 중 (선택적 외부 참고)
    MATURE = 3      # 성숙 (대부분 자체 판단)
    EXPERT = 4      # 전문가 (완전 독립적)

class AutonomousDecisionEngine:
    """독립적 의사결정 시스템"""
    
    def __init__(self, neural_network, knowledge_brain, data_collector):
        self.neural_net = neural_network
        self.knowledge_brain = knowledge_brain
        self.data_collector = data_collector
        
        # 자율성 상태
        self.autonomy_level = AutonomyLevel.LEARNING
        self.confidence_history = []
        self.decision_count = 0
        self.successful_autonomous_decisions = 0
        
        # 학습된 주제별 전문성
        self.topic_expertise = {}
        
        # 개성/성격 파라미터
        self.personality = {
            'curiosity': 0.8,      # 새로운 정보 탐색 욕구
            'skepticism': 0.6,     # 외부 정보에 대한 회의적 태도
            'confidence_threshold': 0.7,  # 독립 판단 임계값
            'learning_eagerness': 0.9     # 학습 적극성
        }
    
    def make_decision(self, user_input: str, context: Dict) -> Dict:
        """핵심 의사결정 메서드"""
        self.decision_count += 1
        
        # 1. 현재 상황 분석
        situation_analysis = self._analyze_situation(user_input, context)
        
        # 2. 행동 결정
        action_plan = self._decide_action(situation_analysis)
        
        # 3. 행동 실행
        result = self._execute_action(action_plan, user_input)
        
        # 4. 자율성 업데이트
        self._update_autonomy(result)
        
        return result
    
    def _analyze_situation(self, user_input: str, context: Dict) -> Dict:
        """상황 분석"""
        # 기존 지식 확인
        related_neurons = self.knowledge_brain.query_knowledge(user_input, top_k=5)
        knowledge_coverage = sum(score for _, score in related_neurons) / 5 if related_neurons else 0.0
        
        # 신경망 확신도
        neural_confidence = context.get('confidence', 0.0)
        
        # 주제별 전문성 확인
        topic_expertise = self._assess_topic_expertise(user_input)
        
        # 종합 분석
        overall_confidence = (
            knowledge_coverage * 0.4 +
            neural_confidence * 0.3 +
            topic_expertise * 0.3
        )
        
        return {
            'knowledge_coverage': knowledge_coverage,
            'neural_confidence': neural_confidence,
            'topic_expertise': topic_expertise,
            'overall_confidence': overall_confidence,
            'related_neurons': related_neurons
        }
    
    def _decide_action(self, analysis: Dict) -> Dict:
        """행동 결정"""
        confidence = analysis['overall_confidence']
        
        # 개성 반영
        adjusted_threshold = (
            self.personality['confidence_threshold'] * 
            (1 - self.personality['curiosity'] * 0.2)
        )
        
        if confidence > adjusted_threshold:
            return {
                'type': 'AUTONOMOUS_RESPONSE',
                'reason': f'충분한 내부 지식 (확신도: {confidence:.2f})',
                'use_external_ai': False
            }
        elif confidence > 0.4:
            return {
                'type': 'SEARCH_AND_SYNTHESIZE',
                'reason': f'추가 정보 수집 후 독립 판단 (확신도: {confidence:.2f})',
                'use_external_ai': False,
                'search_depth': 'moderate'
            }
        elif confidence > 0.2:
            return {
                'type': 'COLLABORATIVE_DECISION',
                'reason': f'외부 AI와 협업 필요 (확신도: {confidence:.2f})',
                'use_external_ai': True,
                'trust_level': 0.5
            }
        else:
            return {
                'type': 'LEARN_AND_GROW',
                'reason': f'학습이 필요한 새로운 영역 (확신도: {confidence:.2f})',
                'use_external_ai': True,
                'search_depth': 'deep'
            }
    
    def _execute_action(self, action_plan: Dict, user_input: str) -> Dict:
        """행동 실행"""
        action_type = action_plan['type']
        
        if action_type == 'AUTONOMOUS_RESPONSE':
            return self._generate_autonomous_response(user_input)
        
        elif action_type == 'SEARCH_AND_SYNTHESIZE':
            return self._search_and_synthesize(user_input, action_plan['search_depth'])
        
        elif action_type == 'COLLABORATIVE_DECISION':
            return self._collaborative_decision(user_input, action_plan['trust_level'])
        
        elif action_type == 'LEARN_AND_GROW':
            return self._learn_and_grow(user_input, action_plan['search_depth'])
        
        else:
            return {'error': 'Unknown action type'}
    
    def _generate_autonomous_response(self, user_input: str) -> Dict:
        """완전 자율 응답 생성"""
        print("🤖 [완전 자율 모드] 내 지식만으로 응답 생성")
        
        # 관련 뉴런 수집
        related_neurons = self.knowledge_brain.query_knowledge(user_input, top_k=5)
        
        if not related_neurons:
            response = f"'{user_input}'에 대한 지식이 아직 부족합니다. 학습하겠습니다."
        else:
            # 지식 통합 및 응답 생성
            knowledge_pieces = []
            for neuron, score in related_neurons:
                # 뉴런 활성화
                neuron.activate()
                
                # 핵심 내용 추출
                content_summary = self._extract_key_points(neuron.content)
                knowledge_pieces.append(f"[신뢰도 {score:.2f}] {content_summary}")
            
            # 자체 추론으로 응답 구성
            response = self._synthesize_knowledge(knowledge_pieces, user_input)
        
        self.successful_autonomous_decisions += 1
        
        return {
            'response': response,
            'mode': 'fully_autonomous',
            'neurons_used': len(related_neurons),
            'autonomy_level': self.autonomy_level.name,
            'confidence': 0.9
        }
    
    def _search_and_synthesize(self, user_input: str, depth: str) -> Dict:
        """검색 후 독립적 종합"""
        print(f"🔍 [검색 후 독립 판단] {depth} 수준으로 정보 수집")
        
        # 자율 데이터 수집
        search_result = self.data_collector.autonomous_search(user_input, depth)
        
        # 수집된 정보를 즉시 학습
        new_neurons = []
        for item in search_result['processed_data'][:3]:  # 상위 3개만
            neuron = self.knowledge_brain.create_neuron(
                content=f"[자율 수집 - {item['source']}] {item['title']}: {item['content']}",
                topic=user_input,
                source=f"Autonomous_{item['source']}"
            )
            new_neurons.append(neuron.id)
        
        # 새로 학습한 내용으로 응답 생성
        response = self._generate_autonomous_response(user_input)
        response.update({
            'mode': 'search_and_synthesize',
            'new_neurons_created': len(new_neurons),
            'search_quality': search_result['quality_score']
        })
        
        return response
    
    def _collaborative_decision(self, user_input: str, trust_level: float) -> Dict:
        """외부 AI와 협업 (의식 시스템 통해 페르소나 주입)"""
        return {
            'mode': 'collaborative',
            'use_external_ai': True,
            'trust_level': trust_level
        }
    
    def _learn_and_grow(self, user_input: str, depth: str) -> Dict:
        """학습 후 성장"""
        return self._search_and_synthesize(user_input, depth)
    
    def _synthesize_knowledge(self, knowledge_pieces: List[str], query: str) -> str:
        """지식 조각들을 독립적으로 종합"""
        if not knowledge_pieces:
            return "관련 정보를 찾을 수 없습니다."
        
        # 간단한 템플릿 기반 응답 생성
        intro = "제가 학습한 내용을 바탕으로 말씀드리면,"
        
        main_content = "\n".join([f"• {piece}" for piece in knowledge_pieces[:3]])
        
        conclusion = "이상이 현재 제가 보유한 지식입니다."
        
        return f"{intro}\n\n{main_content}\n\n{conclusion}"
    
    def _extract_key_points(self, content: str) -> str:
        """내용에서 핵심 포인트 추출"""
        sentences = content.split('.')
        # 가장 긴 문장을 핵심으로 가정 (간단한 휴리스틱)
        if sentences:
            key_sentence = max(sentences, key=len).strip()
            return key_sentence[:200] + "..." if len(key_sentence) > 200 else key_sentence
        return content[:200] + "..."
    
    def _assess_topic_expertise(self, query: str) -> float:
        """주제별 전문성 평가"""
        # 간단한 키워드 매칭으로 전문성 평가
        for topic, expertise in self.topic_expertise.items():
            if topic.lower() in query.lower():
                return expertise
        return 0.0
    
    def _update_autonomy(self, result: Dict):
        """자율성 레벨 업데이트"""
        # 성공적인 자율 결정 비율 계산
        if result.get('mode') in ['fully_autonomous', 'search_and_synthesize']:
            success_rate = self.successful_autonomous_decisions / self.decision_count
            
            # 자율성 레벨 업데이트
            if success_rate > 0.8 and self.decision_count > 20:
                if self.autonomy_level.value < 4:
                    self.autonomy_level = AutonomyLevel(self.autonomy_level.value + 1)
                    print(f"🎉 자율성 레벨 상승: {self.autonomy_level.name}")
        
        # 확신도 이력 업데이트
        self.confidence_history.append(result.get('confidence', 0.0))
        if len(self.confidence_history) > 100:
            self.confidence_history.pop(0)
