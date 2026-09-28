#!/usr/bin/env python3
"""Assemble 04_manuscript.md from chapter finals + editor edits + front/back matter.

Chapter finals are never modified; every editor change is an exact, counted
replacement applied here so the diff is auditable.
"""
import os
import re
import sys

BOOK = "/Users/tobylee/workspace/ai/book-writer/software-factory"
CH = os.path.join(BOOK, "chapters")
SP = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(CH, name), encoding="utf-8") as f:
        return f.read()


def rep(text, old, new, count=1, where=""):
    n = text.count(old)
    if n != count:
        sys.exit(f"[{where}] expected {count} match(es), found {n}: {old[:80]!r}")
    return text.replace(old, new)


def promote_h3(text):
    """### -> ## for lines outside fenced code blocks."""
    out, fence = [], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if not fence and ln.startswith("### "):
            ln = "## " + ln[4:]
        out.append(ln)
    return "\n".join(out)


EDITS = {
    "02_final.md": [
        ("프로덕션 배포", "운영 배포", 3),
    ],
    "05_final.md": [
        ("연구는 신중하라고 말한다. MAST 연구(NeurIPS 2025)는 7개 다중 에이전트 프레임워크의 실행 기록 1,600개 이상을 분석해 실패 모드 14개를 찾았고, 그것들을 시스템 설계 문제, 에이전트 사이의 어긋남, 과제 검증 실패라는 세 범주로 묶었다. 초록의 한 문장이 요지를 말한다. 다중 에이전트 시스템에 대한 열기와 달리 벤치마크에서 얻는 성능 이득은 대개 미미하다.",
         "연구는 신중하라고 말한다. 1장에서 만난 MAST 연구(NeurIPS 2025)를 다시 꺼내 보자. 이 연구는 실패 모드 14개를 시스템 설계 문제, 에이전트 사이의 어긋남, 과제 검증 실패라는 세 범주로 묶었고, 멀티 에이전트 시스템에 대한 열기와 달리 벤치마크에서 얻는 성능 이득은 대개 미미하다고 결론지었다.", 1),
        ("반대 방향의 사례도 있다. Agentless는 LLM에게 다음 행동을 고르게 하지 않았다. 위치 파악, 수리, 검증이라는 고정된 3단계 파이프라인을 돌렸을 뿐인데, 게재판 기준 SWE-bench Lite에서 32.00%를 과제당 0.70달러에 냈다. 당시 오픈소스 에이전트들 가운데 최고 수준이었다(당시 모델 기준).",
         "반대 방향의 사례도 1장에서 봤다. Agentless는 LLM에게 다음 행동을 고르게 하지 않고 위치 파악, 수리, 검증이라는 고정된 3단계 파이프라인만 돌렸는데도, 당시 오픈소스 에이전트들보다 높은 성능을 더 적은 비용으로 냈다(당시 모델 기준).", 1),
        ("에이전트 뷰는 연구 미리보기 단계다", "에이전트 뷰는 리서치 프리뷰 단계다", 1),
    ],
    "06_final.md": [
        ("Simon Willison이 StrongDM 사례를 보며 던진 질문이 정확히 이 장면을 겨냥한다.",
         "1장에서 Simon Willison이 StrongDM 사례를 보며 던진 첫 번째 질문이 정확히 이 장면을 겨냥한다.", 1),
        ("Anthropic의 에이전트 평가 글은 회귀 평가의 통과율은", "Anthropic의 에이전트 평가 글은 회귀 eval의 통과율은", 1),
        ("(둘 다 2026년 9월 기준 연구 미리보기 기능이다)", "(둘 다 2026년 9월 기준 리서치 프리뷰 기능이다)", 1),
        ("| 6 | 회귀 평가 |", "| 6 | 회귀 eval |", 1),
        ("| 8 | 부수는 확인 |", "| 8 | 화면 확인 |", 1),
    ],
    "07_final.md": [
        ('`gather`로 치면 "결제·환불 로직은 건드리지 않는다"나', '`gather`로 치면 "회원 개인정보는 로그와 PR 코멘트에 남기지 않는다"나', 1),
        ("- 결제·환불 로직을 건드리지 않는다.\n", "- 승격 알림은 outbox 기록까지만 한다. jobs의 발송 로직은 건드리지 않는다.\n", 1),
        ("다중 에이전트 SDD 파이프라인", "멀티 에이전트 SDD 파이프라인", 1),
    ],
    "08_final.md": [
        ("Agent HQ는 2026년 2월에 공개 미리보기로 나왔다", "Agent HQ는 2026년 2월에 퍼블릭 프리뷰로 나왔다", 1),
        ("커피를 한 모금 마시고 #41의 프리뷰 URL부터 눌러 본다.", "#41의 프리뷰 URL부터 눌러 본다.", 1),
    ],
    "09_final.md": [
        ("새벽 1시 12분, `gather` 저장소의", "새벽 3시 40분, `gather` 저장소의", 1),
        ("8장에서 PR마다 올린 Cloudflare Workers의 Version URL은 켜 두면 공개된다.",
         "8장에서 PR마다 올린 Cloudflare Workers의 Preview는 기본으로 누구나 접근할 수 있다.", 1),
        ("| 구현 에이전트 | 승인된 계획, 저장소 코드 | 저장소 읽기, 모델 키 | 모델 API | 있음 |",
         "| 구현 에이전트 | 사람 게이트 1을 거친 계획, 저장소 코드 (이슈 본문은 넘기지 않음) | 브랜치·draft PR 쓰기(Claude GitHub 앱 인증, `id-token: write`), 모델 키 | 모델 API, 자기 브랜치·draft PR | 있음 |", 1),
        ("| 프리뷰 배포 | PR 빌드 산출물 | Cloudflare 프리뷰 배포 권한 | Cloudflare (Access 보호) | 없음 |",
         "| 프리뷰 배포 | PR 빌드 산출물 | `CLOUDFLARE_API_TOKEN`·`CLOUDFLARE_ACCOUNT_ID`, PR 코멘트 쓰기 | Cloudflare (Access 보호) | 없음 |", 1),
        ("| 운영 배포 (사람 게이트 2 이후) | 사람이 머지한 `main` | AWS OIDC 단기 토큰, Cloudflare 배포 권한 |",
         "| 운영 배포 (사람 게이트 2·3 이후) | 사람이 머지한 `main` | AWS OIDC 단기 토큰(`id-token: write`), Cloudflare 배포 권한 |", 1),
        ("표의 모양이 원칙을 말해 준다. 모델이 있는 줄에는 쓰기 권한도 수명이 긴 비밀도 없고, 나갈 곳은 모델 API뿐이다. 쓰기나 배포 권한이 있는 줄에는 모델이 없다.",
         "표의 모양이 원칙을 말해 준다. 남이 쓴 글을 읽는 모델 잡에는 쓰기 권한도 수명이 긴 비밀도 없고, 나갈 곳은 모델 API뿐이다. 배포 권한이 있는 줄에는 모델이 없다. 모델이 있으면서 쓰기 권한을 쥔 줄은 구현 에이전트 하나다. draft PR을 열려면 쓰기 권한이 필요한데, PAT 대신 Claude GitHub 앱 인증으로 받는다(8장에서 넣은 `id-token: write`). 대신 이슈 본문은 넘기지 않고 사람 게이트 1을 거친 계획과 저장소 코드에서만 출발하게 해, 삼박자의 다리 하나를 뺐다.", 1),
    ],
    "10_final.md": [
        ("2부에서 혼자 4단계까지 올린 `gather`가 자랐다. 가상의 8인 팀이 이 서비스를 맡는다.",
         "2부에서 혼자 4단계까지 올린 `gather`가 자랐다. 유료 모임이 생기면서 참가비 결제와 환불도 받게 됐고, 가상의 8인 팀이 이 서비스를 맡는다.", 1),
        ("2026년 9월 기준 research preview라", "2026년 9월 기준 리서치 프리뷰라", 1),
    ],
    "11_final.md": [
        ("4장에서 Boris Cherny가 Claude가 틀릴 때마다 CLAUDE.md에 한 줄씩 보탰던 습관의 팀 버전이다.",
         "4장에서 본 Boris Cherny 팀의 습관, 곧 Claude가 틀릴 때마다 CLAUDE.md에 한 줄씩 보태는 습관을 여러 저장소와 도구가 함께 쓰는 하네스로 넓힌 셈이다.", 1),
    ],
    "13_final.md": [
        ('"알린다"는 다이제스트로 구현한다. 모델이 이 표를 잊어도 워크플로는 잊지 않는다.',
         '"알린다"는 다이제스트로 구현한다. 8장의 `factory:*` 라벨 체계에 라벨 둘을 더하는 셈이다. 거부권 기한이 걸린 PR에는 `factory:veto`를, 사람의 결정을 기다리는 항목에는 `factory:needs-decision`을 붙인다. 모델이 이 표를 잊어도 워크플로는 잊지 않는다.', 1),
        ("Igor Ostrovsky는 모든 변경에 사람 승인이 필요한 구조라도 1인 프로젝트에서 충분히 돌아간다고 말한다(커뮤니티 경유).",
         "8장에서 본 Igor Ostrovsky의 말대로, 모든 변경에 사람 승인이 필요한 구조라도 1인 프로젝트는 충분히 돌아간다(커뮤니티 경유).", 1),
        ("그 사이 어디에 설지 정하는 도구가 바로 앞에서 만든 결정 분류표다.", "그 사이 어디에 설지 정하는 도구가 앞에서 만든 결정 분류표다.", 1),
        ("- 에이전트 추천: B (근거: docs/specs/reservation-cancel.md의 '경계' 절)",
         "- 에이전트 추천: B (근거: docs/specs/reservation-cancel.md의 '규칙' 절 2번)", 1),
        ("CRP가 바로 그 출구에 붙이는 정식 양식이다.", "CRP는 그 출구에 붙이는 정식 양식이다.", 1),
        ("반대편의 목소리도 분명하다. MAST 연구는 7개 멀티 에이전트 프레임워크의 실행 기록 1,600여 건에서 실패 모드 14개를 찾아내고, 널리 쓰이는 벤치마크에서 멀티 에이전트의 성능 이득이 대개 미미하다고 보고했다(당시 모델 기준).",
         "반대편의 목소리도 분명하다. 1장과 5장에서 본 MAST 연구는 널리 쓰이는 벤치마크에서 멀티 에이전트의 성능 이득이 대개 미미하다고 보고했다(당시 모델 기준).", 1),
        (" 1. [명세] 대기자 자동 승격 때 알림을 보낼까? — 선택지 2개, 추천 A",
         " 1. [명세] 대기자가 승격되면 모임 개설자에게도 알릴까? — 선택지 2개, 추천 A", 1),
    ],
    "14_final.md": [
        ("### `gather`의 조명 지도", "### gather의 조명 지도", 1),
    ],
    "15_final.md": [
        ("책 곳곳에서 만난 세 가지 부채도 결국 같은 이야기다. 처음부터",
         "10장에서 만난 부채들도 결국 같은 이야기다. 거기서는 당근 박용권의 분류대로 기술·인지·의도 부채를 봤는데, 드물게 불려 가는 사람의 자리에서 보면 세 이름이 더 또렷해진다. 처음부터", 1),
    ],
    "appendix_a_final.md": [
        ('| Wrangler(Workers Version URL용) | v4.21.0 이상 | 기능 발표 2025-07-22 | 문서 명칭이 "preview URLs"에서 "Version URLs"로 바뀜 |',
         "| Wrangler(Workers Preview용) | v4.135.0 이상 | — | `wrangler preview`로 PR마다 Preview를 만든다. 이름이 비슷한 Version URL(옛 이름 preview URL)은 운영 리소스를 쓰므로 PR 테스트에는 쓰지 않는다 |", 1),
        ('Ralph 공식 플러그인의 `/ralph-loop "<작업>" --completion-promise "COMPLETE" --max-iterations 50`',
         'Ralph 공식 플러그인의 `/ralph-loop "<작업>" --completion-promise "<약속 문자열>" --max-iterations <상한>`', 1),
        ("`wrangler preview delete`, `wrangler versions upload --preview-alias`, Codex의", "`wrangler preview delete`, Codex의", 1),
        ("| Cloudflare Workers Version URLs | `developers.cloudflare.com/workers/configuration/previews/` | |",
         "| Cloudflare Workers Previews | `developers.cloudflare.com/workers/previews/` | Version URL 문서는 `developers.cloudflare.com/workers/configuration/previews/` |", 1),
        ("research preview", "리서치 프리뷰", 2),
    ],
    "appendix_b_final.md": [
        ("| 흐름 | 계획 코멘트 → 사람 게이트 1(라벨로 승인) → 구현 잡 → CI(계산적 센서) → 교차 리뷰 → 프리뷰 → 홀드아웃·E2E → draft PR → 사람 게이트 2(머지) → 배포 |",
         "| 흐름 | 계획 코멘트 → 사람 게이트 1(라벨로 승인) → 구현 잡 → draft PR → CI(계산적 센서) → 교차 리뷰·프리뷰 → 홀드아웃·E2E → 사람 게이트 2(머지) → 배포(`api` 운영 배포는 사람 게이트 3) |", 1),
        ("| 트리거 | PR 열림·갱신 |", "| 트리거 | PR 열림·갱신(`gather`는 CI 통과 뒤) |", 1),
        ("| 대표 도구 | Cloudflare Workers Version URL, AWS Amplify PR 프리뷰. Version URL은 공개이니 Cloudflare Access로 보호하고, Durable Object를 쓰는 Worker에는 생성되지 않는다. Amplify는",
         "| 대표 도구 | Cloudflare Workers Preview(`wrangler preview`, Wrangler 4.135.0 이상), AWS Amplify PR 프리뷰. Preview URL은 기본으로 공개이니 Cloudflare Access로 보호한다. 이름이 비슷한 Version URL은 운영 리소스를 쓰므로 PR 테스트에는 쓰지 않는다. Amplify는", 1),
        ("2026-02 발표 기준 public preview", "2026-02 발표 기준 퍼블릭 프리뷰", 1),
        ("(API 트리거, research preview)", "(API 트리거, 리서치 프리뷰)", 1),
    ],
}

