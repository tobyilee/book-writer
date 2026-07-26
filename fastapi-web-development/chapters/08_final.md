# 8장. 오래 걸리는 일 — 스케줄링, 백그라운드 작업, 태스크 큐, 대용량 업로드

리포트 생성 버튼을 누르면 12초가 걸린다고 해보자. 프로젝트 하나의 이번 주 이슈를 전부 훑어 상태별로 세고 담당자별로 묶어 파일로 굽는다. 서버 입장에서 12초는 별일이 아니다. 그런데 화면 앞에 앉은 사람에게는 영원이고, 그 12초를 로드 밸런서가 참아줄지 프록시가 먼저 끊을지는 우리 손 밖이다.

답 자체는 이미 알고 있다. 응답은 지금 돌려주고 일은 뒤에서 한다. 예전 같으면 메서드에 비동기 실행 애너테이션 하나를 붙이고 끝냈을 것이다. FastAPI에도 그 자리를 채우는 물건이 있다. `BackgroundTasks`라는 이름이고, 쓰는 법은 정말로 한 줄이다.

문제는 그 한 줄이 무엇을 약속하고 무엇을 약속하지 않는지다. 12초짜리 리포트를 거기 얹어도 되는가? 그리고 이 일을 매주 월요일 아침 아홉 시에 자동으로 돌리고 싶어지면 — 그때부터 이야기가 완전히 달라진다.

## 응답을 보낸 뒤에 남는 것

먼저 계약부터 읽자. FastAPI 공식 문서는 이 기능을 한 문장으로 정의한다. *"You can define background tasks to be run **after** returning a response."* 응답을 돌려준 **다음에** 실행된다는 것. 경로 함수 파라미터로 `BackgroundTasks`를 선언하고, `add_task`에 함수와 인자를 넘기면 등록이 끝난다.[^8-1] 등록한 함수가 `async def`든 `def`든 상관없다 — 문서 축자로 *"It can be an `async def` or normal `def` function, FastAPI will know how to handle it correctly."*다.

그런데 같은 문서가 곧바로 선을 하나 긋는다.

> "If you need to perform heavy background computation and you don't necessarily need it to be run by the same process (for example, you don't need to share memory, variables, etc), you might benefit from using other bigger tools like Celery."

무거운 계산이고 같은 프로세스에서 돌 필요가 없다면 더 큰 도구를 보라는 것. 반대로 *"small background tasks (like sending an email notification)"* 정도라면 이걸로 충분하다고 한다. 공식 문서가 스스로 적용 범위를 좁힌 셈인데, 여기서 중요한 단어는 "heavy"가 아니라 **"the same process"**다.

정리하면 이렇다. 첫째, 태스크는 요청을 처리한 그 워커 프로세스 안에서 돈다. 둘째, 응답이 나간 뒤에 돈다. 셋째, 그러므로 **그 프로세스가 사라지면 태스크도 함께 사라진다.** 세 번째가 무섭다. 배포로 파드를 내리든, 오토스케일러가 인스턴스를 회수하든, 프로세스가 죽는 사건은 평범한 화요일 오후에도 일어난다.

서버가 대비를 안 하는 것은 아니다. uvicorn은 종료 절차에서 *"wait for any background tasks to run to completion"*을 보장한다. 응답은 나갔지만 아직 안 끝난 태스크를 기다려준다는 뜻이다. 다만 그 시간이 유한하다. 유예 시간이 끝나면 서버는 정리를 중단한다. 그래서 이 장은 13장에 요구 조건 하나를 넘겨둔다 — **백그라운드 태스크의 최악 실행 시간보다 종료 유예 시간이 길어야 한다.** 그 숫자를 정하는 일은 배포를 이야기할 자리의 몫이다.

