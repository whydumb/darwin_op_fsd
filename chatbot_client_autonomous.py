"""
IRO 자율 AI 시스템 클라이언트
"""

import requests
import json
import time
from typing import Optional

class AutonomousAIClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
    
    def check_connection(self) -> bool:
        """서버 연결 확인"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 서버 연결 성공! 상태: {data['status']}")
                brain_status = data.get('brain_status', {})
                print(f"🧠 분류 뉴런: {brain_status.get('neurons', 0)}개")
                print(f"💾 지식 뉴런: {brain_status.get('knowledge_neurons', 0)}개")
                print(f"🎯 자율성: {data.get('autonomy_level', 'UNKNOWN')}")
                return True
        except Exception as e:
            print(f"❌ 서버 연결 실패: {e}")
            print("💡 backend/main.py를 먼저 실행하세요.")
            return False
    
    def chat_autonomous(self, message: str, force_autonomous: bool = False) -> Optional[dict]:
        """자율 모드 채팅"""
        try:
            start_time = time.time()
            response = requests.post(f"{self.api_url}/chat", 
                                   json={"message": message, "force_autonomous": force_autonomous})
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # 자율성 정보 표시
                autonomous_info = data.get('autonomous_decision', {})
                consciousness_info = data.get('consciousness_state', {})
                
                print(f"\n🤖 IRO AI ({elapsed:.1f}s):")
                print(f"   🧠 모드: {autonomous_info.get('mode', 'unknown')}")
                print(f"   🎯 자율성: {autonomous_info.get('autonomy_level', 'LEARNING')}")
                
                if autonomous_info.get('neurons_used'):
                    print(f"   📚 사용 뉴런: {autonomous_info['neurons_used']}개")
                
                if autonomous_info.get('new_neurons_created'):
                    print(f"   🌱 새 뉴런: {autonomous_info['new_neurons_created']}개")
                
                print(f"   💭 응답: {data['response']}")
                
                # 성장 이벤트 알림
                if data.get('growth_event', {}).get('occurred'):
                    reason = data['growth_event']['reason']
                    print(f"   ✨ [신경망 성장] {reason}")
                
                return data
            else:
                print(f"❌ 오류: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 통신 오류: {e}")
            return None
    
    def autonomous_learn(self, topic: str, depth: str = "moderate") -> bool:
        """자율 학습 실행"""
        try:
            print(f"🔍 '{topic}' 자율 학습 시작... (깊이: {depth})")
            
            response = requests.post(f"{self.api_url}/autonomous-learn",
                                   json={"topic": topic, "depth": depth})
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ 자율 학습 완료!")
                    print(f"   📊 생성 뉴런: {data.get('neurons_created')}개")
                    print(f"   🎯 품질 점수: {data.get('search_quality', 0):.2f}")
                    print(f"   🏆 주제 전문성: {data.get('topic_expertise', 0)*100:.1f}%")
                    return True
                else:
                    print(f"❌ 학습 실패: {data.get('error')}")
            return False
        except Exception as e:
            print(f"❌ 학습 오류: {e}")
            return False
    
    def get_status(self) -> Optional[dict]:
        """시스템 상태 조회"""
        try:
            response = requests.get(f"{self.api_url}/status")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ 상태 조회 오류: {e}")
            return None

def print_colored(text: str, color: str = "white"):
    """컬러 출력"""
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "purple": "\033[95m", "cyan": "\033[96m", "white": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}\033[0m")

def main():
    print_colored("🌟 IRO 자율 AI 시스템 v2.0", "cyan")
    print_colored("=" * 60, "cyan")
    
    client = AutonomousAIClient()
    
    if not client.check_connection():
        return
    
    print("\n📋 명령어:")
    print("  일반 대화: 그냥 입력")
    print("  강제 자율: /auto [메시지]")
    print("  자율 학습: /learn [주제] [깊이:shallow/moderate/deep]")
    print("  상태 확인: /status")
    print("  종료: /quit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n💬 당신: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == '/quit':
                print_colored("👋 안녕히 가세요!", "green")
                break
            
            elif user_input.startswith('/auto '):
                message = user_input[6:].strip()
                if message:
                    client.chat_autonomous(message, force_autonomous=True)
            
            elif user_input.startswith('/learn '):
                parts = user_input[7:].split()
                topic = parts[0] if parts else ""
                depth = parts[1] if len(parts) > 1 else "moderate"
                
                if topic:
                    client.autonomous_learn(topic, depth)
                else:
                    print("사용법: /learn [주제] [깊이]")
            
            elif user_input == '/status':
                status = client.get_status()
                if status:
                    print(json.dumps(status, indent=2, ensure_ascii=False))
            
            else:
                # 일반 대화 (자율 판단)
                client.chat_autonomous(user_input)
        
        except KeyboardInterrupt:
            print_colored("\n👋 안녕히 가세요!", "green")
            break
        except Exception as e:
            print_colored(f"오류: {e}", "red")

if __name__ == "__main__":
    main()