PROMOTE = {"13_final.md", "14_final.md", "15_final.md"}

PARTS = {
    "01_final.md": """# 1부. 팩토리라는 생각

팩토리가 무엇이고 이미 가진 CI/CD와 무엇이 다른지, 에이전트에게 얼마나 맡길지를 무엇으로 정하는지, 모델과 도구를 어디에 배치할지를 다룬다. 뒤의 모든 장이 쓰는 어휘와 지도가 여기서 나온다.
""",
    "04_final.md": """# 2부. 한 사람의 팩토리 — 사다리 오르기

혼자 일하는 개발자가 2장에서 소개한 가상의 예약 서비스 `gather` 하나로 1단계에서 4단계까지 오른다. 장마다 이 저장소에 부품이 하나씩 쌓인다. 지침 파일과 첫 훅, 루프, 검증 게이트, 명세, 이슈에서 배포까지 가는 파이프라인, 그리고 그 파이프라인을 가두는 담장이다.
""",
    "10_final.md": """# 3부. 여럿의 팩토리 — 팀으로 확장하기

팀의 문제는 개인 단계의 연장이 아니다. 모두가 빨라졌는데 팀이 막히는 리뷰 병목에서 출발해, 팀이 팩토리를 들이는 순서와 공유 하네스, 여러 저장소와 여러 사람이 함께 쓰는 중앙 플랫폼과 비용을 다룬다. 혼자 일하는 독자에게도 리뷰 부채의 이야기는 그대로 통한다.
""",
    "13_final.md": """# 4부. 사람은 필요할 때만

1인과 팀, 두 길이 5단계에서 만난다. 팩토리가 언제 누구를 무엇을 들고 부를지 정하고, 1장의 선언으로 돌아가 다크 팩토리 논쟁을 판정하고, 드물게 불려 가는 사람이 판단력을 지키는 법을 묻는다.
""",
}