한 가지 더 있다. 태스크가 **조용히 실패하는** 경로다. 응답 바깥에서 도니까 그 안에서 난 예외가 클라이언트에게 전달될 길이 구조적으로 없다. 그리고 실제로 물린 기록이 남아 있다. 이슈 #14137(2025-10)에서 백그라운드 태스크가 도는 방식에 회귀가 보고됐고, tiangolo가 제시한 처방은 `Depends(func, scope="function")`이었다. 4장에서 소개만 하고 넘어간 그 파라미터가 여기서 다시 나온 것이다.

왜 `yield` 의존성의 정리 시점이 백그라운드 태스크와 얽힐까? 순서를 그려보면 보인다. 응답이 나가고, 의존성이 정리되고, 태스크가 돈다 — 이 셋의 앞뒤가 어디서 갈리느냐에 따라 태스크가 손에 쥔 자원이 이미 닫혀 있을 수 있다. 그래서 규칙 하나를 정하자. **응답 뒤에 돌 코드에는 요청의 세션을 물려주지 않는다.** 넘기는 것은 식별자뿐이고, 태스크는 필요한 자원을 자기가 연다. 그리고 로깅도 태스크 안에 직접 넣자 — 밖에서 잡아주는 그물이 있다고 가정하지 말자.

## 어디까지 믿어도 되는가

그렇다면 12초짜리 리포트는 `BackgroundTasks`로 충분할까? 답하려면 "무겁다/가볍다"보다 나은 자가 필요하다. 무게는 사람마다 다르게 느끼지만, **유실됐을 때 무슨 일이 벌어지는가**는 팀이 함께 답할 수 있는 질문이다.

> 아래 네 문항은 **저자 기준**이다. 공식 권장도 업계 표준도 아니라 이 장의 계약 분석에서 도출한 것이며, 팀들이 실제로 어떤 기준으로 갈랐는지에 대한 증언은 리서치에서 찾지 못했다.

하나, 이 일이 사라지면 누가 아쉬운가? 알림 메일 한 통이 안 갔다면 사용자가 다시 누르면 된다. 결제 정산 기록이 안 남았다면 아무도 다시 눌러주지 않는다. **유실이 허용되지 않으면 큐다.** 프로세스와 함께 사라지는 물건에 원장을 맡길 수는 없다.

둘, 실패하면 다시 시도해야 하는가? `BackgroundTasks`에는 재시도도, 실패한 작업을 모아두는 곳도 없다. 직접 만들 수는 있지만, 그러기 시작하면 큐를 절반쯤 다시 짓게 된다.

셋, 몇 초 걸리는가? 앞 절의 종료 유예 시간이 상한이다. 12초짜리 리포트가 걸리는 곳이 여기다 — 유예 시간이 넉넉하면 살고 빠듯하면 죽는데, **"배포 설정에 따라 살기도 하고 죽기도 하는 기능"은 이미 설계가 잘못된 것이다.**

넷, 기다리는 일인가 계산하는 일인가? 5장에서 이 구분을 세우고 결론을 하나 미뤄뒀다 — 썸네일 생성 같은 CPU 바운드 작업을 스레드로 미는 것은 응급 처치일 뿐이라고. 스레드로 옮겨도 프로세스당 40이라는 자리는 그대로고, 계산 작업은 스레드로 옮긴다고 병렬로 돌지도 않는다. **오프로드는 이벤트 루프를 살릴 뿐 용량을 만들지 못한다.** 그러니 CPU를 진짜로 쓰는 일의 답은 처음부터 하나였다. 프로세스 밖으로 내보내는 것.

하나라도 걸리면 큐로 넘어간다. 하나도 안 걸리면 `BackgroundTasks`가 정답이다 — 브로커도 워커 배포도 없이 한 줄로 끝나는 선택지를 괜히 버릴 이유는 없다.

## 큐로 넘길 때 무엇을 보고 고를까

넘어가기로 했다고 하자. 파이썬 진영의 태스크 큐는 2026-07 기준 최근 릴리스 시점이 이렇다. Celery 5.6.3(2026-03) · arq 0.28.0(2026-04) · TaskIQ 0.12.4(2026-05) · Dramatiq 2.2.0(2026-06) · RQ 2.10.0(2026-06).

