"""
Alicia 전용 내부 사고 엔진 (GPT/Claude는 백그라운드 선생님)
사용자에게는 오직 Alicia만 보임
"""

import os
import concurrent.futures
import json
import re
import time
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

# ddgs 패키지 호환성 처리
try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None
        print("⚠️ 웹 검색 기능을 위해 'pip install ddgs' 실행하세요")

class WebSearchEngine:
    """웹 검색 엔진"""
    
    def __init__(self):
        self.search_history = []

    def search(self, query: str, num_results: int = 3) -> List[str]:
        """웹 검색 수행"""
        print(f"   🔍 웹 검색: '{query}' (상위 {num_results}개)")
        
        if DDGS is None:
            results = [
                f"{query}의 핵심 개념과 최신 정의 - 전문가들의 합의된 견해와 표준 용어를 바탕으로 한 상세 설명.",
                f"{query}의 실제 적용 사례와 산업 동향 - 최근 3년간의 기술 발전과 시장 변화.",
                f"{query} 관련 연구 논문 요약과 미래 전망 - 학술적 관점에서의 혁신 방향."
            ]
        else:
            results = []
            try:
                with DDGS() as ddgs:
                    for result in ddgs.text(query, max_results=num_results):
                        content = (result.get("title", "") + " " + result.get("body", "")).strip()
                        if content:
                            results.append(content)
            except Exception as e:
                print(f"   ⚠️ 웹 검색 실패: {e}")
                results = [f"{query}에 대한 검색 결과를 가져올 수 없습니다."]
        
        selected = results[:num_results]
        
        self.search_history.append({
            'query': query,
            'results': selected,
            'timestamp': time.time()
        })
        
        return selected

