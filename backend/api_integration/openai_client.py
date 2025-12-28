"""
OpenAI API 클라이언트
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient:
    """OpenAI API를 사용한 응답 생성기"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY가 .env 파일에 올바르게 설정되지 않았습니다!")
        
        self.client = OpenAI(api_key=api_key)
        
        # 카테고리별 시스템 프롬프트
        self.system_prompts = {
            0: """너는 친근한 IRO 로봇 대회 선배야. 
            편하게 대화하듯이 격려해주고, 대회 준비에 대한 일반적인 조언을 해줘.
            친근하고 응원하는 톤으로 말해줘.""",
            
            1: """너는 IRO 로봇 대회 기술 전문 코치야.
            아두이노, 센서, 모터 제어 등 기술적 질문에 구체적으로 답변해.
            코드 예시를 포함하고, 초중고 학생 수준에 맞게 단계별로 설명해.
            실제 대회에서 구현 가능한 현실적인 해결책을 제시해.""",
            
            2: """너는 IRO 우주 로봇 미션 설계 멘토야.
            우주 환경을 고려한 창의적 아이디어를 제안하고,
            실제 구현 가능한 수준의 미션 설계를 도와줘.
            단계별 구현 계획도 함께 제시해."""
        }
    
    def generate_response(self, user_input, category, conversation_history=None):
        """카테고리에 맞는 응답 생성"""
        if conversation_history is None:
            conversation_history = []
        
        # 시스템 프롬프트 선택
        system_prompt = self.system_prompts.get(category, self.system_prompts[0])
        
        # 메시지 구성
        messages = [{"role": "system", "content": system_prompt}]
        
        # 최근 대화 기록 추가 (최대 10개)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
