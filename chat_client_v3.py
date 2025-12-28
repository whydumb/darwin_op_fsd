"""
IRO AI 멀티-협업 클라이언트
GPT + Claude 협업 + 자가 성장 결과 확인
"""
import requests
import time

def main():
    print("🤖 IRO AI 멀티-협업 시스템")
    print("=" * 60)
    print("🧠 자가 성장 신경망 + GPT & Claude 협업")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # 서버 연결 확인
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        health = response.json()
        print("✅ 서버 연결 성공!")
        print(f"   상태: {health['status']}")
        
        # 구성 요소 상태 표시
        components = health.get('components', {})
        for comp, status in components.items():
            emoji = "✅" if status == "ready" else "⚠️"
            print(f"   {emoji} {comp}: {status}")
        
    except Exception as e:
        print(f"❌ 서버에 연결할 수 없습니다: {e}")
        print("💡 다른 터미널에서 'python backend/main.py' 실행 중인지 확인하세요.")
        return
    
    categories = {0: "💬 일반대화", 1: "🔧 기술질문", 2: "🎨 창의설계"}
    
    print("\n🚀 대화를 시작하세요! (종료: q)")
    print("예시 질문:")
    print("  • '화성 탐사 로봇의 바퀴 시스템 설계해줘'")
    print("  • '아두이노 PID 제어 알고리즘 설명해줘'")
    print("  • '로봇 대회 준비하면서 힘든데 조언해줘'")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n🧑‍🎓 당신: ").strip()
            
            if user_input.lower() == 'q':
                print("\n👋 IRO 대회 준비 화이팅! 🚀")
                break
                
            if not user_input:
                continue
            
            print("⏳ GPT와 Claude가 협업하여 분석 중...", end="\r")
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/chat", 
                json={"message": user_input},
                timeout=60
            )
            duration = time.time() - start_time
            
            print(f"✅ 응답 완료 ({duration:.1f}초)        ")
            
            if response.status_code == 200:
                data = response.json()
                
                # 🤖 AI 응답 표시
                category_name = categories.get(data['category'], '기타')
                confidence = data['confidence'] * 100
                
                print(f"\n🤖 IRO AI 수석 코치 ({category_name} | 확신도: {confidence:.1f}%):")
                print("=" * 50)
                print(data['response'])
                print("=" * 50)
                
                # 🤝 협업 정보 표시
                ai_collab = data.get('ai_collaboration', {})
                winner = ai_collab.get('winner', '').upper()
                mode = ai_collab.get('mode', 'unknown')
                
                if mode == 'collaborative':
                    print(f"\n🏆 AI 협업 결과: {winner}의 답변이 선택됨")
                    if ai_collab.get('reason'):
                        print(f"   선택 이유: {ai_collab['reason']}")
                elif mode == 'single':
                    print(f"\n🤖 {winner} 단독 응답")
                elif mode == 'fallback':
                    print(f"\n⚠️ {winner} 대체 응답 (다른 AI 실패)")
                elif mode == 'error':
                    print(f"\n⚠️ AI 서비스 오류")
                
                # 🌱 성장 정보 표시
                growth = data.get('growth_event', {})
                if growth.get('occurred'):
                    print(f"\n🌱 AI 성장 발생!")
                    print(f"   성장 이유: {growth['reason']}")
                
                # 🧠 뇌 상태 표시
                brain = data.get('brain_status', {})
                if brain:
                    print(f"\n🧠 AI 뇌 상태:")
                    print(f"   뉴런 수: {brain.get('neurons', 0)}개")
                    print(f"   총 대화: {brain.get('conversations', 0)}회")
                    print(f"   성장 횟수: {brain.get('growth_events', 0)}회")
                    if brain.get('instant_growths', 0) > 0:
                        print(f"   즉시 성장: {brain.get('instant_growths', 0)}회")
                
                # 피드백 수집
                print(f"\n💡 AI 분류가 정확했나요?")
                print("   0: 일반대화  1: 기술질문  2: 창의설계  엔터: 맞음")
                feedback = input("   올바른 번호: ").strip()
                
                if feedback in ['0', '1', '2']:
                    fb_response = requests.post(
                        f"{base_url}/api/feedback",
                        json={
                            "conversation_id": data['conversation_id'],
                            "correct_category": int(feedback)
                        },
                        timeout=5
                    )
                    
                    if fb_response.status_code == 200:
                        if int(feedback) != data['category']:
                            print("   ✅ 피드백 감사합니다! AI가 더 똑똑해질 거예요! 🧠✨")
                        else:
                            print("   ✅ 정확한 분류였네요! AI가 자신감을 얻었습니다! 💪")
                
            else:
                print(f"❌ 서버 오류 ({response.status_code}): {response.text}")
                
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except requests.exceptions.Timeout:
            print("❌ 서버 응답 시간 초과 (60초). 다시 시도해주세요.")
        except Exception as e:
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    main()