Node에서 Bull·BullMQ·Agenda를 붙이던 자리에 이 목록이 온다고 보면 된다. 여기서 어느 것이 낫다고 말하지는 않겠다. 이 책의 리서치에는 팀들이 무엇을 골랐고 왜 후회했는지에 대한 근거가 없고, 없는 근거로 서열을 매기지는 않기로 했다. 대신 **무엇을 보고 고를지**는 말할 수 있다. 다음 축들은 **저자 기준**이다.

- 우리 앱의 비동기 모델과 맞물리는가. 태스크 함수가 앱 코드를 임포트하는 순간 실무 문제가 된다. 6장에서 만든 것은 `AsyncSession`인데, 태스크 실행기가 코루틴을 직접 돌려주지 않으면 태스크 안에서 이벤트 루프를 따로 띄우거나 동기 세션을 하나 더 유지해야 한다. **데이터 계층을 두 벌 갖게 되는 것이 이 선택의 진짜 비용이다.**
- 브로커로 무엇을 요구하는가. 7장에서 이미 들여온 것이 있다면, 같은 것을 쓸 수 있는지부터 보는 편이 낫다. 운영할 미들웨어가 하나 느는 것은 생각보다 큰 결정이다.
- 재시도·데드레터·멱등성의 계약이 어떻게 생겼는가. 몇 번 다시 시도하는지, 끝내 실패한 작업이 어디로 가는지, 같은 작업이 두 번 실행돼도 안전한지. 마지막 항목은 도구가 아니라 우리 코드가 답해야 한다.
- 주기 실행이 내장돼 있는가. 다음 절의 주제이며, 여기에 답이 있으면 스케줄러를 따로 세우지 않아도 된다.
- 운영 중에 안이 보이는가. 대기 중인 작업 수, 실패 목록, 워커 상태. 없으면 큐는 블랙박스다.

Celery에 대해서는 한 가지를 정직하게 밝혀둔다. 이 책은 **Celery의 asyncio 네이티브 지원 여부에 대한 공식 진술을 확보하지 못했다.** 확인한 것은 정황뿐이다 — Celery 공식 문서의 concurrency 옵션 목록은 prefork · Eventlet · gevent · thread · solo이고, 그 목록에 asyncio 풀이 없다. 정황은 진술이 아니므로 여기서 멈춘다. 덧붙여 공식 문서는 5.5.x가 Python 3.8–3.13에서 돈다고 적어두고 있는데 PyPI 최신은 5.6.3이다. **5.6.x의 지원 범위**는 이 책이 확인하지 못했다. 도입을 검토한다면 이 둘은 직접 확인하고 넘어가자.

## 매주 월요일 아홉 시, 그리고 네 번

이제 리포트를 자동으로 돌릴 차례다. 주기 실행 애너테이션 한 줄, Quartz 설정 몇 줄, 또는 node-cron 한 줄로 끝내던 자리다. FastAPI에는 그 자리가 **비어 있다.** 주기 실행을 프레임워크가 주지 않으므로 층을 골라야 하고, 고를 수 있는 층은 셋이다.

앱 안에서 돌린다. 앱이 뜰 때 스케줄러를 함께 띄우고 시각이 되면 함수를 부른다. 배포 단위가 늘지 않아 가장 간단하다. 파이썬에는 이 역할의 라이브러리가 여럿 있는데, 이 책은 그중 어느 것의 현재 API·버전도 확인하지 못했다. 도구를 단정하는 대신 구조만 이야기하겠다.

큐 도구의 주기 기능을 쓴다. 앞 절의 축 네 번째다. 큐를 이미 세웠다면 스케줄도 거기 얹는 것이 자연스럽다.

배포 층에 맡긴다. 정해진 시각에 컨테이너를 하나 띄워 명령을 실행시키는 방식이고, 쿠버네티스라면 CronJob이 그 자리다. 앱 프로세스와 완전히 분리되는 것이 장점이자 단점이다.

