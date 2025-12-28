"""
IRO AI 클라이언트 v4.0 - 학습 + 완전한 기억 모드
- 기존: 일반 대화, 피드백, 학습 모드, 주제 학습
- 추가: 완전한 기억 시스템 (전체 개요, 주제별 검색, 뉴런 상세, 대화 기록)
- 수정: 타임아웃 300초로 증가
"""

import requests
import time

def print_separator(char="=", length=60):
    print(char * length)

def print_brain_status(brain_status):
    """뇌 상태를 시각적으로 표시"""
    print(f"\n🧠 AI 뇌 상태:")
    print(f"   🔢 분류 뉴런: {brain_status.get('neurons', 0)}개")
    print(f"   🧩 지식 뉴런: {brain_status.get('knowledge_neurons', 0)}개")
    print(f"   🔗 지식 연결: {brain_status.get('knowledge_connections', 0)}개")
    print(f"   📚 학습 주제: {brain_status.get('topics_learned', 0)}개")
    print(f"   🌱 성장 이벤트: {brain_status.get('knowledge_growth_events', 0)}회")
    print(f"   📖 총 대화: {brain_status.get('conversations', 0)}회")
    
    learning_status = "🟢 ON" if brain_status.get('learning_mode') else "🔴 OFF"
    print(f"   🎯 학습 모드: {learning_status}")

