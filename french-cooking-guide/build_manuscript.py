#!/usr/bin/env python3
"""04_manuscript.md + book_manifest.json 통합 빌드."""
import json
from pathlib import Path

ROOT = Path("/Users/tobylee/workspace/ai/book-writer/french-cooking-guide")
CHAP = ROOT / "chapters"

CHAPTER_ORDER = [
    "00_final.md",
    "01_final.md", "02_final.md", "03_final.md", "04_final.md", "05_final.md",
    "06_final.md", "07_final.md", "08_final.md", "09_final.md", "10_final.md",
    "99_final.md",
]

TITLE = "브리즈번의 부엌에서, 프렌치를 시작하자"
SUBTITLE = "한식이 익숙한 우리를 위한 프랑스 가정식 입문"
AUTHOR = "Toby-AI"
VERSION = "1.0.0"

PREFACE = """## 머리말

브리즈번에 살면서 한식은 익숙하고, 일식·이탈리안·미국식 BBQ도 한두 가지는 자신 있게 차려낼 수 있는 사람이 있다. 사워도우를 굽고, 김치를 담그고, 갈비찜의 양념 비율은 손이 안다. 그런데 비스트로 메뉴판의 *Bœuf bourguignon* /뵈프 부르기뇽/ 앞에서는 잠시 머뭇거린다. 한 번도 만들어본 적이 없으니까.

이 책은 그 한 사람을 위한 책이다. 호주 마트에서 구할 수 있는 재료만으로, 모체 소스 4종과 가정식 코어 12종 — 도합 풀 레시피 16개를 차근차근 만들어보는 책. 그중 *식탁에 한 접시로 차려내는* 기준으로는 12가지 요리가 손에 들어온다. Coles와 Woolworths 동선, Sunnybank의 한국·아시아 마트, Brisbane Fish Market의 새벽장, James Street의 deli — 우리가 매주 다니는 그 길 위에서 비스트로 한 접시가 만들어진다.

읽는 법은 자유롭다. 처음부터 차례로 읽으면 *마음·도구·테크닉·소스·요리*의 사다리를 한 칸씩 올라간다. 이미 사워도우를 굽는 손이라면 1·2장은 가볍게 훑고 넘어가도 좋다. 책의 척추는 3장(테크닉)·5장(모체 소스)·7장(braise) 셋이다. 셋만 손에 들어와도 책의 약속은 절반 이상 지켜진다. 그리고 4장의 pan sauce — 매일 저녁의 작은 소스 — 가 그 척추 셋을 잇는 가장 빠른 다리다.

본문에는 사진이 없다. 대신 사진이 풍부한 외부 레시피 링크를 본문에 직접 박아두었다. Serious Eats, RecipeTin Eats, David Lebovitz, BBC Good Food — 모두 단계별 사진이 단단한 출처들이다. 책을 읽다가 손이 멈출 때 그 링크를 열어 사진을 한 번 보고 다시 돌아오면 된다.

자, 같이 시작해보자. 망고나무 잎이 흔들리는 베란다 옆 부엌에서, 양파 한 알을 갈색이 될 때까지 볶는 일부터.

---

"""

AFTERWORD = """# 맺음말

이 책을 끝까지 함께 읽어준 당신께 작은 감사를 전하고 싶다. 첫 페이지에서 *Bœuf bourguignon*을 만든다는 약속이 이제는 약속이 아니라 손에 든 레시피가 됐길 바란다. 두 번째 만들 때 첫 번째보다 나아졌다면 — 그게 이 책의 진짜 결말이다.

이 책은 사람 한 명이 혼자 쓴 책이 아니다. 리서치 단계에서 학술 자료와 호주 식재료 정보를 모은 리서치 에이전트들, 책의 골격과 챕터 흐름을 짠 플래너와 리뷰어, 12개 챕터를 직접 손으로 옮긴 챕터 저술가들, Toby 평어체가 흔들릴 때마다 잡아준 스타일 가디언, 그리고 마지막으로 모든 조각을 한 권으로 묶은 편집자 — 여러 AI 협업자들이 같은 노트를 돌려가며 함께 썼다. 부엌이 한 사람의 공간이 아니라 *brigade*의 공간인 것과 비슷하다. 책 한 권도 그렇게 만들어졌다.

그리고 이 모든 것이 시작될 수 있었던 건, 브리즈번의 부엌에서 한식과 프렌치 사이를 오가며 첫 질문을 던진 한 독자 덕분이다. *“프랑스 요리를 직접 만들어보고 싶다”* — 그 한 줄이 이 책의 모든 단락의 출발점이었다. 다음에 무엇을 만들지는 이제 그 손에 달려 있다.

— Toby-AI, 브리즈번에서

"""


