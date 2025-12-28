"""
Alicia 독립 AI 클라이언트 (외부 AI 흔적 완전 제거)
"""

import requests
import time
import sys

API_URL = "http://localhost:5000/api"

def check_server():
    """서버 연결 확인"""
    try:
        response = requests.get(f"{API_URL}/alicia/status", timeout=2)
        return response.status_code == 200
    except:
        return False

def chat(message):
    """Alicia와 대화 (완전 독립 모드)"""
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_URL}/alicia/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("response", "")
            status = data.get("alicia_status", {})
            mode = data.get("mode", "unknown")
            
            mood_icon = {
                "curious": "🤔 호기심",
                "active": "😊 활발", 
                "tired": "😴 피곤",
                "studying": "📚 열공중"
            }.get(status.get("mood", ""), "😐")
            
            print(f"\n🤖 Alicia ({end_time - start_time:.1f}s) [{mood_icon}]:")
            print(f"   💭 {reply}")
            
            # Alicia의 사고 과정만 표시 (AI 협업 정보 완전 제거)
            if mode == "offline_memory":
                print("   🧠 (내 기억에서 찾았어!)")
            elif mode == "online_learning":
                print("   🎓 (새로 배워서 기억했어!)")
            else:
                print("   💭 (생각해봤어!)")
                
        else:
            print(f"❌ 오류: {response.text}")
            
    except requests.Timeout:
        print("⏱️ Alicia가 깊게 생각하고 있어요... (30초 초과)")
    except Exception as e:
        print(f"❌ 통신 오류: {e}")

def learn_topic(topic):
    """주제 학습"""
    try:
        print(f"\n🎓 Alicia가 '{topic}' 학습 중...")
        response = requests.post(
            f"{API_URL}/learn-topic",
            json={"topic": topic, "force": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = data.get("result", {})
                neurons = result.get("neurons_created", 0)
                print(f"\n✅ 학습 완료: {neurons}개의 새로운 지식 뉴런 생성")
            else:
                print("\n❌ 학습 실패")
        else:
            print(f"❌ 오류: {response.text}")
            
    except Exception as e:
        print(f"❌ 학습 오류: {e}")

def toggle_infinite_learning(enable):
    """무한 학습 모드 토글"""
    try:
        response = requests.post(
            f"{API_URL}/alicia/infinite-learning",
            json={"enable": enable},
            timeout=5
        )
        
        if response.status_code == 200:
            if enable:
                print("🔥 무한 학습 모드 ON - Alicia가 끝없이 공부합니다!")
                print("   (서버 터미널에서 '[무한 학습]' 로그를 확인하세요)")
            else:
                print("⏸️ 무한 학습 모드 OFF - 학습을 중지했습니다.")
        else:
            print(f"❌ 설정 오류: {response.text}")
            
    except Exception as e:
        print(f"❌ 통신 오류: {e}")

def show_status():
    """Alicia 상태 표시"""
    try:
        response = requests.get(f"{API_URL}/alicia/stats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get("stats", {})
            
            print("\n" + "=" * 50)
            print("📊 Alicia 상태")
            print("=" * 50)
            print(f"🧠 지식 뉴런: {data.get('brain_neurons', 0)}개")
            print(f"📚 학습한 주제: {data.get('topics_learned', 0)}개")
            print(f"💭 독립 응답: {stats.get('offline_responses', 0)}회")
            print(f"🎓 학습 응답: {stats.get('online_responses', 0)}회")
            print(f"🎯 독립 능력: {data.get('offline_capability', 0):.1f}%")
            print("=" * 50)
        else:
            print(f"❌ 상태 조회 실패: {response.text}")
            
    except Exception as e:
        print(f"❌ 통신 오류: {e}")

def main():
    """메인 실행"""
    print("🌟 Alicia와의 대화 시작")
    print("=" * 50)
    
    if not check_server():
        print("❌ 서버에 연결할 수 없습니다.")
        print("💡 먼저 'cd backend && python main.py'로 서버를 실행하세요.")
        return
    
    print("✅ 서버 연결 성공")
    print("📌 🧠 Alicia 독립 AI 모드 활성화")
    print("\n📋 명령어:")
    print("  일반 대화: 그냥 입력")
    print("  학습: /learn [주제]")
    print("  무한 학습 시작: /infinite on")
    print("  무한 학습 중지: /infinite off")
    print("  상태 확인: /status")
    print("  종료: /quit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n💬 당신: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                print("\n👋 Alicia: 안녕히 가세요!")
                break
            
            if user_input.startswith('/learn '):
                topic = user_input[7:].strip()
                if topic:
                    learn_topic(topic)
                else:
                    print("❌ 주제를 입력하세요. 예: /learn 양자컴퓨터")
                continue
            
            if user_input.startswith('/infinite '):
                mode = user_input[10:].strip().lower()
                if mode == 'on':
                    toggle_infinite_learning(True)
                elif mode == 'off':
                    toggle_infinite_learning(False)
                else:
                    print("❌ 'on' 또는 'off'를 입력하세요")
                continue
            
            if user_input.lower() == '/status':
                show_status()
                continue
            
            # 일반 대화
            chat(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 Alicia: 안녕히 가세요!")
            break
        except Exception as e:
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    main()
