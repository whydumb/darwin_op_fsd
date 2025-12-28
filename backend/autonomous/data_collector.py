"""
자율 데이터 수집 시스템 - 한국어 최적화 및 안전 모드
"""

import time
import random
import re
from typing import List, Dict, Optional

# DuckDuckGo 안전 임포트 (새/구 버전 모두 지원)
try:
    from ddgs import DDGS
    print("✅ 새 DDGS 패키지 사용")
except ImportError:
    try:
        from duckduckgo_search import DDGS
        print("⚠️ 구 duckduckgo-search 패키지 사용 (업데이트 권장)")
    except ImportError:
        print("❌ DuckDuckGo 검색 모듈을 찾을 수 없습니다.")
        DDGS = None

# Wikipedia 안전 임포트
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
    print("✅ Wikipedia 패키지 사용 가능")
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️ Wikipedia 패키지가 없습니다. DuckDuckGo만 사용합니다.")

class AutonomousDataCollector:
    """독립적 데이터 수집 시스템 - 한국어 최적화"""
    
    def __init__(self):
        self.search_engines = {}
        
        if DDGS:
            self.search_engines['duckduckgo'] = self._search_duckduckgo
        
        if WIKIPEDIA_AVAILABLE:
            self.search_engines['wikipedia'] = self._search_wikipedia
        
        self.search_history = []
    
    def autonomous_search(self, query: str, depth: str = 'moderate') -> Dict:
        """자율적 정보 수집 - 한국어 특화"""
        print(f"🔍 [자율 탐색] '{query}' 조사 시작...")
        
        collected_data = {}
        search_strategies = self._generate_search_strategies(query, depth)
        
        for strategy in search_strategies:
            engine = strategy['engine']
            search_query = strategy['query']
            
            try:
                if engine in self.search_engines:
                    results = self.search_engines[engine](search_query)
                    if results:
                        collected_data[f"{engine}_{search_query[:20]}"] = results
                        print(f"   ✅ {engine}: {len(results)}개 결과 수집")
                    else:
                        print(f"   ⚠️ {engine}: 결과 없음")
                    
                    time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"   ⚠️ {engine} 오류: {e}")
        
        # 한국어 최적화된 데이터 처리
        processed_data = self._process_and_evaluate_korean(collected_data, query)
        
        return {
            'query': query,
            'strategies_used': len(search_strategies),
            'raw_data': collected_data,
            'processed_data': processed_data,
            'quality_score': self._calculate_quality_score(processed_data)
        }
    
    def _generate_search_strategies(self, query: str, depth: str) -> List[Dict]:
        """한국어 검색 전략 생성"""
        base_strategies = [
            {'engine': 'duckduckgo', 'query': query},
        ]
        
        if WIKIPEDIA_AVAILABLE:
            base_strategies.append({'engine': 'wikipedia', 'query': query})
        
        if depth == 'deep':
            # 한국어 특화 검색어 확장
            additional_strategies = [
                {'engine': 'duckduckgo', 'query': f"{query} 뜻"},
                {'engine': 'duckduckgo', 'query': f"{query} 의미"},
                {'engine': 'duckduckgo', 'query': f"{query}이란"},
            ]
            base_strategies.extend(additional_strategies)
        
        return base_strategies
    
    def _search_duckduckgo(self, query: str) -> List[Dict]:
        """DuckDuckGo 검색"""
        if not DDGS:
            return []
            
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=8))
            
            return [
                {
                    'title': r.get('title', ''),
                    'content': r.get('body', ''),
                    'url': r.get('href', ''),
                    'source': 'duckduckgo'
                }
                for r in results if r.get('body', '').strip()
            ]
        except Exception as e:
            print(f"DuckDuckGo 검색 실패: {e}")
            return []
    
    def _search_wikipedia(self, query: str) -> List[Dict]:
        """위키피디아 검색"""
        if not WIKIPEDIA_AVAILABLE:
            return []
        
        try:
            wikipedia.set_lang('ko')
            search_results = wikipedia.search(query, results=3)
            
            contents = []
            for title in search_results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    if page.summary.strip():
                        contents.append({
                            'title': page.title,
                            'content': page.summary,
                            'full_content': page.content[:2000],
                            'url': page.url,
                            'source': 'wikipedia'
                        })
                except Exception:
                    continue
            
            return contents
        except Exception as e:
            print(f"Wikipedia 검색 실패: {e}")
            return []
    
    def _process_and_evaluate_korean(self, raw_data: Dict, query: str) -> List[Dict]:
        """한국어 최적화된 데이터 처리"""
        processed = []
        seen_titles = set()
        
        for source_key, data_list in raw_data.items():
            for item in data_list:
                if not isinstance(item, dict):
                    continue
                
                title = item.get('title', '')
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                
                content = item.get('content', '') + ' ' + item.get('full_content', '')
                cleaned_content = self._clean_korean_text(content)
                
                if len(cleaned_content.strip()) < 10:  # 너무 짧은 내용 제외
                    continue
                
                # 한국어 특화 관련성 계산
                relevance_score = self._calculate_korean_relevance(cleaned_content, query)
                
                print(f"   📊 '{title[:30]}...' - 관련도: {relevance_score:.3f}")
                
                # 임계값을 0.1로 대폭 완화 (한국어 특성 고려)
                if relevance_score > 0.1:
                    processed.append({
                        'source': item.get('source', 'unknown'),
                        'title': title,
                        'content': cleaned_content[:1200],
                        'url': item.get('url', ''),
                        'relevance_score': relevance_score,
                        'word_count': len(cleaned_content.split())
                    })
        
        processed.sort(key=lambda x: x['relevance_score'], reverse=True)
        print(f"   📈 데이터 정제: 원본 {len(seen_titles)}개 → 유효 {len(processed)}개")
        
        return processed[:8]  # 상위 8개 보존
    
    def _clean_korean_text(self, text: str) -> str:
        """한국어 텍스트 정제"""
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        # 한글, 영문, 숫자, 기본 문장부호만 보존
        text = re.sub(r'[^\w\s가-힣.,!?():-]', '', text)
        
        return text.strip()
    
    def _calculate_korean_relevance(self, content: str, query: str) -> float:
        """한국어 최적화 관련성 계산"""
        if not content or not query:
            return 0.0
            
        content_lower = content.lower()
        query_lower = query.lower()
        
        # 1. 직접 포함 검사 (가장 높은 점수)
        if query_lower in content_lower:
            # 쿼리가 제목이나 첫 문장에 있으면 보너스
            first_part = content_lower[:200]
            if query_lower in first_part:
                return 0.9
            return 0.7
        
        # 2. 조사 제거 후 어근 매칭
        query_stem = self._remove_korean_particles(query_lower)
        content_stems = self._remove_korean_particles(content_lower)
        
        if query_stem in content_stems:
            return 0.6
        
        # 3. 단어별 부분 매칭
        query_words = query_lower.split()
        match_count = 0
        total_words = len(query_words)
        
        for word in query_words:
            word_stem = self._remove_korean_particles(word)
            if word in content_lower or word_stem in content_stems:
                match_count += 1
        
        if total_words > 0:
            partial_score = (match_count / total_words) * 0.5
            return partial_score
        
        return 0.0
    
    def _remove_korean_particles(self, text: str) -> str:
        """한국어 조사 제거 (간단한 버전)"""
        # 자주 사용되는 조사들 제거
        particles = ['은', '는', '이', '가', '을', '를', '의', '에', '에서', '로', '으로', '와', '과', '한테', '께']
        
        for particle in particles:
            text = text.replace(particle, '')
        
        return text
    
    def _calculate_quality_score(self, processed_data: List[Dict]) -> float:
        """품질 점수 계산"""
        if not processed_data:
            return 0.0
        
        total_score = sum(item['relevance_score'] for item in processed_data)
        source_diversity = len(set(item['source'] for item in processed_data))
        
        return (total_score / len(processed_data)) * (1 + source_diversity * 0.1)