def build_toc():
    return """## 차례

- 머리말
- 프롤로그. 우리가 이 책을 시작한 이유
- 1장. 프렌치 요리는 무엇을 발명했나 — Escoffier에서 Nouvelle까지
- 2장. 도구와 부엌 — 사워도우 베이커가 새로 들여야 할 것
- 3장. 일곱 가지 테크닉 사전 — *sauté*부터 *émulsion*까지
- 4장. Pan sauce — 가장 작고 가장 자주 만드는 소스
- 5장. 5대 모체 소스, 뼈대를 잡아보자
- 6장. 봄·여름의 식탁 — 가벼운 비스트로 네 접시
- 7장. 짧은 쿨 시즌의 식탁 — Braise의 기술과 시간의 요리
- 8장. 보존의 부엌 — 시간을 저장하는 두 방식
- 9장. 식탁의 마무리 — 두 개의 디저트
- 10장. 프렌치는 끝없이 깊다 — 자력 확장의 지도
- 에필로그. 양파를 갈색이 될 때까지 — 우리가 함께 지나온 자리
- 부록 A. 호주 식재료 변환표
- 부록 B. 모체 소스 한눈 매트릭스
- 부록 C. 퀸즐랜드 농산물 월별 캘린더
- 부록 D. 추천 도서·블로그·매장 리스트
- 부록 E. 호주 와인 미니 페어링표
- 맺음말

---

"""


APPENDIX_A = """# 부록 A. 호주 식재료 변환표

본문 박스로 흩어져 있던 치환 정보를 한 곳에 모은 *quick reference*. 정육 컷·유제품·와인·specialty 4섹션.

## 정육 컷

- *Paleron* /팔르롱/ → oyster blade / flat iron (Cleaver's Organic / Vic's PQM)
- *Jarret* /자레/ → beef shin (정육점 부탁 또는 Coles/Woolies *gravy beef*가 가장 가까운 대체)
- *Joue* /주/ → beef cheek (Stewart's·Logan Road Meats 부탁)
- *Onglet* /옹글레/ → hanger steak
- *Bavette* /바베트/ → skirt
- *Magret* /마그레/ → duck breast (Pepe's Ducks·Luv-a-Duck)

## 유제품

- *Crème fraîche* /크렘 프레슈/ → thickened cream + buttermilk 24h, 또는 Tatura·Schulz 브랜드 (Black Pearl Epicure·Rosalie Gourmet)
- *Beurre d'Isigny* 84% → Pepe Saya 82% / Lurpak 80%
- *Gruyère*·*Comté* → Black Pearl Epicure / James Street Market

## 와인·증류주

- *Cognac* /코냑/ → Brandy → Australian Grand Brut
- *Pinot Noir* 권장 호주 산지: Mornington, Yarra (Dan Murphy's·1st Choice 브리즈번 매장 안정 입고)

## specialty

- *Pearl onion* → pickling onion / 양파 wedge
- *메밀가루* → Sunnybank Plaza·Yuan's·K-Mart Korean Mart (Sunnybank Hills) / Bob's Red Mill 보조
- *Duck fat* → Black Pearl Epicure 통 / lard + olive oil 6:4
- *호주 mussel* → Brisbane Fish Market·Manettas (online)

---

"""