세 층 중 첫 번째에 함정이 있다. **워커가 N개면 스케줄도 N번 돈다.**

이건 추측이 아니라 5장에서 확인한 사실에서 그대로 따라 나온다. `--workers`가 만드는 것은 스레드가 아니라 독립된 프로세스이고, 프로세스는 메모리를 공유하지 않는다. 앱 코드가 "앱이 뜰 때 스케줄러를 하나 띄운다"고 적혀 있으면, 워커 4개짜리 서버에서는 **스케줄러가 4개 뜬다.** 각자 자기 시계를 보다가 월요일 아홉 시에 각자 리포트를 만든다. 레플리카를 셋으로 늘리면 12개다. 곱셈이다.

7장에서 알림이 절반만 도착하던 문제와 정확히 대칭이다. 그쪽은 프로세스 경계 때문에 **덜 도착했고**, 이쪽은 같은 경계 때문에 **더 실행된다.**

더 고약한 것은 이 버그가 당신을 잘 피해 다닌다는 점이다. 로컬에서는 워커가 하나라 완벽하게 돌고 스테이징도 대개 하나다. 워커를 늘리는 것은 프로덕션의 결정이므로 **이 버그는 프로덕션에서만 나타난다.** 그것도 리포트 메일이 네 통 왔다는 제보로.

구조적인 답은 둘 중 하나다. 하나, 스케줄을 앱 밖으로 뺀다 — 위의 두 번째나 세 번째 층이 이 방향이다. 둘, 앱 안에 두되 여럿 중 하나만 실행하도록 조율한다. 조율에 쓰는 도구가 분산 락이나 리더 선출이고, 어느 쪽이든 프로세스 밖의 공유 저장소가 필요하다. 어차피 밖의 무언가가 필요하다면, 스케줄 자체를 밖에 두는 편이 단순한 경우가 많다.

기억해두자. 프레임워크는 "이 코드는 전체에서 한 번만 돌아야 한다"는 요구를 표현해주지 않는다. 그 요구는 우리가 적어야 한다.

## 1메가바이트라는 벽

`tracker`의 이슈에는 스크린샷이 붙고, 가끔 로그 덤프가 붙고, 아주 가끔 30메가바이트짜리 영상이 올라온다. 업로드를 받으려면 의존성이 하나 필요하다.

```bash
uv add python-multipart
```

파라미터에 `UploadFile` 타입을 적으면 끝이다. 여기서 나오는 첫 질문은 늘 같다. **이거 메모리에 다 올라오는 건가?** 공식 문서의 답은 "spooled" 파일이라는 것이다 — 어느 크기까지는 메모리에 두고, 그 선을 넘으면 디스크로 옮긴다. 그런데 그 선이 몇 바이트인지는 문서가 말해주지 않는다. 소스에 있다.

```python
class MultiPartParser:
    spool_max_size = 1024 * 1024  # 1MB
    """The maximum size of the spooled temporary file used to store file data."""
    max_part_size = 1024 * 1024  # 1MB
    """The maximum size of a part in the multipart request."""
```

> 출처: starlette 1.3.1 태그 `starlette/formparsers.py` (조회 2026-07-26)

값이 같아서 한 덩어리로 보이지만, 붙어 있는 설명이 이미 갈라진다. 하는 일이 전혀 다르다.

`spool_max_size`는 **메모리에서 디스크로 갈아타는 지점**이다. 1메가바이트까지는 메모리에 들고 있다가 넘어가면 임시 파일로 내려간다. 저장 위치의 문제이지 거부의 문제가 아니다. 그래서 "다 메모리에 올린다"도 틀렸고 "항상 디스크에 쓴다"도 틀렸다.

`max_part_size`는 **거부선**이다. 멀티파트의 한 파트가 이 크기를 넘으면 파서가 예외를 던진다. 앞의 것이 저장 위치를 정한다면 이건 통과 여부를 정한다.

