"""
지식 데이터베이스 - 대화 기록 및 피드백 저장
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class KnowledgeDatabase:
    """대화 기록 및 피드백 관리"""
    
    def __init__(self, db_path: str = "data/knowledge/database.json"):
        self.db_path = db_path
        self.data = {
            "conversations": [],
            "feedbacks": [],
            "statistics": {
                "total_conversations": 0,
                "total_feedbacks": 0,
                "created_at": datetime.now().isoformat()
            }
        }
        
        self._ensure_directory()
        self._load_data()
    
    def _ensure_directory(self):
        """디렉토리 생성"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _load_data(self):
        """데이터 로드"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # statistics 키가 없으면 기본값 생성
                    if 'statistics' not in loaded_data:
                        loaded_data['statistics'] = {
                            "total_conversations": len(loaded_data.get('conversations', [])),
                            "total_feedbacks": len(loaded_data.get('feedbacks', [])),
                            "created_at": datetime.now().isoformat()
                        }
                    self.data = loaded_data
                print(f"📂 데이터베이스 로드: {len(self.data.get('conversations', []))}개 대화, {len(self.data.get('feedbacks', []))}개 피드백")
            except Exception as e:
                print(f"⚠️ 데이터베이스 로드 실패: {e}")
    
    def _save_data(self):
        """데이터 저장"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 데이터베이스 저장 실패: {e}")
    
    def add_conversation(self, user_input: str, features: any, category: int, 
                        confidence: float, ai_response: str) -> int:
        """대화 기록 추가"""
        conv_id = len(self.data["conversations"]) + 1
        
        conversation = {
            "id": conv_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "category": category,
            "confidence": confidence,
            "features": features.tolist() if hasattr(features, 'tolist') else features,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["conversations"].append(conversation)
        self.data["statistics"]["total_conversations"] += 1
        
        self._save_data()
        return conv_id
    
    def add_feedback(self, conversation_id: int, correct_category: int, rating: int = 5) -> bool:
        """피드백 추가"""
        try:
            feedback = {
                "conversation_id": conversation_id,
                "correct_category": correct_category,
                "rating": rating,
                "timestamp": datetime.now().isoformat()
            }
            
            self.data["feedbacks"].append(feedback)
            self.data["statistics"]["total_feedbacks"] += 1
            
            self._save_data()
            return True
        except Exception as e:
            print(f"❌ 피드백 저장 실패: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """통계 정보"""
        return {
            "total_conversations": len(self.data.get("conversations", [])),
            "total_feedbacks": len(self.data.get("feedbacks", [])),
            "recent_conversations": self.data.get("conversations", [])[-5:],
            "database_size": f"{os.path.getsize(self.db_path) / 1024:.1f}KB" if os.path.exists(self.db_path) else "0KB"
        }