APPENDIX_B = """# 부록 B. 모체 소스 한눈 매트릭스

| 모체 | 베이스 | 주요 파생 | 가정 사용 빈도 |
|---|---|---|---|
| *Béchamel* /베샤멜/ | 우유 + white roux | *Mornay*, *Soubise* | 높음 |
| *Velouté* /블루테/ | white stock + blond roux | *Suprême*, *Allemande* | 중간 |
| *Espagnole* /에스파뇰/ | brown stock + brown roux | *Bordelaise*, *Demi-glace* | 낮음 (가정) |
| *Tomate* /토마트/ | 토마토 베이스 | *Provençale*, *Portugaise* | 높음 |
| *Hollandaise* /올랑데즈/ | 노른자 + 정제 버터 + 산 | *Béarnaise*, *Mousseline*, *Maltaise* | 중간 |

---

"""

APPENDIX_C = """# 부록 C. 퀸즐랜드 농산물 월별 캘린더

리서치 4계절 표를 **QLD 기준 12개월 그리드**로 재가공. 각 달에 추천 프렌치 프로젝트 1~2개.

**핵심 QLD 차이 (시드니·멜번 캘린더와 다른 점):**

- **망고 (Kensington Pride·R2E2·Calypso) — 9월~2월**, 호주 망고의 본산. *Tarte aux mangues caramélisées* 변주를 강력 추천한다.
- **람부탄·망고스틴·파파야** — 시드니보다 흔하다. 12~3월 풀시즌.
- **Stone fruit** (복숭아·자두·살구) — 시드니보다 시즌이 짧고 약함 (대부분 NSW·VIC산 수입).
- **사과·배** — 입수 가능하나 대부분 빅토리아·태즈매니아산. *Tarte Tatin*은 그대로 가능 (Pink Lady·Granny Smith 안정).
- **토마토·바질·zucchini** — 거의 연중 가능 (브리즈번 가정 텃밭에서도 잘 자람). 라따투이의 토마토는 *제철과 정확히 겹친다*.
- **Moreton Bay bug** (QLD 특산) — 11~3월. *Bouillabaisse* 자력 확장 시 변주 가능.
- **저녁 9 °C까지 떨어지는 쿨 시즌** — 5~8월 (3~4달). braise·confit 시즌은 시드니보다 짧고 온화하다.

| 월 | QLD 풀시즌 | 추천 프렌치 프로젝트 |
|---|---|---|
| 1월 (한여름) | 망고·토마토·바질·zucchini·옥수수 | *Salade Niçoise*, *Ratatouille*, *Tarte aux mangues* |
| 2월 | 망고·복숭아·라즈베리·바질 | *Quiche Lorraine* (저녁), *Crêpes Suzette* |
| 3월 (가을 진입) | 토마토·파프리카·가지·무화과 | *Ratatouille* (시즌 마지막), *Moules Marinières* |
| 4월 | 사과·배·버섯·시금치 | *Quiche aux champignons*, *Pâte brisée* 연습 |
| 5월 (쿨 시즌 시작) | 양파·리크·당근·brassicas | *Soupe à l'oignon gratinée* 시작 |
| 6월 | 양파·감자·리크·오렌지 | *Coq au Vin*, *Gratin Dauphinois* |
| 7월 (한겨울) | 양파·감자·rutabaga·사과 | *Boeuf Bourguignon*, *Tarte Tatin* |
| 8월 (쿨 시즌 마지막) | 시금치·콜리플라워·리크 | *Confit de canard* (보존 작업) |
| 9월 (봄) | 아스파라거스·딸기·완두콩·망고 시작 | *Hollandaise* + asparagus, *Velouté* 연습 |
| 10월 | 아스파라거스·완두콩·딸기·망고 | *Crêpes au sucre*, *Béchamel* 응용 |
| 11월 (여름 진입) | 토마토·zucchini·바질·체리 | *Salade Niçoise* 시작, *Galette Bretonne* |
| 12월 | 망고·복숭아·체리·토마토 | *Tarte aux mangues*, *Crème Brûlée* |

---

"""

