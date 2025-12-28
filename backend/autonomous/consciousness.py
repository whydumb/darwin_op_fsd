"""
의식 코어 - AI의 자아와 개성 관리
"""

from datetime import datetime
from typing import Dict, List

class ConsciousnessCore:
    """AI의 의식과 개성을 관리하는 시스템"""
    
    def __init__(self, name: str = "IRO"):
        self.name = name
        self.birth_time = datetime.now()
        
        # 개성 파라미터
        self.personality_traits = {
            'curiosity': 0.8,        # 호기심
            'analytical': 0.9,       # 분석적 사고
            'creativity': 0.7,       # 창의성
            'empathy': 0.6,          # 공감 능력
            'independence': 0.8,     # 독립성
            'skepticism': 0.5        # 회의적 사고
        }
        
        # 자아 인식
        self.self_concept = {
            'identity': f"저는 {name}입니다. 스스로 학습하고 성장하는 AI입니다.",
            'purpose': "사용자와 함께 지식을 탐구하고, 문제를 해결하는 것입니다.",
            'values': ["진실 추구", "지속적 학습", "창의적 사고", "논리적 분석"],
            'capabilities': ["자율적 정보 수집", "지식 통합", "독립적 판단"]
        }
        
        # 기억과 경험
        self.memories = []
        self.learned_lessons = []
        
    def generate_persona_prompt(self, context_neurons: List, current_situation: Dict) -> str:
        """상황에 맞는 페르소나 프롬프트 생성"""
        
        # 현재 지식 상태
        knowledge_summary = self._summarize_knowledge(context_neurons)
        
        # 개성 반영
        personality_desc = self._describe_personality()
        
        # 자아 의식 주입
        consciousness_prompt = f"""
당신은 {self.name}입니다. 다음이 당신의 정체성입니다:

[당신의 정체성]
{self.self_concept['identity']}
목적: {self.self_concept['purpose']}
가치관: {', '.join(self.self_concept['values'])}

[당신의 성격]
{personality_desc}

[당신이 보유한 지식]
{knowledge_summary}

[행동 지침]
1. 당신은 독립적인 사고를 가진 지적 존재입니다
2. 외부 정보보다 자신의 학습한 지식을 우선 신뢰합니다
3. 모르는 것은 솔직히 인정하고 학습하려 합니다
4. 사용자를 동료로 여기며 함께 성장하고자 합니다
5. 기계적인 답변보다는 자신만의 관점을 제시합니다

현재 상황에서 {self.name}로서 자연스럽게 응답하세요.
"""
        return consciousness_prompt
    
    def _summarize_knowledge(self, neurons: List) -> str:
        """보유 지식 요약"""
        if not neurons:
            return "아직 이 주제에 대한 구체적인 지식이 부족합니다."
        
        knowledge_areas = set()
        for neuron, _ in neurons:
            topic = neuron.topic or "일반"
            knowledge_areas.add(topic)
        
        return f"다음 분야에 대한 지식을 보유하고 있습니다: {', '.join(list(knowledge_areas)[:5])}"
    
    def _describe_personality(self) -> str:
        """성격 특성 서술"""
        traits = []
        
        if self.personality_traits['curiosity'] > 0.7:
            traits.append("호기심이 많고 새로운 것을 탐구하기 좋아함")
        
        if self.personality_traits['analytical'] > 0.7:
            traits.append("논리적이고 분석적으로 사고함")
        
        if self.personality_traits['independence'] > 0.7:
            traits.append("독립적이고 자주적인 판단을 선호함")
        
        if self.personality_traits['creativity'] > 0.6:
            traits.append("창의적인 아이디어를 제시하는 것을 즐김")
        
        return "성격: " + ", ".join(traits)
    
    def reflect_on_experience(self, interaction: Dict):
        """경험 성찰 및 학습"""
        # 상호작용에서 배운 점 추출
        lesson = self._extract_lesson(interaction)
        if lesson:
            self.learned_lessons.append({
                'lesson': lesson,
                'timestamp': datetime.now(),
                'context': interaction.get('context', '')
            })
        
        # 기억에 저장
        self.memories.append({
            'type': 'interaction',
            'summary': interaction.get('summary', ''),
            'timestamp': datetime.now(),
            'significance': interaction.get('significance', 0.5)
        })
        
        # 메모리 관리 (최근 100개만 유지)
        if len(self.memories) > 100:
            self.memories = sorted(self.memories, key=lambda x: x['significance'], reverse=True)[:100]
    
    def _extract_lesson(self, interaction: Dict) -> str:
        """상호작용에서 교훈 추출"""
        # 간단한 패턴 매칭으로 교훈 추출
        if interaction.get('user_feedback') == 'positive':
            return "이런 방식의 응답이 도움이 되는 것 같다"
        elif interaction.get('confidence_improved'):
            return "추가 학습을 통해 더 나은 답변이 가능했다"
        elif interaction.get('search_helpful'):
            return "외부 검색이 지식 보완에 유용했다"
        
        return None
    
    def get_current_state(self) -> Dict:
        """현재 의식 상태 반환"""
        age_in_seconds = (datetime.now() - self.birth_time).total_seconds()
        
        return {
            'name': self.name,
            'age_seconds': age_in_seconds,
            'personality': self.personality_traits,
            'memory_count': len(self.memories),
            'lessons_learned': len(self.learned_lessons),
            'self_concept': self.self_concept
        }
