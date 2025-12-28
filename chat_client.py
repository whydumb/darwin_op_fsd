"""
IRO AI 채팅 클라이언트
사용자가 터미널에서 AI와 대화할 수 있는 프로그램
"""
import requests
import json

def main():
    print("🤖 IRO AI 채팅 클라이언트")
    print("=" * 50)
    print("서버 연결 확인 중...")
    
    base_url = "http://localhost:5000"
    
    # 서버 연결 테스트
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ 서버 연결 성공!")
            print(f"   상태: {health_data['status']}")
        else:
            print("❌ 서버 상태 불량")
            return
    except Exception as e:
        print(f"❌ 서버에 연결할 수 없습니다: {e}")
        print("💡 다른 터미널에서 'python backend/main.py'가 실행 중인지 확인하세요.")
        return
    
    categories = {
        0: "💬 일반대화",
        1: "🔧 기술질문", 
        2: "🎨 창의설계"
    }
    
    print("\n🚀 대화를 시작하세요! (종료: q)")
    print("예시: '아두이노 라인트레이싱 알고리즘 알려주세요'")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n🧑‍🎓 당신: ").strip()
            
            if user_input.lower() == 'q':
                print("\n👋 대화를 종료합니다. IRO 대회 준비 화이팅!")
                break
                
            if not user_input:
                continue
            
            # 서버로 메시지 전송
            print("⏳ AI가 생각 중...")
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": user_input},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                category_name = categories.get(data['category'], '기타')
                confidence = data['confidence'] * 100
                
                print(f"\n🤖 IRO AI ({category_name} | 확신도: {confidence:.1f}%):")
                print(f"{data['response']}")
                
                # AI 뇌 상태 표시
                brain = data.get('brain_status', {})
                if brain:
                    print(f"\n🧠 AI 상태: {brain.get('neurons', 0)}개 뉴런 | "
                          f"{brain.get('conversations', 0)}회 대화 경험")
                
                # 피드백 수집 (학습 데이터)
                print(f"\n💡 AI 분류가 정확했나요?")
                print("   0: 일반대화/격려")
                print("   1: 기술질문/코딩") 
                print("   2: 창의적설계")
                print("   엔터: 맞음")
                
                feedback = input("   올바른 번호 입력: ").strip()
                
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
                        print("   ⚠️ 피드백 저장 실패")
                else:
                    # 자동 피드백 (맞다고 가정)
                    requests.post(
                        f"{base_url}/api/feedback",
                        json={
                            "conversation_id": data['conversation_id'],
                            "correct_category": data['category']
                        }
                    )
                    
            else:
                print(f"❌ 서버 오류 ({response.status_code}): {response.text}")
                
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except requests.exceptions.Timeout:
            print("❌ 서버 응답 시간 초과. 다시 시도해주세요.")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