ORDER = [f"{i:02d}_final.md" for i in range(1, 16)]


def chapter(name):
    t = load(name)
    for old, new, cnt in EDITS.get(name, []):
        t = rep(t, old, new, cnt, name)
    if name in PROMOTE:
        t = promote_h3(t)
    return t.rstrip("\n") + "\n"


def main():
    parts = []
    parts.append(open(os.path.join(SP, "front.md"), encoding="utf-8").read().rstrip("\n") + "\n")
    for name in ORDER:
        if name in PARTS:
            parts.append(PARTS[name])
        parts.append(chapter(name))
    parts.append(open(os.path.join(SP, "epilogue.md"), encoding="utf-8").read().rstrip("\n") + "\n")
    parts.append(chapter("appendix_a_final.md"))
    parts.append(chapter("appendix_b_final.md"))
    rp = os.path.join(SP, "references.md")
    refs = open(rp, encoding="utf-8").read().strip("\n") if os.path.exists(rp) else "[미완성]"
    parts.append("# 참고문헌\n\n" + refs + "\n")
    out = "\n".join(parts)
    with open(os.path.join(BOOK, "04_manuscript.md"), "w", encoding="utf-8") as f:
        f.write(out)
    # per-chapter split of the integrated text for the length report
    split_dir = os.path.join(SP, "lr", "software-factory", "chapters")
    os.makedirs(split_dir, exist_ok=True)
    for name in ORDER:
        with open(os.path.join(split_dir, name), "w", encoding="utf-8") as f:
            f.write(chapter(name))
    print("ok", len(out))


if __name__ == "__main__":
    main()