문제는 두 번째 값이다. 1메가바이트는 첨부 파일 기준으로 너무 작다. 올리면 되지 않을까? 여기서 걸린다. 폼 파싱을 직접 부르는 쪽에는 이 값을 넘길 인자가 있지만, 우리가 쓰는 선언형 경로에는 그 인자를 넘길 손잡이가 없다.

```python
body = await request.form()
```

> 출처: fastapi 0.140.0 태그 `fastapi/routing.py` (조회 2026-07-26)

경로 함수 파라미터에 `UploadFile`을 적으면 FastAPI가 대신 부르는 것이 이 한 줄이다. **인자가 없다.** 그래서 기본값이 그대로 적용된다. 값을 바꾸려면 파싱을 직접 부르거나 파서 쪽에 손을 대야 한다. "필요하면 한도를 올려라"라는 조언을 어딘가에서 보게 되겠지만, 그 조언이 가리키는 곳이 이 경로에는 없다.

우연히도 서블릿 진영의 멀티파트 최대 파일 크기 기본값 역시 1메가바이트다. 숫자는 같은데 성질이 다르다. 그쪽에서는 설정 파일의 한 줄이 그 값을 바꾸고, 여기서는 그 한 줄을 적을 데가 없다. 번역이 잘 되는 듯하다가 마지막 한 칸에서 어긋나는 자리다.

이 층이 주는 것은 파트 단위 한도다. 요청 전체를 한 번에 막는 스위치가 아니다. 그래서 방어선은 대개 앱보다 앞에 선다 — 리버스 프록시의 바디 크기 제한, 또는 우리가 직접 얹은 ASGI 계층.

앱 안에서 크기를 확인할 방법이 아예 없는 것은 아니다. `UploadFile`에는 `size` 속성이 있고, 이건 헤더가 아니라 실제로 읽어들인 내용에서 계산된 값이다.[^8-2] `Content-Length`를 믿는 것보다 낫다.

## 첨부 하나를 받아내기

이제 조립하자. 6장은 `Attachment`에 파일 바이트를 넣지 않기로 했고, 어디에 둘지는 이 장으로 넘겼다.

그 답도 5장의 문장에서 나온다. 워커는 메모리를 공유하지 않고, 레플리카는 파일 시스템도 공유하지 않는다. 인스턴스 A가 로컬 디스크에 저장한 파일을 인스턴스 B가 내려줄 방법이 없으니, **컨테이너의 로컬 디스크는 단일 인스턴스 전제가 성립할 때만 저장소가 된다.** `storage_key`가 가리키는 곳은 프로세스 밖의 공유 저장소여야 한다. 아예 파일이 앱을 통과하지 않게 하는 선택지도 있다 — 클라이언트가 서명된 URL로 저장소에 직접 올리고 앱은 메타데이터만 받는 방식이다.

여기서는 앱을 통과시키는 쪽으로 간다. 방어선은 세 겹이다 — **크기를 제한하고, 스트리밍으로 저장하고, 무거운 것은 오프로드한다.**

> **📐 저자 설계 —** 아래 배선은 FastAPI 공식 권장이 아니라, 5장의 오프로드 규칙과 6장의 세션 규칙에서 이 책이 도출한 한 가지 안이다. 저장소 쓰기 함수는 어떤 저장소를 골랐는지에 따라 달라지므로 내부를 비워둔다.

```python
# src/tracker/services/attachment.py
from uuid import uuid4

from anyio import to_thread
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from tracker.models.attachment import Attachment

# ...(5장, 생략)

CHUNK_SIZE = 1024 * 1024


def append_to_storage(storage_key: str, chunk: bytes) -> None:
    ...


class AttachmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_attachment(
        self, *, issue_id: int, uploader_id: int, file: UploadFile
    ) -> Attachment:
        storage_key = f"issues/{issue_id}/{uuid4().hex}"
        size = 0
        while chunk := await file.read(CHUNK_SIZE):
            size += len(chunk)
            await to_thread.run_sync(append_to_storage, storage_key, chunk)

        attachment = Attachment(
            issue_id=issue_id,
            uploader_id=uploader_id,
            filename=file.filename or "unnamed",
            content_type=file.content_type or "application/octet-stream",
            size_bytes=size,
            storage_key=storage_key,
        )
        self.session.add(attachment)
        await self.session.commit()
        return attachment
```

