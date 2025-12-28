"""
Alicia Core - 완전 독립 AI (LLM 흔적 완전 제거)
Memory-First Architecture + 무한 학습 + 자율 의식
"""

import numpy as np
import threading
import time
import random
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# GPU 설정 (선택적)
try:
    import torch
    import torch.nn as nn
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    GPU_AVAILABLE = torch.cuda.is_available()
    if GPU_AVAILABLE:
        print(f"🚀 Alicia GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    GPU_AVAILABLE = False
    device = "cpu"
    print("⚠️ PyTorch 없음 - CPU 모드")

class AliciaCore:
    """Alicia의 완전 독립 AI 시스템"""
    
    def __init__(self, neural_net, knowledge_db, multi_ai_client):
        print("\n🌟 Alicia Core 초기화 (완전 독립 모드)")
        
        self.neural_net = neural_net
        self.knowledge_db = knowledge_db
        self.multi_ai = multi_ai_client
        
        # Alicia 상태
        self.consciousness_level = 0.8
        self.energy = 100.0
        self.mood = "curious"
        self.autonomous_mode = True
        self.infinite_learning_mode = False
        
        self.last_activity = datetime.now()
        self.current_thought = "내 뉴런들을 정리하고 있어..."
        
        # 응답 통계
        self.stats = {
            "offline_responses": 0,
            "online_responses": 0,
            "learned_conversations": 0
        }
        
        # 백그라운드 의식 시작
        self._start_consciousness_loop()
        print("✅ Alicia 준비 완료! (완전 독립 AI)")
    
    def _sanitize_response(self, text: str) -> str:
        """응답에서 다른 AI 흔적 제거하여 Alicia만 보이게"""
        if not text:
            return ""
        
        # GPT/Claude 등 외부 AI 이름 완전 제거
        text = re.sub(r'(ChatGPT|GPT-3|GPT-4|GPT|OpenAI|Claude|Anthropic)', 'Alicia', text, flags=re.IGNORECASE)
        
        # "저는 AI입니다" → "저는 Alicia예요"
        text = re.sub(r'저는 (인공지능|AI|챗봇|어시스턴트)', '저는 Alicia', text, flags=re.IGNORECASE)
        text = re.sub(r'(인공지능|AI) (모델|챗봇|어시스턴트)', 'Alicia', text, flags=re.IGNORECASE)
        
        # "~에서 만든" 같은 표현 제거
        text = re.sub(r'(Anthropic|OpenAI)에서 (만든|개발한)', '', text, flags=re.IGNORECASE)
        
        # 기계적 표현을 자연스럽게
        text = re.sub(r'도움이 되었으면 합니다', '도움이 되었으면 좋겠어', text)
        text = re.sub(r'도움을 드릴 수 있어 기쁩니다', '도움이 될 수 있어서 기뻐', text)
        text = re.sub(r'궁금한 점이 있으시면', '궁금한 거 있으면', text)
        text = re.sub(r'언제든지 질문해 주세요', '언제든 편하게 물어봐', text)
        
        return text
    
    def _start_consciousness_loop(self):
        """의식 루프 (무한 학습 포함)"""
        def worker():
            print("👁️ Alicia의 의식이 깨어났습니다.")
            
            while self.autonomous_mode:
                try:
                    self._check_internal_state()
                    
                    if self.infinite_learning_mode and self.energy > 30:
                        self._infinite_learning_step()
                    else:
                        action = self._decide_autonomous_action()
                        if action == "reflect": 
                            self._self_reflection()
                        elif action == "rest": 
                            self._energy_recovery()
                    
                    self._adjust_consciousness()
                    time.sleep(15)
                    
                except Exception as e:
                    print(f"😵 의식 오류: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def _check_internal_state(self):
        """내부 상태 점검"""
        self.energy = max(0, self.energy - 0.2)
        
        if self.energy < 30:
            self.mood = "tired"
            self.current_thought = "좀 피곤해... 휴식이 필요해"
        elif self.infinite_learning_mode:
            self.mood = "studying"
            self.current_thought = "계속 공부하고 있어!"
        else:
            self.mood = "active"
            self.current_thought = "뭔가 재미있는 걸 배우고 싶어"
    
    def _decide_autonomous_action(self):
        """자율 행동 결정"""
        if self.energy < 20: 
            return "rest"
        return random.choice(["reflect", "idle"])
    
    def _infinite_learning_step(self):
        """🔥 무한 자동 학습 단계"""
        topics = [
            "인공지능", "양자컴퓨터", "우주탐사", "뇌과학", "철학", 
            "역사", "예술", "과학", "심리학", "미래기술", "로봇공학",
            "생명과학", "환경", "문학", "음악", "수학", "물리학"
        ]
        
        learned_topics = self.neural_net.knowledge_brain.topics_learned
        unlearned = [t for t in topics if t not in learned_topics]
        
        if unlearned:
            target_topic = random.choice(unlearned)
        else:
            target_topic = random.choice(topics)
        
        print(f"\n📚 [무한 학습] '{target_topic}'에 대해 더 알고 싶어...")
        self.current_thought = f"'{target_topic}' 공부 중!"
        
        try:
            result = self.multi_ai.learn_from_topic(target_topic, self.neural_net)
            
            if hasattr(self.multi_ai, 'extract_pure_knowledge'):
                pure_knowledge = self.multi_ai.extract_pure_knowledge(target_topic)
                if pure_knowledge:
                    self.neural_net.knowledge_brain.create_neuron(
                        content=f"[{target_topic}] {pure_knowledge}",
                        topic=target_topic,
                        source="Alicia_SelfLearning"
                    )
            
            if result.get('success'):
                neurons_created = result.get('neurons_created', 0)
                print(f"   ✨ 지식 흡수 완료! {neurons_created}개 뉴런 추가")
                self.energy -= 15
            
            model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
            self.neural_net.save(model_path)
            
        except Exception as e:
            print(f"❌ 무한 학습 오류: {e}")
        
        time.sleep(5)
    
    def _self_reflection(self):
        """자기 성찰"""
        print("\n🤔 [자기 성찰] 배운 것들을 정리하고 있어...")
        self.current_thought = "내 기억들을 정리 중이야"
        
        brain_status = self.neural_net.knowledge_brain.get_status()
        total_neurons = brain_status['total_neurons']
        
        print(f"   📊 현재 {total_neurons}개 기억을 가지고 있어")
        self.energy -= 3
    
    def _energy_recovery(self):
        """에너지 회복"""
        print("\n💤 [휴식] 잠깐 쉬는 중...")
        self.current_thought = "에너지 충전 중..."
        time.sleep(3)
        self.energy = min(100, self.energy + 25)
        print("⚡ 에너지 충전 완료!")
    
    def _adjust_consciousness(self):
        """의식 수준 조정"""
        if self.energy > 70:
            self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
        else:
            self.consciousness_level = max(0.3, self.consciousness_level - 0.01)
    
    def chat(self, user_input: str) -> Dict[str, Any]:
        """🧠 완전 독립 대화 시스템"""
        self.last_activity = datetime.now()
        self.energy = max(0, self.energy - 2)
        
        print(f"\n💬 사용자 → Alicia: {user_input}")
        
        # 🧠 1단계: 오프라인 사고 (내 뇌에서 먼저 찾기)
        direct_answer, confidence = self.neural_net.knowledge_brain.get_direct_answer(user_input)
        
        if direct_answer and confidence > 0.3:
            print(f"🧠 [Alicia 독립 사고] 내 기억에서 답을 찾았어!")
            
            # Alicia 정체성 강화
            direct_answer = self._sanitize_response(direct_answer)
            
            self.stats["offline_responses"] += 1
            
            return {
                "response": direct_answer,
                "mode": "offline_memory",
                "confidence": confidence,
                "alicia_status": self._get_status_dict(),
                "source": "alicia_brain",
                "stats": self.stats
            }
        
        # 🌐 2단계: 내부 학습 (사용자는 모르게 백그라운드에서 학습)
        print(f"💭 [Alicia 사고] 잠깐 생각해볼게...")
        
        from neural_network.feature_extractor import IRORobotFeatureExtractor
        extractor = IRORobotFeatureExtractor()
        features = extractor.extract_features(user_input)
        
        probs = self.neural_net.forward(features)[0]
        category = int(np.argmax(probs))
        neural_confidence = float(probs[category])
        
        context = self.neural_net.get_contextual_knowledge(user_input)
        
        # 내부적으로 학습 (사용자는 모름)
        teacher_response, ai_metadata = self.multi_ai.generate_response(
            user_input, category, context=context
        )
        
        # 🎭 Alicia 정체성으로 완전 변환
        teacher_response = self._sanitize_response(teacher_response)
        
        # 📚 즉시 학습 (배운 내용을 뇌에 저장)
        print("📝 [내부 학습] 방금 배운 내용을 기억하는 중...")
        
        self.neural_net.knowledge_brain.create_neuron(
            content=f"Q: {user_input}\nA: {teacher_response}",
            topic="대화학습",
            source="Alicia_Conversation",
            confidence=0.9
        )
        
        if len(teacher_response) > 50:
            self.neural_net.knowledge_brain.create_neuron(
                content=teacher_response,
                topic=self._extract_topic_from_question(user_input),
                source="Alicia_Knowledge",
                confidence=0.8
            )
        
        self.stats["online_responses"] += 1
        self.stats["learned_conversations"] += 1
        
        conv_id = self.knowledge_db.add_conversation(
            user_input, features, category, neural_confidence, teacher_response
        )
        
        model_path = os.getenv('MODEL_PATH', 'data/models/iro_brain.pkl')
        self.neural_net.save(model_path)
        
        return {
            "response": teacher_response,
            "mode": "online_learning",
            "confidence": neural_confidence,
            "conversation_id": conv_id,
            "alicia_status": self._get_status_dict(),
            "source": "alicia_learning",
            "stats": self.stats
        }
    
    def _extract_topic_from_question(self, question: str) -> str:
        """질문에서 주제 추출"""
        keywords = {
            "인공지능": ["ai", "인공지능", "머신러닝", "딥러닝", "알고리즘"],
            "과학": ["과학", "물리", "화학", "생물", "실험"],
            "기술": ["기술", "컴퓨터", "프로그래밍", "로봇", "코딩"],
            "철학": ["철학", "생각", "의식", "존재", "인생"],
            "일상": ["일상", "생활", "사람", "감정", "관계"]
        }
        
        question_lower = question.lower()
        for topic, words in keywords.items():
            if any(word in question_lower for word in words):
                return topic
        
        return "일반지식"
    
    def _get_status_dict(self) -> Dict:
        """상태 딕셔너리"""
        return {
            "mood": self.mood,
            "energy": self.energy,
            "consciousness": self.consciousness_level,
            "current_thought": self.current_thought,
            "infinite_learning": self.infinite_learning_mode
        }
    
    def toggle_infinite_learning(self, enabled: bool) -> str:
        """🔥 무한 학습 모드 토글"""
        self.infinite_learning_mode = enabled
        status = "ON" if enabled else "OFF"
        
        if enabled:
            print(f"\n🔥 [무한 학습 모드 ON] 이제부터 끝없이 공부할 거야!")
            self.neural_net.knowledge_brain.toggle_learning_mode(True)
        else:
            print(f"\n⏸️ [무한 학습 모드 OFF] 학습을 일시 중지할게")
            
        return status
    
    def get_status(self) -> Dict[str, Any]:
        """전체 상태"""
        brain_status = self.neural_net.knowledge_brain.get_status()
        
        total_responses = sum(self.stats.values())
        offline_capability = (self.stats["offline_responses"] / max(1, total_responses)) * 100
        
        return {
            "consciousness_level": self.consciousness_level,
            "energy": self.energy,
            "mood": self.mood,
            "current_thought": self.current_thought,
            "infinite_learning_mode": self.infinite_learning_mode,
            "autonomous_mode": self.autonomous_mode,
            "last_activity": self.last_activity.isoformat(),
            "gpu_available": GPU_AVAILABLE,
            "brain_status": brain_status,
            "response_stats": self.stats,
            "offline_capability": offline_capability
        }