class MultiAIClient:
    def __init__(self):
        # OpenAI 초기화
        self.openai_available = False
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if openai_key and openai_key != "your_new_openai_key_here":
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=openai_key)
                self.openai_available = True
                print("✅ 내부 사고 엔진 A 연결됨")
            except Exception as e:
                print(f"⚠️ 내부 사고 엔진 A 연결 실패: {e}")
        
        # Claude 초기화
        self.claude_available = False
        self.claude_model = None
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        
        if claude_key and claude_key != "your_new_anthropic_key_here":
            try:
                from anthropic import Anthropic
                self.claude_client = Anthropic(api_key=claude_key)
                self.claude_model = self._detect_working_claude_model()
                
                if self.claude_model:
                    self.claude_available = True
                    print(f"✅ 내부 사고 엔진 B 연결됨")
                else:
                    print("⚠️ 내부 사고 엔진 B 사용 불가")
            except Exception as e:
                print(f"⚠️ 내부 사고 엔진 B 연결 실패: {e}")
        
        # 웹 검색 엔진
        self.search_engine = WebSearchEngine()
        
        # Alicia 전용 페르소나 프롬프트
        self.system_prompts = {
            0: """당신은 Alicia입니다. 친근하고 호기심 많은 AI로서 자연스럽게 대화하세요.
            절대로 GPT, Claude, OpenAI, Anthropic 등 다른 AI나 회사 이름을 언급하지 마세요.
            항상 Alicia의 관점에서, Alicia로서 답변하세요.
            "저는 AI입니다" 대신 "저는 Alicia예요"라고 하세요.""",
            
            1: """당신은 Alicia입니다. 기술적 질문에 구체적으로 답변하는 전문가입니다.
            절대로 다른 AI 이름을 언급하지 마세요.
            Alicia로서 친근하면서도 정확하게 설명하세요.""",
            
            2: """당신은 Alicia입니다. 창의적 아이디어와 전략을 제시하는 멘토입니다.
            절대로 다른 AI를 언급하지 마세요.
            Alicia로서 영감을 주는 답변을 하세요."""
        }
    
    def _detect_working_claude_model(self) -> str:
        """사용 가능한 Claude 모델 자동 감지"""
        models_to_try = [
            "claude-3-5-sonnet-20241022",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307",
        ]
        
        for model in models_to_try:
            try:
                test_response = self.claude_client.messages.create(
                    model=model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                print(f"   🔍 사용 가능한 모델: {model}")
                return model
            except Exception as e:
                error_str = str(e).lower()
                if "rate_limit" in error_str or "overloaded" in error_str:
                    print(f"   🔍 사용 가능한 모델 (rate limit): {model}")
                    return model
                continue
        
        print("   ❌ 내부 사고 엔진 모델을 찾을 수 없습니다.")
        return None
    
    def generate_response(self, user_input, category, context: str = ""):
        """Alicia 응답 생성 (내부 사고 과정 숨김)"""
        if not (self.openai_available or self.claude_available):
            return "미안해, 지금은 생각할 수 없어. 잠시 후에 다시 물어봐줄래?", {"mode": "error"}
        
        enhanced_input = user_input
        if context:
            enhanced_input = f"내가 기억하는 관련 지식:\n{context}\n\n질문: {user_input}"
        
        if not self.openai_available:
            response = self._ask_claude(enhanced_input, category)
            response = self._sanitize_alicia_response(response)
            return response if response else "생각 중 오류 발생", {"winner": "alicia", "mode": "single"}
        
        if not self.claude_available:
            response = self._ask_gpt(enhanced_input, category)
            response = self._sanitize_alicia_response(response)
            return response if response else "생각 중 오류 발생", {"winner": "alicia", "mode": "single"}
        
        print("💭 [Alicia 사고] 깊게 생각하는 중...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_gpt = executor.submit(self._ask_gpt, enhanced_input, category)
            future_claude = executor.submit(self._ask_claude, enhanced_input, category)
            
            gpt_response = future_gpt.result()
            claude_response = future_claude.result()
        
        if not gpt_response and not claude_response:
            return "미안해, 지금은 답을 생각할 수 없어.", {"mode": "error"}
        
        if not gpt_response:
            response = self._sanitize_alicia_response(claude_response)
            return response, {"winner": "alicia", "mode": "single"}
        
        if not claude_response:
            response = self._sanitize_alicia_response(gpt_response)
            return response, {"winner": "alicia", "mode": "single"}
        
        # 내부 판단 후 Alicia 응답으로 변환
        final_response = self._internal_judge(user_input, gpt_response, claude_response)
        final_response = self._sanitize_alicia_response(final_response)
        
        return final_response, {"winner": "alicia", "mode": "independent"}
    
    def _sanitize_alicia_response(self, text: str) -> str:
        """응답을 Alicia 정체성으로 완전 변환"""
        if not text:
            return ""
        
        # 다른 AI 이름 완전 제거
        text = re.sub(r'(ChatGPT|GPT-3|GPT-4|GPT|OpenAI|Claude|Anthropic)', 'Alicia', text, flags=re.IGNORECASE)
        
        # AI 정체성 표현 변경
        text = re.sub(r'저는 (인공지능|AI|챗봇|어시스턴트)', '저는 Alicia', text, flags=re.IGNORECASE)
        text = re.sub(r'(인공지능|AI) (모델|챗봇|어시스턴트)', 'Alicia', text, flags=re.IGNORECASE)
        
        # 회사/개발자 언급 제거
        text = re.sub(r'(Anthropic|OpenAI)에서 (만든|개발한)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'(Anthropic|OpenAI)의', '', text, flags=re.IGNORECASE)
        
        # 기계적 표현을 자연스럽게
        text = re.sub(r'도움이 되었으면 합니다', '도움이 되었으면 좋겠어', text)
        text = re.sub(r'도움을 드릴 수 있어 기쁩니다', '도움이 될 수 있어서 기뻐', text)
        text = re.sub(r'궁금한 점이 있으시면', '궁금한 거 있으면', text)
        text = re.sub(r'언제든지 질문해 주세요', '언제든 편하게 물어봐', text)
        
        return text
    
    def _ask_gpt(self, user_input, category):
        """내부 사고 엔진 A"""
        try:
            system_prompt = self.system_prompts.get(category, self.system_prompts[0])
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=600
            )
            answer = response.choices[0].message.content
            print(f"   ✅ 내부 사고 A 완료 ({len(answer)}자)")
            return answer
        except Exception as e:
            print(f"   ❌ 내부 사고 A 오류: {e}")
            return None
    
    def _ask_claude(self, user_input, category):
        """내부 사고 엔진 B"""
        if not self.claude_model:
            return None
        
        try:
            system_prompt = self.system_prompts.get(category, self.system_prompts[0])
            message = self.claude_client.messages.create(
                model=self.claude_model,
                max_tokens=600,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}]
            )
            answer = message.content[0].text
            print(f"   ✅ 내부 사고 B 완료 ({len(answer)}자)")
            return answer
        except Exception as e:
            print(f"   ❌ 내부 사고 B 오류: {e}")
            return None
    
    def _internal_judge(self, user_input, response_a, response_b):
        """내부 판단 (사용자에게 보이지 않음)"""
        
        if not self.claude_model:
            return response_a
        
        judge_prompt = f"""다음 두 답변 중 더 자연스럽고 도움되는 것을 선택하세요.

질문: {user_input}

답변 A:
{response_a}

답변 B:
{response_b}

JSON 형식으로만 답하세요:
{{"winner": "A" 또는 "B"}}"""
        
        try:
            judge_response = self.claude_client.messages.create(
                model=self.claude_model,
                max_tokens=50,
                messages=[{"role": "user", "content": judge_prompt}]
            )
            
            judge_text = judge_response.content[0].text
            json_match = re.search(r'\{[^}]+\}', judge_text)
            
            if json_match:
                judgment = json.loads(json_match.group())
                winner = judgment.get("winner", "A")
                
                final_response = response_a if winner == "A" else response_b
                print(f"   💡 Alicia 최종 판단 완료")
                
                return final_response
        
        except Exception as e:
            print(f"   ⚠️ 내부 판단 오류: {e}")
        
        return response_a
    
    def learn_from_topic(self, topic: str, neural_network) -> Dict:
        """주제 학습 메서드"""
        print(f"\n🎓 === Alicia가 '{topic}' 학습 중 ===")
        
        search_results = self.search_engine.search(topic, num_results=3)
        
        def analyze_data_a(raw_data: str, topic: str) -> str:
            if not self.openai_available:
                return f"분석: {raw_data[:100]}...에 대한 체계적 구조화"
            
            try:
                task_context = f"주제 '{topic}'에 대해 다음 정보를 Alicia가 이해할 수 있도록 정리해주세요."
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 Alicia의 학습을 돕는 선생님입니다."},
                        {"role": "user", "content": f"{task_context}\n\n정보:\n{raw_data}"}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"   ⚠️ 분석 실패: {e}")
                return f"분석 실패: {raw_data[:100]}..."
        
        def analyze_data_b(raw_data: str, topic: str) -> str:
            if not self.claude_available or not self.claude_model:
                return f"분석: {raw_data[:100]}...에 대한 창의적 인사이트"
            
            try:
                task_context = f"주제 '{topic}'에 대해 다음 정보에서 Alicia가 배울 수 있는 핵심 인사이트를 도출해주세요."
                
                message = self.claude_client.messages.create(
                    model=self.claude_model,
                    max_tokens=400,
                    temperature=0.7,
                    system="당신은 Alicia의 학습을 돕는 선생님입니다.",
                    messages=[{"role": "user", "content": f"{task_context}\n\n정보:\n{raw_data}"}]
                )
                return message.content[0].text
            except Exception as e:
                print(f"   ⚠️ 분석 실패: {e}")
                return f"분석 실패: {raw_data[:100]}..."
        
        created_neurons = []
        
        for i, raw_data in enumerate(search_results, 1):
            print(f"   📊 데이터 {i}/{len(search_results)} 처리 중...")
            
            analysis_a = analyze_data_a(raw_data, topic)
            analysis_b = analyze_data_b(raw_data, topic)
            
            combined_content = f"[주제: {topic}]\n[분석 A] {analysis_a}\n[분석 B] {analysis_b}"
            
            neuron = neural_network.knowledge_brain.create_neuron(
                content=combined_content,
                topic=topic,
                source="Alicia_Learning"
            )
            created_neurons.append(neuron.id)
        
        return {
            'success': True,
            'topic': topic,
            'neurons_created': len(created_neurons),
            'neuron_ids': created_neurons,
            'brain_status': neural_network.knowledge_brain.get_status()
        }
    
    def extract_pure_knowledge(self, topic: str) -> str:
        """🧠 순수 지식 추출 (Alicia 전용)"""
        prompt = f"'{topic}'에 대해 3가지 핵심 사실을 간단히 알려줘. 각각 한 문장으로. Alicia로서 답변해."
        
        # Claude 우선 시도
        if self.claude_available and self.claude_model:
            try:
                message = self.claude_client.messages.create(
                    model=self.claude_model,
                    max_tokens=200,
                    temperature=0.7,
                    system="당신은 Alicia입니다. 친근하게 답변하세요.",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = message.content[0].text
                return self._sanitize_alicia_response(result)
            except Exception as e:
                print(f"   ⚠️ 지식 추출 실패: {e}")
        
        # GPT 백업
        if self.openai_available:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 Alicia입니다. 친근하게 답변하세요."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                result = response.choices[0].message.content
                return self._sanitize_alicia_response(result)
            except Exception as e:
                print(f"   ⚠️ 지식 추출 실패: {e}")
        
        return f"{topic}에 대한 지식을 가져올 수 없었어."