조각으로 읽는 이유는 메모리다. 30메가바이트짜리를 한 번에 바이트열로 올리면 프로세스가 그만큼을 더 쓴다. 저장소 쓰기를 `to_thread.run_sync`로 감싼 것은 5장의 기본형 그대로다 — 저장소 클라이언트가 동기 라이브러리일 때 이벤트 루프를 지키는 방법이다.[^8-3] 비동기 클라이언트라면 이 줄은 그냥 `await`가 된다.

응답 스키마는 3장의 접미사 규약을 그대로 따른다.

```python
# src/tracker/schemas/attachment.py
from pydantic import BaseModel, ConfigDict


class AttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    content_type: str
    size_bytes: int
```

라우터는 얇다.

```python
# src/tracker/api/attachments.py
from fastapi import APIRouter, UploadFile

from tracker.deps import CurrentUser, SessionDep
from tracker.errors import ValidationFailedError
from tracker.schemas.attachment import AttachmentRead
from tracker.services.attachment import AttachmentService

router = APIRouter(prefix="/issues/{issue_id}/attachments", tags=["attachments"])

MAX_UPLOAD_BYTES = 20 * 1024 * 1024


@router.post("", response_model=AttachmentRead, status_code=201)
async def upload_attachment(
    issue_id: int,
    file: UploadFile,
    session: SessionDep,
    user: CurrentUser,
) -> AttachmentRead:
    if file.size is not None and file.size > MAX_UPLOAD_BYTES:
        raise ValidationFailedError(
            "첨부 파일이 허용 크기를 넘었습니다", code="attachment.too_large"
        )
    service = AttachmentService(session)
    attachment = await service.add_attachment(
        issue_id=issue_id, uploader_id=user.id, file=file
    )
    return AttachmentRead.model_validate(attachment)
```

상수를 20메가바이트로 잡아뒀지만, 앞 절의 파트 한도를 그대로 뒀다면 여기 닿기 전에 파서가 먼저 거절한다. **앱 안의 검사는 그 한도를 옮긴 뒤에야 의미가 생긴다.** 두 값이 따로 논다는 것을 잊으면 20이 지켜지는 줄 안다.

썸네일은 여기 없다. 5장에서 CPU 바운드 작업의 답을 이미 정해뒀기 때문이다 — 프로세스 밖. 업로드 응답은 첨부 레코드만 돌려주고, 썸네일은 잠시 뒤 붙는다. 6장에서 `Attachment`의 `thumbnail_key`를 널 허용 타입으로 적어둔 것이 여기서 값을 한다. 그 "잠시 뒤"를 무엇이 책임지는지는 아래에서 정한다.

리포트로 돌아오자. 첫 버전은 이렇게 시작한다.

```python
# src/tracker/api/projects.py (8장에서 추가)
from fastapi import BackgroundTasks

from tracker.services.report import build_weekly_report

# ...(2장, 생략)


@router.post("/{project_id}/reports", status_code=202)
async def request_weekly_report(
    project_id: int,
    background_tasks: BackgroundTasks,
    user: CurrentUser,
) -> dict[str, str]:
    background_tasks.add_task(build_weekly_report, project_id)
    return {"status": "accepted"}
```

`build_weekly_report`가 받는 것은 프로젝트 식별자 하나뿐이다. 세션은 받지 않는다 — 앞에서 정한 규칙이다.

```python
# src/tracker/services/report.py
from tracker.db import session_factory


async def build_weekly_report(project_id: int) -> None:
    async with session_factory() as session:
        ...
```