APPENDIX_D = """# 부록 D. 추천 도서·블로그·매장 리스트

### 도서 6권

- Julia Child, *Mastering the Art of French Cooking* — 모든 가정 프렌치의 출발점
- Patricia Wells, *The Food Lover's Guide to Paris* — 비스트로 문화의 풍경
- David Lebovitz, *My Paris Kitchen* — 가정 부엌 친화적 레시피
- Daniel Boulud, *Daniel: My French Cuisine* — 셰프식 정통
- Thomas Keller, *Bouchon* — 비스트로 클래식의 완성도
- Anthony Bourdain, *Les Halles Cookbook* — 경쾌한 가정식 레퍼런스

한국·디아스포라 1권: Eric Kim, *Korean American* — 한식의 손이 새로운 언어를 만나는 좋은 동행

### 블로그·웹사이트 5개

- **Serious Eats** — Kenji López-Alt·Daniel Gritzer의 과학 기반 가이드
- **RecipeTin Eats** (Nagi Maehashi) — 호주 거주자에 가장 가까운 다리. 호주 마트 재료로 검증된 레시피
- **David Lebovitz** (davidlebovitz.com) — 파리 거주 미국인의 정통 가정 프렌치
- **The French Cooking Academy** — 동영상으로 단계 확인하기 좋다
- **Hank Shaw** (honest-food.net) — *Confit de canard* 등 보존 부엌의 깊이

### 호주 specialty 매장 — Brisbane 우선

**Brisbane (본 책 페르소나 거주지):**

- *European deli·charcuterie·cheese:* Black Pearl Epicure (Fortitude Valley), Rosalie Gourmet Market (Paddington), James Street Market (Fortitude Valley), Continental Deli (Mt Gravatt), The Stocked Pantry (online, Brisbane hub)
- *정육 (cuts on request):* Vic's Premium Quality Meat, Cleaver's Organic, Stewart's Quality Meats (Toombul/Brookside), New Farm Deli butcher, Logan Road Meats
- *수산:* Brisbane Fish Market (Hamilton), Samies Girl Seafood (Newstead), Morgan's Seafood (Scarborough), Manettas (online)
- *한국·아시아 식재료:* Sunnybank Plaza, Market Square Sunnybank, Yuan's Supermarket, K-Mart Korean Mart (Sunnybank Hills) — 한국 간장·고추장·참기름·신김치·메밀가루·들기름

**타 도시 (출장·여행 시 참고):** Sydney (Harris Farm·Vic's Meat·Simon Johnson), Melbourne (Mediterranean Wholesalers·Maker & Monger·Cannings), Adelaide (Adelaide Central Market), Perth (Boatshed Market·Mondo Butchers).

---

"""

APPENDIX_E = """# 부록 E. 호주 와인 미니 페어링표

깊이 있는 페어링은 *Halliday Wine Companion*에 맡기고, 책에서는 *quick reference 1페이지*만.

| 요리 | 호주 산지·품종 | 한 줄 이유 |
|---|---|---|
| *Steak au poivre* (4장) | Barossa Shiraz / McLaren Vale Grenache | 후추·코냑 크림에 묵직한 탄닌 |
| *Béchamel* 그라탕 (5장) | Tasmania Chardonnay (오크 절제) | 우유·치즈에 산미 |
| *Salade Niçoise* (6장) | Languedoc Picpoul / Hunter Verdelho | 안초비·올리브에 짭짤한 미네랄 |
| *Moules Marinières* (6장) | **Adelaide Hills Sauvignon Blanc** (요리에 쓴 와인과 동일) | 조개 즙 sauce에 그대로 |
| *Ratatouille* (6장) | McLaren Vale Grenache / Provence Rosé | 토마토·허브에 가벼운 붉은 과일 |
| *Quiche Lorraine* (6장) | Hunter Semillon (3~5년) | 베이컨·크림에 산미와 lanolin |
| *Coq au Vin* (7장) | Mornington / Yarra Pinot Noir | 요리에 Pinot 썼으니 그대로 |
| *Boeuf Bourguignon* (7장) | Yarra Pinot / Heathcote Shiraz | 부르고뉴식 vs 호주식 두 갈래 |
| *Confit de Canard* (8장) | Clare Valley Riesling (off-dry) | 지방에 산미와 약한 단맛 |
| *Crème Brûlée* (9장) | Rutherglen Muscat | 캐러멜에 호주식 단맛 |

---

"""


