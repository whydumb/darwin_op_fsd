"""
지식 검증 엔진 - GPT+Claude 교차 검증 시스템
Wikipedia 등에서 수집한 정보의 신뢰성을 보장
"""

import json
import re
from typing import Dict, List, Optional, Tuple

class KnowledgeVerifier:
    """GPT와 Claude를 활용한 정보 검증 시스템"""
    
    def __init__(self, multi_ai_client):
        self.multi_ai_client = multi_ai_client
        
        # 검증 설정
        self.trust_threshold = 0.6  # 신뢰도 임계값
        self.verification_history = []
        
        # 검증 프롬프트 템플릿
        self.verification_prompts = {
            'gpt_primary': """당신은 엄격한 사실 확인 전문가입니다.
다음 정보를 검증하고 평가해주세요:

주제: {topic}
출처: {source}
내용: {content}

다음 기준으로 평가하세요:
1. 사실적 정확성 (0.0~1.0)
2. 출처 신뢰성 (0.0~1.0)
3. 편향 여부 탐지
4. 교육적 적합성 (IRO 로봇 대회 학생용)

반드시 JSON 형식으로만 답변하세요:
{{
  "factual_accuracy": 0.0-1.0,
  "source_reliability": 0.0-1.0,
  "bias_detected": true/false,
  "educational_value": 0.0-1.0,
  "trust_score": 0.0-1.0,
  "issues": ["문제점1", "문제점2"],
  "verified_content": "검증되고 정제된 내용",
  "reasoning": "판단 근거"
}}""",
            
            'claude_cross_check': """당신은 독립적인 검증 전문가입니다.
GPT가 1차 검증한 정보를 재검토해주세요:

원본 정보:
주제: {topic}
내용: {content}

GPT 검증 결과:
- 신뢰도: {gpt_score}
- 문제점: {gpt_issues}

독립적으로 재평가하고 JSON으로 답변하세요:
{{
  "agrees_with_gpt": true/false,
  "trust_score": 0.0-1.0,
  "additional_concerns": ["추가 우려사항"],
  "recommendation": "accept/reject/modify",
  "final_content": "최종 정제된 내용",
  "reasoning": "재검증 근거"
}}"""
        }
    
    def verify_information(self, raw_data: Dict, topic: str) -> Dict:
        """정보 검증 메인 프로세스"""
        print(f"🔍 [검증 시작] '{topic}' 정보 검증 중...")
        
        content = raw_data.get('content', '')[:1500]  # 길이 제한
        source = raw_data.get('source', 'unknown')
        title = raw_data.get('title', '')
        
        # 1단계: GPT 1차 검증
        gpt_result = self._gpt_verify(content, topic, source)
        
        # 2단계: Claude 교차 검증 (GPT 사용 가능한 경우에만)
        claude_result = None
        if gpt_result and gpt_result.get('trust_score', 0) > 0.5:
            claude_result = self._claude_cross_verify(
                content, topic, gpt_result
            )
        
        # 3단계: 최종 판정
        final_verdict = self._synthesize_results(
            gpt_result, claude_result, raw_data
        )
        
        # 검증 이력 저장
        self.verification_history.append({
            'topic': topic,
            'source': source,
            'title': title[:100],
            'verdict': final_verdict
        })
        
        return final_verdict
    
    def _gpt_verify(self, content: str, topic: str, source: str) -> Optional[Dict]:
        """GPT를 통한 1차 검증"""
        print("   🤖 [GPT 검증] 사실 확인 중...")
        
        if not self.multi_ai_client.openai_available:
            print("      ⚠️ GPT 사용 불가")
            return None
        
        try:
            prompt = self.verification_prompts['gpt_primary'].format(
                topic=topic, source=source, content=content
            )
            
            response = self.multi_ai_client.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 정보 검증 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            result_text = response.choices[0].message.content
            parsed_result = self._parse_json_response(result_text)
            
            if parsed_result:
                score = parsed_result.get('trust_score', 0.0)
                print(f"      ✅ GPT 신뢰도: {score*100:.1f}%")
                return parsed_result
            else:
                print("      ⚠️ GPT 응답 파싱 실패")
                return None
                
        except Exception as e:
            print(f"      ❌ GPT 검증 오류: {e}")
            return None
    
    def _claude_cross_verify(self, content: str, topic: str, 
                           gpt_result: Dict) -> Optional[Dict]:
        """Claude를 통한 교차 검증"""
        print("   🧠 [Claude 검증] 교차 확인 중...")
        
        if not self.multi_ai_client.claude_available:
            print("      ⚠️ Claude 사용 불가")
            return None
        
        try:
            prompt = self.verification_prompts['claude_cross_check'].format(
                topic=topic,
                content=content,
                gpt_score=f"{gpt_result.get('trust_score', 0)*100:.1f}%",
                gpt_issues=', '.join(gpt_result.get('issues', []))
            )
            
            message = self.multi_ai_client.claude_client.messages.create(
                model=self.multi_ai_client.claude_model,
                max_tokens=600,
                temperature=0.3,
                system="당신은 독립적인 사실 검증 전문가입니다.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = message.content[0].text
            parsed_result = self._parse_json_response(result_text)
            
            if parsed_result:
                score = parsed_result.get('trust_score', 0.0)
                print(f"      ✅ Claude 신뢰도: {score*100:.1f}%")
                return parsed_result
            else:
                print("      ⚠️ Claude 응답 파싱 실패")
                return None
                
        except Exception as e:
            print(f"      ❌ Claude 검증 오류: {e}")
            return None
    
    def _synthesize_results(self, gpt_result: Optional[Dict], 
                           claude_result: Optional[Dict], 
                           raw_data: Dict) -> Dict:
        """검증 결과 종합 및 최종 판정"""
        print("   ⚖️ [종합 평가] 최종 신뢰도 계산...")
        
        # 기본값 설정
        base_verdict = {
            'is_verified': False,
            'trust_score': 0.0,
            'verified_content': raw_data.get('content', ''),
            'verification_method': 'none',
            'issues': ['검증 실패'],
            'reasoning': '검증 시스템 오류'
        }
        
        # GPT 결과만 있는 경우
        if gpt_result and not claude_result:
            gpt_score = gpt_result.get('trust_score', 0.0)
            
            if gpt_score >= self.trust_threshold:
                return {
                    'is_verified': True,
                    'trust_score': gpt_score,
                    'verified_content': gpt_result.get('verified_content', raw_data.get('content', '')),
                    'verification_method': 'gpt_only',
                    'issues': gpt_result.get('issues', []),
                    'reasoning': f"GPT 단독 검증 통과 ({gpt_score*100:.1f}%)"
                }
            else:
                return {
                    **base_verdict,
                    'trust_score': gpt_score,
                    'reasoning': f"GPT 신뢰도 부족 ({gpt_score*100:.1f}% < {self.trust_threshold*100}%)"
                }
        
        # GPT + Claude 교차 검증
        elif gpt_result and claude_result:
            gpt_score = gpt_result.get('trust_score', 0.0)
            claude_score = claude_result.get('trust_score', 0.0)
            agrees = claude_result.get('agrees_with_gpt', True)
            recommendation = claude_result.get('recommendation', 'accept')
            
            # 가중 평균 (GPT 40%, Claude 60%)
            combined_score = (gpt_score * 0.4) + (claude_score * 0.6)
            
            # 의견 불일치 시 신뢰도 하락
            if not agrees:
                combined_score *= 0.85
                print(f"      ⚠️ AI 간 의견 불일치 (신뢰도 15% 하락)")
            
            # 최종 판정
            if combined_score >= self.trust_threshold and recommendation != 'reject':
                final_content = claude_result.get('final_content') or gpt_result.get('verified_content', raw_data.get('content', ''))
                
                return {
                    'is_verified': True,
                    'trust_score': combined_score,
                    'verified_content': final_content,
                    'verification_method': 'cross_verified',
                    'issues': gpt_result.get('issues', []) + claude_result.get('additional_concerns', []),
                    'reasoning': f"교차 검증 통과 ({combined_score*100:.1f}%, 합의: {'예' if agrees else '아니오'})"
                }
            else:
                return {
                    **base_verdict,
                    'trust_score': combined_score,
                    'reasoning': f"교차 검증 실패 (신뢰도: {combined_score*100:.1f}%, 권고: {recommendation})"
                }
        
        # 검증 불가능한 경우
        else:
            return {
                **base_verdict,
                'reasoning': 'AI 검증 시스템 사용 불가'
            }
    
    def _parse_json_response(self, text: str) -> Optional[Dict]:
        """AI 응답에서 JSON 추출 및 파싱"""
        try:
            # JSON 패턴 찾기
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return None
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    def get_verification_stats(self) -> Dict:
        """검증 통계 반환"""
        if not self.verification_history:
            return {
                'total_verifications': 0,
                'success_rate': 0.0,
                'avg_trust_score': 0.0
            }
        
        total = len(self.verification_history)
        verified = sum(1 for v in self.verification_history if v['verdict']['is_verified'])
        avg_score = sum(v['verdict']['trust_score'] for v in self.verification_history) / total
        
        return {
            'total_verifications': total,
            'verified_count': verified,
            'rejected_count': total - verified,
            'success_rate': verified / total,
            'avg_trust_score': avg_score,
            'trust_threshold': self.trust_threshold
        }