6장의 세션 팩토리로 자기 세션을 자기가 여는 것이다.

이 버전은 언제까지 유효할까. 네 문항에 대보자. 유실되면 사용자가 다시 누르면 되고, 12초는 유예 시간 안이고, 작업 대부분은 데이터베이스를 기다리는 시간이다. 지금은 통과다. **그런데 전부 "지금은"이 붙는다.** 리포트가 40초로 늘어나면 세 번째가 깨지고, 자동 발송이 붙어 사람이 다시 누를 수 없게 되면 첫 번째가 깨진다.

깨졌을 때 코드가 얼마나 바뀔까. 한 줄이면 되도록 미리 접어두자.

> **📐 저자 설계 —** 아래 함수는 특정 태스크 큐의 API가 아니라, 어떤 도구를 고르든 그 뒤에 숨기려고 이 책이 만든 이음매다.

```python
# src/tracker/tasks.py
async def enqueue_weekly_report(project_id: int) -> None:
    ...


async def enqueue_thumbnail(attachment_id: int) -> None:
    ...
```

썸네일도 같은 모양이다. 업로드가 끝나면 `enqueue_thumbnail`을 부르고, 5장의 `generate_thumbnail`은 큐 워커 쪽에서 돈다 — 5장이 미뤄둔 "프로세스 밖"이 이 한 줄이다. 리포트 쪽은 라우터에서 `background_tasks.add_task(build_weekly_report, project_id)`를 `await enqueue_weekly_report(project_id)`로 바꾸면 승격이 끝난다. 라우터는 자기 일이 큐로 가는지 같은 프로세스에서 도는지 모른 채 남고, 도구를 바꿀 때 손댈 파일은 `tasks.py` 하나다.

---

이 장에서 반복된 문장이 하나 있다. **프로세스 경계는 프레임워크가 지워주지 않는다.** 태스크가 프로세스와 함께 사라지는 것도, 스케줄이 워커 수만큼 실행되는 것도, 로컬 디스크가 저장소가 되지 못하는 것도 전부 그 한 문장의 다른 얼굴이다. 5장에서 이 사실을 배웠고, 7장에서 알림으로 겪었고, 여기서는 세 번 더 만났다.

그러니 당신 앱에 물어볼 것이 있다. 응답 뒤에 도는 코드가 어디에 있는가. 그중 사라지면 곤란한 것이 있는가. 그리고 정해진 시각에 도는 코드가 있다면, 그건 몇 번 돌고 있는가.

[^8-1]: `from fastapi import BackgroundTasks`와 `background_tasks.add_task(func, *args, **kwargs)` 호출 형태, 태스크 함수가 `async def`·`def` 양쪽 모두 가능하다는 서술, 응답 이후 실행 보장 — FastAPI 공식 문서 *Background Tasks*, https://fastapi.tiangolo.com/tutorial/background-tasks/ (조회 2026-07-26)

[^8-2]: `UploadFile`의 속성 `filename`·`content_type`·`file`과 비동기 메서드 `read()`·`write()`·`seek()`·`close()`, 그리고 `python-multipart` 의존 — FastAPI 공식 문서 *Request Files*, https://fastapi.tiangolo.com/tutorial/request-files/ (조회 2026-07-26). `size` 속성은 starlette 1.3.1 태그 `starlette/datastructures.py`의 `UploadFile.__init__`에서 확인 (조회 2026-07-26)

[^8-3]: `from anyio import to_thread`와 `to_thread.run_sync(func, *args)` — 5장 각주에서 확인한 AnyIO 공식 문서 *Working with threads*, https://anyio.readthedocs.io/en/stable/threads.html. `Session.add()`·`Session.commit()`의 호출 형태 — SQLAlchemy 2.0 *Session Basics*, https://docs.sqlalchemy.org/en/20/orm/session_basics.html (둘 다 조회 2026-07-26)
