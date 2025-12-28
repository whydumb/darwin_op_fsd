"""
시스템 통합 테스트 스크립트 - 경로 문제 해결 포함
"""

import sys
import os

# 경로 문제 해결
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_path = os.path.join(project_root, 'backend')

print(f"🔍 프로젝트 루트: {project_root}")
print(f"🔍 백엔드 경로 추가: {backend_path}")

# Python 경로에 추가
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

def test_imports():
    """모든 모듈 임포트 테스트"""
    print("\n🧪 모듈 임포트 테스트 시작...")
    
    tests = []
    
    # 신경망 모듈 테스트
    try:
        from neural_network.growing_network import SelfGrowingNeuralNetwork
        print("✅ 신경망 모듈")
        tests.append(True)
    except Exception as e:
        print(f"❌ 신경망 모듈: {e}")
        tests.append(False)
    
    # 특징 추출기 테스트
    try:
        from neural_network.feature_extractor import IRORobotFeatureExtractor
        print("✅ 특징 추출기")
        tests.append(True)
    except Exception as e:
        print(f"❌ 특징 추출기: {e}")
        tests.append(False)
    
    # 데이터베이스 테스트
    try:
        from knowledge_base.database import KnowledgeDatabase
        print("✅ 데이터베이스")
        tests.append(True)
    except Exception as e:
        print(f"❌ 데이터베이스: {e}")
        tests.append(False)
    
    success_rate = sum(tests) / len(tests) * 100
    print(f"\n📊 테스트 결과: {sum(tests)}/{len(tests)} 성공 ({success_rate:.1f}%)")
    
    return all(tests)

if __name__ == "__main__":
    if test_imports():
        print("🎉 모든 모듈이 정상적으로 로드되었습니다!")
    else:
        print("⚠️ 일부 모듈에 문제가 있습니다.")