def main():
    base_url = "http://localhost:5000"
    
    print_separator()
    print("🤖 IRO AI v4.0 - 자가 성장 + GPT+Claude 협업 + 완전한 기억 모드")
    print_separator()
    print("💡 사용 가능한 명령어:")
    print("  📝 일반 대화: 질문을 입력하세요")
    print("  🎯 학습 모드: '/learn on' 또는 '/learn off'")
    print("  📚 주제 학습: '/study [주제명]' (예: /study 양자컴퓨팅)")
    print("  📊 상태 확인: '/status'")
    print("  🧠 기억 개요: '/memory'")
    print("  🧠 주제 기억: '/memory [주제명]'")
    print("  🔍 뉴런 상세: '/detail [뉴런ID]'")
    print("  💬 대화 기록: '/history'")
    print("  🚪 종료: 'q' 또는 'quit'")
    print_separator()
    
    # 서버 연결 확인
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ 서버 연결 성공!")
            
            # 컴포넌트 상태 표시
            components = health_data.get('components', {})
            for comp, status in components.items():
                emoji = "✅" if status == "ready" else "❌"
                print(f"   {emoji} {comp}: {status}")
            
            # 초기 뇌 상태 표시
            brain_status = health_data.get('brain_status', {})
            if brain_status:
                print_brain_status(brain_status)
        else:
            print(f"⚠️ 서버 응답 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        print("💡 다른 터미널에서 'python backend/main.py'를 실행하세요.")
        return
    
    print_separator()
    print("🚀 대화를 시작하세요!")
    
    while True:
        try:
            user_input = input("\n🧑‍🎓 입력: ").strip()
            
            if user_input.lower() in ['q', 'quit']:
                print("\n👋 IRO AI와의 대화를 종료합니다. 로봇 대회 화이팅! 🚀")
                break
            
            if not user_input:
                continue
            
            # 🎯 학습 모드 토글
            if user_input.lower().startswith('/learn '):
                mode = user_input[7:].strip().lower()
                if mode in ['on', 'off']:
                    enabled = (mode == 'on')
                    
                    response = requests.post(
                        f"{base_url}/api/learning-mode",
                        json={"enabled": enabled},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        status_text = "활성화" if enabled else "비활성화"
                        print(f"✅ 학습 모드 {status_text}됨")
                        print_brain_status(data.get('brain_status', {}))
                    else:
                        print(f"❌ 학습 모드 변경 실패: {response.text}")
                else:
                    print("❌ 사용법: '/learn on' 또는 '/learn off'")
                continue
            
            # 📚 주제 학습
            if user_input.lower().startswith('/study '):
                topic = user_input[7:].strip()
                if not topic:
                    print("❌ 사용법: '/study [주제명]' (예: /study 머신러닝)")
                    continue
                
                print(f"\n🎓 '{topic}' 주제 학습을 시작합니다...")
                print("   (웹 검색 → GPT+Claude 협업 분석 → 지식 뉴런 생성)")
                print("   ⏳ 처리 중... (최대 5분 소요)")
                
                start_time = time.time()
                
                try:
                    # ✅ 타임아웃 300초로 증가
                    response = requests.post(
                        f"{base_url}/api/learn-topic",
                        json={"topic": topic, "force": True},
                        timeout=300
                    )
                    
                    duration = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        result = data.get('result', {})
                        
                        print(f"\n✨ 학습 완료! ({duration:.1f}초 소요)")
                        print(f"   📊 생성된 뉴런: {result.get('neurons_created', 0)}개")
                        print(f"   🆔 뉴런 ID: {result.get('neuron_ids', [])}")
                        
                        brain_status = data.get('brain_status', {})
                        print_brain_status(brain_status)
                        
                        print(f"\n💡 이제 '{topic}' 관련 질문을 하면 학습한 지식을 활용해 답변합니다!")
                        
                    else:
                        error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                        if error_data.get('error') == 'learning_mode_off':
                            print("⚠️ 학습 모드가 비활성화되어 있습니다.")
                            print("   '/learn on' 명령으로 학습 모드를 활성화하거나")
                            print("   force 모드로 일회성 학습을 수행했습니다.")
                        else:
                            print(f"❌ 학습 실패: {response.text}")
                            
                except requests.exceptions.Timeout:
                    print("❌ 학습 시간 초과 (5분). 네트워크를 확인하고 다시 시도해주세요.")
                except Exception as e:
                    print(f"❌ 학습 중 오류: {e}")
                
                continue
            
            # 📊 상태 확인
            if user_input.lower() == '/status':
                try:
                    response = requests.get(f"{base_url}/api/status", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        brain_status = data.get('neural_network', {})
                        db_stats = data.get('knowledge_base', {})
                        
                        print("\n📊 === 시스템 상태 리포트 ===")
                        print_brain_status(brain_status)
                        
                        print(f"\n💾 데이터베이스 통계:")
                        print(f"   📝 총 대화 기록: {db_stats.get('total_conversations', 0)}개")
                        print(f"   👍 피드백 수: {db_stats.get('total_feedback', 0)}개")
                        print(f"   📈 피드백 비율: {db_stats.get('feedback_rate', 0):.1f}%")
                    else:
                        print(f"❌ 상태 조회 실패: {response.text}")
                except Exception as e:
                    print(f"❌ 상태 조회 오류: {e}")
                continue

            # 🧠 기억 개요
            if user_input.lower() == '/memory':
                try:
                    response = requests.get(f"{base_url}/api/memories", timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"\n🧠 === IRO AI 기억 저장소 ===")
                        print(f"📊 총 지식 뉴런: {data['total_neurons']}개")
                        print(f"📚 학습 주제: {data['total_topics']}개")
                        
                        print(f"\n📚 주제별 기억 현황 (상위 8개):")
                        for topic_info in data['topics'][:8]:
                            print(f"   📖 {topic_info['topic']}: {topic_info['neuron_count']}개 뉴런 "
                                  f"(활성화 {topic_info['total_activations']}회, "
                                  f"신뢰도 {topic_info['avg_confidence']*100:.1f}%)")
                        
                        print(f"\n🔥 핵심 지식 (가장 많이 연결됨):")
                        for neuron in data['most_connected']:
                            preview_line = neuron['content'].split('\n')[0]
                            preview = (preview_line[:60] + '...') if len(preview_line) > 60 else preview_line
                            print(f"   • ID-{neuron['id']} [{neuron['topic']}] {preview}")
                            print(f"     연결: {len(neuron['connections'])}개 | 활성화: {neuron['activation_count']}회")
                        
                        print(f"\n✨ 최근 학습:")
                        for neuron in data['recent_memories']:
                            preview_line = neuron['content'].split('\n')[0]
                            preview = (preview_line[:60] + '...') if len(preview_line) > 60 else preview_line
                            created = neuron['created_at'][:19] if neuron['created_at'] else 'N/A'
                            print(f"   • ID-{neuron['id']} [{neuron['topic']}] {preview}")
                            print(f"     생성: {created}")
                        
                        print(f"\n💡 사용법:")
                        print("   • '/memory [주제명]' - 특정 주제 상세 조회")
                        print("   • '/detail [뉴런ID]' - 뉴런 상세 정보")
                        print("   • '/history' - 최근 대화 기록")
                    else:
                        print(f"❌ 기억 조회 실패: {response.text}")
                except Exception as e:
                    print(f"❌ 기억 조회 오류: {e}")
                continue

            # 🧠 주제별 기억 조회
            if user_input.lower().startswith('/memory '):
                topic = user_input[8:].strip()
                try:
                    response = requests.post(
                        f"{base_url}/api/memory/topic",
                        json={"topic": topic},
                        timeout=15
                    )
                    if response.status_code == 200:
                        data = response.json()
                        memories = data.get('memories', [])
                        if not memories:
                            print(f"\n⚠️ '{topic}' 관련 기억이 없습니다.")
                            print("💡 '/study [주제명]'으로 새로 학습할 수 있습니다.")
                        else:
                            print(f"\n📚 === '{topic}' 관련 기억 ({len(memories)}개) ===")
                            for i, memory in enumerate(memories, 1):
                                print(f"\n{i}. 🆔 뉴런 ID-{memory['id']}")
                                print(f"   🔥 활성화: {memory['activation_count']}회")
                                print(f"   🔗 연결: {len(memory['connections'])}개")
                                print(f"   📅 생성: {memory['created_at'][:19]}")
                                print(f"   ─────────────────────────────────")
                                content = memory['content']
                                if len(content) > 200:
                                    print(f"   {content[:200]}...")
                                    print(f"   💡 '/detail {memory['id']}'로 전체 내용 보기")
                                else:
                                    print(f"   {content}")
                                print(f"   ─────────────────────────────────")
                    else:
                        print(f"❌ 주제 기억 조회 실패: {response.text}")
                except Exception as e:
                    print(f"❌ 주제 기억 조회 오류: {e}")
                continue

            # 🔍 뉴런 상세 정보
            if user_input.lower().startswith('/detail '):
                parts = user_input.split()
                if len(parts) != 2 or not parts[1].isdigit():
                    print("❌ 사용법: '/detail [뉴런ID]' (예: /detail 5)")
                    continue
                neuron_id = int(parts[1])
                try:
                    response = requests.get(f"{base_url}/api/memory/{neuron_id}", timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        neuron = data.get('neuron', {})
                        print(f"\n🔍 === 뉴런 ID-{neuron['id']} 상세 정보 ===")
                        print(f"📚 주제: {neuron['topic']}")
                        print(f"🔧 출처: {neuron['source']}")
                        print(f"💯 신뢰도: {neuron['confidence']*100:.1f}%")
                        print(f"🔥 활성화: {neuron['activation_count']}회")
                        print(f"📅 생성: {neuron['created_at'][:19]}")
                        if neuron.get('last_accessed'):
                            print(f"👁️ 최근 접근: {neuron['last_accessed'][:19]}")
                        print(f"\n📝 전체 내용:")
                        print("═" * 60)
                        print(neuron.get('full_content', ''))
                        print("═" * 60)
                        connected = neuron.get('connected_neurons', [])
                        if connected:
                            print(f"\n🔗 연결된 뉴런들 ({len(connected)}개):")
                            for i, conn in enumerate(connected[:5], 1):
                                print(f"   {i}. ID-{conn['id']} [{conn['topic']}] "
                                      f"(연결강도: {conn['connection_strength']:.2f})")
                                print(f"      {conn['content_preview']}")
                            if len(connected) > 5:
                                print(f"   ... 외 {len(connected)-5}개 더")
                    elif response.status_code == 404:
                        print(f"❌ ID-{neuron_id} 뉴런을 찾을 수 없습니다.")
                    else:
                        print(f"❌ 뉴런 조회 실패: {response.text}")
                except Exception as e:
                    print(f"❌ 뉴런 상세 조회 오류: {e}")
                continue

            # 💬 최근 대화 기록
            if user_input.lower() == '/history':
                try:
                    response = requests.get(
                        f"{base_url}/api/conversations/recent",
                        params={'limit': 10},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        conversations = data.get('conversations', [])
                        print(f"\n💬 === 최근 대화 기록 ({len(conversations)}/{data['total_conversations']}개) ===")
                        categories = {0: "💬 일반대화", 1: "🔧 기술질문", 2: "🎨 창의설계"}
                        for i, conv in enumerate(conversations, 1):
                            cat_name = categories.get(conv.get('predicted_category'), '기타')
                            confidence = conv.get('confidence', 0) * 100
                            timestamp = conv.get('timestamp', '')[:19] if conv.get('timestamp') else 'N/A'
                            print(f"\n{i}. [{timestamp}] {cat_name} (확신도: {confidence:.1f}%)")
                            print(f"   👤 질문: {conv.get('user_input','')[:80]}...")
                            print(f"   🤖 응답: {conv.get('response','')[:80]}...")
                            if conv.get('feedback_given'):
                                print("   ✅ 피드백 제공됨")
                    else:
                        print(f"❌ 대화 기록 조회 실패: {response.text}")
                except Exception as e:
                    print(f"❌ 대화 기록 조회 오류: {e}")
                continue
            
            # 💬 일반 채팅
            print("⏳ AI가 생각 중...", end="\r")
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/chat",
                json={"message": user_input},
                timeout=120  # 일반 대화는 2분으로 유지
            )
            duration = time.time() - start_time
            
            print(f"✅ 응답 완료 ({duration:.1f}초)" + " " * 20)
            
            if response.status_code == 200:
                data = response.json()
                
                # AI 응답 표시
                categories = {0: "💬 일반대화", 1: "🔧 기술질문", 2: "🎨 창의설계"}
                category_name = categories.get(data['category'], '기타')
                confidence = data['confidence'] * 100
                
                print(f"\n🤖 IRO AI ({category_name} | 확신도: {confidence:.1f}%):")
                print("─" * 50)
                print(data['response'])
                print("─" * 50)
                
                # 협업 정보 표시
                ai_collab = data.get('ai_collaboration', {})
                mode = ai_collab.get('mode', 'unknown')
                winner = ai_collab.get('winner', 'Unknown')
                
                if mode == 'collaborative':
                    print(f"\n🏆 AI 협업: {winner.upper()} 선택됨")
                    if ai_collab.get('reason'):
                        print(f"   이유: {ai_collab['reason']}")
                elif mode == 'single':
                    print(f"\n🤖 {winner.upper()} 단독 응답")
                elif mode == 'error':
                    print(f"\n⚠️ AI 서비스 오류")
                
                # 컨텍스트 사용 여부
                if data.get('context_used'):
                    print("   💡 학습된 지식을 활용하여 답변했습니다")
                
                # 성장 이벤트
                growth = data.get('growth_event', {})
                if growth.get('occurred'):
                    print(f"\n🌱 AI 성장 발생! 이유: {growth['reason']}")
                
                # 간단한 뇌 상태
                brain = data.get('brain_status', {})
                if brain:
                    knowledge_neurons = brain.get('knowledge_neurons', 0)
                    topics = brain.get('topics_learned', 0)
                    if knowledge_neurons > 0:
                        print(f"\n🧠 현재 지식 뉴런: {knowledge_neurons}개 | 학습 주제: {topics}개")
                
                # 피드백 요청
                print(f"\n💡 분류가 정확했나요? (선택사항)")
                print("   0: 일반대화  1: 기술질문  2: 창의설계  엔터: 정확함")
                feedback_input = input("   올바른 번호: ").strip()
                
                if feedback_input in ['0', '1', '2']:
                    feedback_category = int(feedback_input)
                    
                    fb_response = requests.post(
                        f"{base_url}/api/feedback",
                        json={
                            "conversation_id": data['conversation_id'],
                            "correct_category": feedback_category
                        },
                        timeout=5
                    )
                    
                    if fb_response.status_code == 200:
                        if feedback_category != data['category']:
                            print("   ✅ 피드백 감사합니다! AI가 더 똑똑해질 거예요! 🧠✨")
                        else:
                            print("   ✅ 정확한 분류였네요! AI가 자신감을 얻었습니다! 💪")
                    else:
                        print("   ⚠️ 피드백 저장 실패")
                
            else:
                print(f"❌ 서버 오류 ({response.status_code}): {response.text}")
            
            print_separator("-")
            
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except requests.exceptions.Timeout:
            print("❌ 서버 응답 시간 초과. 다시 시도해주세요.")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