def main():
    parts = []
    parts.append(f"# {TITLE}\n## {SUBTITLE}\n\n*{AUTHOR}*\n\n")
    parts.append("---\n\n")
    parts.append(PREFACE)
    parts.append(build_toc())

    for fn in CHAPTER_ORDER:
        path = CHAP / fn
        body = path.read_text(encoding="utf-8").rstrip() + "\n\n---\n\n"
        parts.append(body)

    parts.append(APPENDIX_A)
    parts.append(APPENDIX_B)
    parts.append(APPENDIX_C)
    parts.append(APPENDIX_D)
    parts.append(APPENDIX_E)

    parts.append(AFTERWORD)

    manuscript = "".join(parts)

    out_path = ROOT / "04_manuscript.md"
    out_path.write_text(manuscript, encoding="utf-8")
    print(f"Manuscript saved: {out_path}")
    print(f"Size: {len(manuscript):,} chars / {len(manuscript.encode('utf-8')):,} bytes")

    import uuid
    manifest = {
        "title": TITLE,
        "subtitle": SUBTITLE,
        "author": AUTHOR,
        "language": "ko",
        "version": VERSION,
        "slug": "french-cooking-guide",
        "manuscript": "04_manuscript.md",
        "cover": "cover.png",
        "pub_date": "2026-04-30",
        "identifier": f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'toby-ai/french-cooking-guide/v1.0.0')}",
        "description": "브리즈번 거주 한국인 홈쿡을 위한 프랑스 가정식 입문서. 호주 마트 재료만으로 모체 소스 4종과 가정식 12가지를 만들고, 한식 손이 알던 동작과 프렌치 테크닉의 다리를 매번 짚는다. 평어체·청유형의 동반자 화법으로 풀어쓴 약 11만 자 입문서.",
        "chapters": [
            {"id": "prologue", "title": "우리가 이 책을 시작한 이유", "file": "chapters/00_final.md"},
            {"id": "ch01", "title": "프렌치 요리는 무엇을 발명했나 — Escoffier에서 Nouvelle까지", "file": "chapters/01_final.md"},
            {"id": "ch02", "title": "도구와 부엌 — 사워도우 베이커가 새로 들여야 할 것", "file": "chapters/02_final.md"},
            {"id": "ch03", "title": "일곱 가지 테크닉 사전 — sauté부터 émulsion까지", "file": "chapters/03_final.md"},
            {"id": "ch04", "title": "Pan sauce — 가장 작고 가장 자주 만드는 소스", "file": "chapters/04_final.md"},
            {"id": "ch05", "title": "5대 모체 소스, 뼈대를 잡아보자", "file": "chapters/05_final.md"},
            {"id": "ch06", "title": "봄·여름의 식탁 — 가벼운 비스트로 네 접시", "file": "chapters/06_final.md"},
            {"id": "ch07", "title": "짧은 쿨 시즌의 식탁 — Braise의 기술과 시간의 요리", "file": "chapters/07_final.md"},
            {"id": "ch08", "title": "보존의 부엌 — 시간을 저장하는 두 방식", "file": "chapters/08_final.md"},
            {"id": "ch09", "title": "식탁의 마무리 — 두 개의 디저트", "file": "chapters/09_final.md"},
            {"id": "ch10", "title": "프렌치는 끝없이 깊다 — 자력 확장의 지도", "file": "chapters/10_final.md"},
            {"id": "epilogue", "title": "양파를 갈색이 될 때까지 — 우리가 함께 지나온 자리", "file": "chapters/99_final.md"},
        ],
        "appendices": [
            {"id": "appendix-a", "title": "호주 식재료 변환표"},
            {"id": "appendix-b", "title": "모체 소스 한눈 매트릭스"},
            {"id": "appendix-c", "title": "퀸즐랜드 농산물 월별 캘린더"},
            {"id": "appendix-d", "title": "추천 도서·블로그·매장 리스트"},
            {"id": "appendix-e", "title": "호주 와인 미니 페어링표"},
        ],
    }
    manifest_path = ROOT / "book_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Manifest saved: {manifest_path}")


if __name__ == "__main__":
    main()
