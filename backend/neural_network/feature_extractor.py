"""
IRO 로봇 대회 특화 특징 추출기
사용자 입력 → 10차원 벡터 변환
"""

import numpy as np
import re
from typing import List

class IRORobotFeatureExtractor:
    """IRO 로봇 대회에 특화된 특징 추출"""
    
    def __init__(self):
        self.category_keywords = {
            0: {  # 일반 대화/격려  
                'keywords': ['안녕', '고마워', '감사', '도와줘', '처음', '시작', '준비', '팀', '대회', '선배'],
                'weight': 1.5
            },
            1: {  # 기술 질문
                'keywords': ['아두이노', '센서', '모터', '코드', '프로그래밍', '회로', '제어', '알고리즘',
                           '초음파', 'pwm', '서보', '블루투스', '와이파이', 'c언어', '파이썬'],
                'weight': 2.0
            },
            2: {  # 미션 설계
                'keywords': ['미션', '우주', '임무', '설계', '아이디어', '전략', '계획', '창의적',
                           '샘플', '탐사', '로버', '착륙', '경기', '룰', '규정'],
                'weight': 1.8
            }
        }
        
        self.sentiment_keywords = {
            'positive': ['좋', '최고', '완벽', '성공', '잘', '훌륭', '대단', '신나'],
            'negative': ['어렵', '힘들', '모르', '실패', '안돼', '문제', '포기']
        }
        
        self.question_patterns = [
            r'\?$', r'^(어떻게|어떤|무엇|왜|언제|어디)', r'(알려줘|설명해|도와줘|가르쳐)'
        ]
    
    def extract_features(self, text: str) -> np.ndarray:
        """텍스트 → 1x10 특징 벡터"""
        text_lower = text.lower()
        features = np.zeros(10)
        
        # [0-2] 카테고리별 키워드 점수
        for cat_id, cat_info in self.category_keywords.items():
            keywords = cat_info['keywords']
            weight = cat_info['weight']
            matches = sum(1 for kw in keywords if kw in text_lower)
            features[cat_id] = min(1.0, (matches / len(keywords)) * weight)
        
        # [3] 질문 여부
        is_question = any(re.search(pattern, text) for pattern in self.question_patterns)
        features[3] = 1.0 if is_question else 0.0
        
        # [4] 감정 점수 (-1 ~ +1)
        pos_count = sum(1 for kw in self.sentiment_keywords['positive'] if kw in text_lower)
        neg_count = sum(1 for kw in self.sentiment_keywords['negative'] if kw in text_lower)
        if pos_count + neg_count > 0:
            features[4] = (pos_count - neg_count) / (pos_count + neg_count)
        
        # [5] 텍스트 길이 정규화
        features[5] = 1 / (1 + np.exp(-len(text) / 50 + 2))
        
        # [6] 숫자/코드 포함 여부
        features[6] = 1.0 if re.search(r'\d+|[(){}\[\]<>]', text) else 0.0
        
        # [7] 전문 용어 밀도
        all_tech_keywords = []
        for cat_info in self.category_keywords.values():
            all_tech_keywords.extend(cat_info['keywords'])
        words = text_lower.split()
        if words:
            tech_density = sum(1 for word in words if any(kw in word for kw in all_tech_keywords)) / len(words)
            features[7] = min(1.0, tech_density * 3)
        
        # [8] 문장 복잡도
        sentences = re.split(r'[.!?]+', text)
        features[8] = min(1.0, len(sentences) / 5)
        
        # [9] 대화 맥락 점수
        polite_markers = ['요', '습니다', '해주', '부탁', '선배', '님']
        features[9] = min(1.0, sum(1 for marker in polite_markers if marker in text_lower) / 3)
        
        return features.reshape(1, -1)