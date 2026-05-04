# 11장. 데스크톱 앱 — Electron과 Tauri의 네이티브 경계

사내 도구 하나를 만들어야 하는 상황을 상상해보자. 백엔드는 Java Spring으로 잘 돌아가고 있고, 이미 React로 웹 UI도 있다. 그런데 팀장이 한 마디 한다. "이거, 데스크톱 앱으로 만들 수 없어요? 파일 시스템 접근이 필요해서." 웹 API만으로는 부족한 순간이다. 브라우저 보안 정책이 파일 시스템을 막고 있고, 알림(notification)도 마음대로 쓸 수 없다.

이 순간, TypeScript 개발자에게 주어진 선택지는 두 가지다. Electron과 Tauri. 둘 다 TypeScript로 UI를 짜고, 둘 다 Windows·macOS·Linux를 지원한다. 그런데 선택은 생각보다 간단하지 않다. 이 챕터는 그 선택의 근거를 함께 쌓아간다.

그리고 데스크톱 이야기를 마무리하면서, 모바일로 자연스럽게 발을 내딛는다. React Native라는 이름은 들어봤을 것이다. 토스가 쓰고, 당근이 쓰고, 쿠팡이츠가 쓴다. 그런데 TypeScript 시각에서 React Native를 들여다본 한국어 자료는 빈약하다. 이 챕터가 그 자리를 채우는 것을 책임으로 삼는다.

---

## Electron — 웹의 힘으로 데스크톱을 정복한 방식

### 왜 VS Code는 Electron을 선택했는가

2015년, Microsoft는 VS Code를 Electron으로 만들기로 했다. 그 결정은 지금도 논쟁거리다. 전 세계 개발자가 매일 쓰는 에디터가 Chromium을 품고 있다는 사실이 여전히 불편한 사람들이 있다. 메모리를 500MB 넘게 쓴다는 푸념도 빠지지 않는다.

하지만 그 결정을 무모한 선택이라고 보기는 어렵다. Electron의 핵심 제안은 간단하다. **"웹 개발자가 이미 아는 기술로 데스크톱 앱을 만들 수 있게 한다."** HTML, CSS, JavaScript — 그것으로 충분하다. 네이티브 UI 툴킷을 새로 배울 필요가 없다. Java로 치면 JavaFX나 Swing을 배울 필요 없이 Spring MVC 지식으로 데스크톱을 만드는 셈이다.

> 📚 **Java/Kotlin 시선 — JavaFX/Swing ↔ Electron/Tauri: 배포 모델의 차이**
>
> JavaFX와 Swing은 JVM 위에서 네이티브 UI 컴포넌트(또는 커스텀 렌더링)를 직접 그린다. 배포는 JAR이고, JVM이 설치되어 있어야 한다. GraalVM native-image로 독립 실행 파일을 만들 수 있지만 제약이 많다.
>
> Electron은 Chromium + Node.js 런타임 전체를 앱과 함께 묶어서 배포한다. 최종 사용자는 Java를 설치할 필요가 없다. 대신 바이너리가 크다 — 기본 Hello World가 150MB 내외. Tauri는 이 문제를 OS의 내장 WebView를 쓰는 방식으로 해결한다 (뒤에서 자세히).
>
> Spring 개발자가 "배포 단위"라는 개념을 바꿔 생각해야 한다. JAR이 아니라 설치 파일(.dmg, .exe, .AppImage)이 최종 산출물이다.

VS Code 외에도 Slack, Discord, Notion, Figma, 그리고 국내 팀들의 사내 도구 다수가 Electron으로 만들어진다. 카카오와 네이버의 일부 내부 도구도 Electron을 쓴다. 이미 React·Vue 기반 웹 코드베이스가 있는 팀에게는 재사용 비율이 높고, 웹 개발자 채용 시장이 넓다는 점이 Electron 선택의 실용적 이유가 된다.

그렇다면 Electron의 구조를 제대로 이해해보자. 제대로 알지 않으면 나중에 찜찜한 코드를 쓰게 된다.

### 메인 프로세스와 렌더러 프로세스 — 두 세계의 공존

Electron 앱은 두 종류의 프로세스로 나뉜다.

**메인 프로세스(Main Process)**는 Node.js 환경이다. 파일 시스템, 운영체제 API, 창 관리, 시스템 트레이 — 네이티브 기능은 전부 여기서 다룬다. 앱이 시작되면 메인 프로세스가 먼저 실행되고, `BrowserWindow`를 만들어 렌더러를 띄운다.

**렌더러 프로세스(Renderer Process)**는 Chromium 환경이다. 각 `BrowserWindow`마다 별도의 렌더러가 생긴다. 여기서는 React, Vue, Svelte — 어떤 웹 프레임워크든 쓸 수 있다. DOM에 접근하고, CSS를 입히고, 사용자와 상호작용한다.

두 프로세스는 별개의 프로세스이기 때문에 메모리를 공유하지 않는다. 직접 함수를 호출할 수 없다. 그렇다면 어떻게 소통할까? 바로 **IPC(Inter-Process Communication)**다.

```typescript
// 메인 프로세스: main.ts
import { app, BrowserWindow, ipcMain } from 'electron'
import * as fs from 'fs/promises'

app.whenReady().then(() => {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,   // 보안: 렌더러와 Node.js를 격리
      nodeIntegration: false,   // 보안: 렌더러에서 Node.js 직접 접근 금지
    },
  })

  // 렌더러로부터 파일 읽기 요청을 받는다
  ipcMain.handle('read-file', async (event, filePath: string) => {
    const content = await fs.readFile(filePath, 'utf-8')
    return content
  })

  win.loadFile('index.html')
})
```

```typescript
// 렌더러 프로세스: renderer.ts (React 컴포넌트 안에서)
const content = await window.electronAPI.readFile('/path/to/file.txt')
```

```typescript
// preload.ts — 두 세계의 다리
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  readFile: (filePath: string) => ipcRenderer.invoke('read-file', filePath),
})
```

여기서 `contextBridge`가 중요하다. 과거 Electron 앱들은 렌더러에서 직접 `ipcRenderer`를 import해 썼다. 그런데 그러면 렌더러가 Node.js API에 직접 접근할 수 있어서 보안 구멍이 생긴다. 악의적인 스크립트가 렌더러에 주입되면 파일 시스템을 마음대로 읽을 수 있다. `contextBridge`는 이 위험을 차단한다. 메인과 렌더러 사이에 선택적으로 노출할 API만 골라서 내보내는 것이다.

### IPC 타이핑 — 타입이 경계를 넘을 수 있는가

자, 이제 TypeScript 개발자로서 진짜 고민이 시작된다. 위의 코드를 보면 `ipcMain.handle('read-file', ...)` 에서 채널 이름이 문자열이다. 렌더러에서 `ipcRenderer.invoke('read-file', filePath)` 를 호출할 때도 문자열이다. 채널 이름을 오타 내도 컴파일 에러가 없다. 인자 타입이 맞지 않아도 컴파일 에러가 없다.

이것은 꽤 난감한 상황이다. TypeScript를 쓰는 이유가 뭔가? 타입 안전성 아닌가. 그런데 IPC 경계에서는 타입이 사라진다.

다행히 이 문제를 해결하는 패턴들이 있다. 가장 직접적인 방법은 **타입 브릿지**를 수동으로 만드는 것이다.

```typescript
// ipc-types.ts — 메인/렌더러가 공유하는 IPC 계약
export interface IpcChannels {
  'read-file': {
    request: [filePath: string]
    response: string
  }
  'write-file': {
    request: [filePath: string, content: string]
    response: void
  }
  'get-app-version': {
    request: []
    response: string
  }
}

// 타입 안전한 ipcMain.handle 래퍼
type IpcMainTyped = {
  handle<K extends keyof IpcChannels>(
    channel: K,
    handler: (
      event: Electron.IpcMainInvokeEvent,
      ...args: IpcChannels[K]['request']
    ) => Promise<IpcChannels[K]['response']>
  ): void
}

// 타입 안전한 ipcRenderer.invoke 래퍼
type IpcRendererTyped = {
  invoke<K extends keyof IpcChannels>(
    channel: K,
    ...args: IpcChannels[K]['request']
  ): Promise<IpcChannels[K]['response']>
}
```

이렇게 하면 채널 이름을 오타 내면 컴파일 에러가 난다. 인자 타입이 맞지 않아도 컴파일 에러가 난다. `IpcChannels` 인터페이스가 메인과 렌더러 사이의 계약서 역할을 한다.

**electron-trpc**는 이 개념을 한 단계 더 밀어붙인 라이브러리다. 13장에서 다룰 tRPC의 아이디어 — "API 스펙을 공유하면 클라이언트 타입이 자동으로" — 를 Electron IPC에 적용한다.

```typescript
// electron-trpc를 쓴 예
import { initTRPC } from '@trpc/server'
import { createIPCHandler } from 'electron-trpc/main'

const t = initTRPC.create()
const router = t.router({
  readFile: t.procedure
    .input(z.object({ filePath: z.string() }))
    .query(async ({ input }) => {
      return fs.readFile(input.filePath, 'utf-8')
    }),
  writeFile: t.procedure
    .input(z.object({ filePath: z.string(), content: z.string() }))
    .mutation(async ({ input }) => {
      await fs.writeFile(input.filePath, input.content)
    }),
})

export type AppRouter = typeof router

// 메인 프로세스에서 핸들러 등록
createIPCHandler({ router, windows: [win] })
```

```typescript
// 렌더러에서
import { createTRPCProxyClient } from '@trpc/client'
import { ipcLink } from 'electron-trpc/renderer'
import type { AppRouter } from '../main/router'

const trpc = createTRPCProxyClient<AppRouter>({
  links: [ipcLink()],
})

// 완전한 타입 안전성 — AppRouter에서 자동 추론
const content = await trpc.readFile.query({ filePath: '/path/to/file.txt' })
const _: string = content  // 타입이 string으로 잘 추론된다
```

`AppRouter` 타입 하나를 메인과 렌더러가 공유하는 것으로 IPC 경계의 타입 안전성이 완성된다. 채널 이름도 없고, 인자 타입도 명시할 필요 없다. tRPC가 5장에서 배운 "타입을 만드는 타입" 기술로 내부적으로 다 처리한다. 정말 우아한 해법이다.

### Electron의 비용 — 솔직하게 직면해야 한다

Electron을 쓰면 반드시 마주하는 현실적인 불편함이 있다. 외면하면 나중에 더 난감하다.

**바이너리 크기.** 단순한 앱도 배포 파일이 150~200MB에 달한다. Chromium과 Node.js 런타임을 통째로 들고 다니기 때문이다. 사용자가 앱을 다운로드할 때 무거움을 느낀다. 자동 업데이트도 그만큼 느리다.

**메모리 사용량.** 빈 Electron 앱이 100MB 이상 메모리를 쓴다. 사내 도구라면 괜찮을 수 있지만, 여러 앱을 동시에 쓰는 사용자 환경에서는 부담이다. Slack이 메모리를 많이 먹는다는 불평은 Electron이 구조적으로 안고 가는 비용이다.

**보안 모델.** `nodeIntegration: true` 로 설정한 오래된 Electron 앱들이 많다. 이 설정은 렌더러에서 Node.js API 직접 접근을 허용해서, XSS 취약점이 있으면 공격자가 파일 시스템에 접근할 수 있다. 신규 프로젝트라면 `contextIsolation: true`, `nodeIntegration: false`, `contextBridge` 사용이 필수다.

그렇다면 이런 비용 없이 비슷한 것을 만들 수 있을까? Tauri가 그 질문에 대한 답이다.

---

## Tauri — Rust 백엔드와 네이티브 WebView의 만남

### Tauri가 Electron과 다른 결정적 지점

Tauri는 2022년 v1이 나오고 2024년 10월 v2가 GA(General Availability) 상태가 됐다. Electron과 목표는 같다 — TypeScript로 크로스 플랫폼 데스크톱 앱 만들기. 그런데 접근 방식이 완전히 다르다.

Electron은 Chromium을 앱에 번들한다. Tauri는 **OS 내장 WebView**를 쓴다. macOS는 WKWebView, Windows는 WebView2(Edge 기반), Linux는 WebKitGTK. 이미 OS에 있는 것을 쓰니까 배포 바이너리에 브라우저를 넣을 필요가 없다.

그 결과가 놀랍다. 같은 기능의 Hello World 앱 기준으로 Electron은 150~200MB, Tauri는 1~5MB다. 약 1/10에서 1/50 수준이다.

Electron의 메인 프로세스가 Node.js라면, Tauri의 백엔드는 **Rust**다. 여기서 Java 백엔드 개발자가 흥미로운 질문을 할 수 있다. "Rust라면 학습 곡선이 급하지 않나요? TypeScript 코드만 쓰고 싶은데."

좋은 소식이 있다. Tauri의 기본 명령들(파일 읽기, 경로 접근 등)은 이미 Rust로 만들어져 있고, TS에서 그냥 호출하면 된다. 커스텀 기능이 필요할 때만 Rust를 직접 쓴다. 그리고 그 경계, 즉 TS에서 Rust 함수를 호출하는 방식이 Tauri의 가장 흥미로운 부분이다.

### `invoke` — TS에서 Rust를 호출하는 방법

Tauri의 IPC는 Electron보다 훨씬 단순하다. 렌더러(프론트)에서 `invoke` 하나로 Rust 함수를 호출한다.

```rust
// src-tauri/src/lib.rs — Rust 백엔드
use tauri::command;

#[command]
fn read_file(file_path: String) -> Result<String, String> {
    std::fs::read_to_string(&file_path)
        .map_err(|e| e.to_string())
}

#[command]
fn greet(name: String) -> String {
    format!("안녕하세요, {}님!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_file, greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
// 프론트엔드 (TypeScript)
import { invoke } from '@tauri-apps/api/core'

// 이렇게 호출한다
const content = await invoke<string>('read_file', { filePath: '/path/to/file.txt' })
const greeting = await invoke<string>('greet', { name: '토비' })
```

여기서 찜찜한 부분이 보이는가? `invoke<string>('read_file', { filePath: '...' })` 에서 `'read_file'`이 문자열이다. `{ filePath: '...' }` 의 타입도 수동으로 맞춰야 한다. Electron의 순수 IPC 방식과 같은 문제 — 경계에서 타입이 약해진다.

### tauri-specta — Rust 타입을 TypeScript로 내보내기

이 문제를 해결하는 도구가 **tauri-specta**다. Specta는 Rust 타입을 TypeScript 타입으로 자동 생성하는 라이브러리다. tauri-specta는 이것을 Tauri `invoke` 바인딩에 적용한다.

```rust
// Cargo.toml에 specta, specta-typescript, tauri-specta 추가

use specta::Type;
use specta_typescript::Typescript;
use tauri_specta::{collect_commands, ts};

#[derive(Debug, serde::Serialize, serde::Deserialize, Type)]
pub struct FileReadResult {
    pub content: String,
    pub size: u64,
}

#[tauri::command]
#[specta::specta]
fn read_file(file_path: String) -> Result<FileReadResult, String> {
    let content = std::fs::read_to_string(&file_path)
        .map_err(|e| e.to_string())?;
    let size = content.len() as u64;
    Ok(FileReadResult { content, size })
}

fn main() {
    // 타입 내보내기 (개발 시에만 실행)
    #[cfg(debug_assertions)]
    ts::export(
        collect_commands![read_file, greet],
        "../src/bindings.ts"  // TS 파일로 자동 생성
    ).unwrap();

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_file, greet])
        .run(tauri::generate_context!())
        .unwrap();
}
```

이렇게 하면 `src/bindings.ts` 파일이 자동 생성된다.

```typescript
// 자동 생성된 bindings.ts
import { invoke } from "@tauri-apps/api/core"

export interface FileReadResult {
  content: string
  size: number
}

export const commands = {
  readFile: async (filePath: string): Promise<FileReadResult> => {
    return await invoke<FileReadResult>("read_file", { filePath })
  },
  greet: async (name: string): Promise<string> => {
    return await invoke<string>("greet", { name })
  },
}
```

```typescript
// 프론트엔드에서 사용
import { commands } from './bindings'

// 완전한 타입 안전성 — Rust 타입이 TS 타입으로
const result = await commands.readFile('/path/to/file.txt')
console.log(result.content)  // string
console.log(result.size)     // number
```

이것은 5장에서 다룬 "타입을 만드는 타입" 개념의 언어 간 확장이다. Rust의 `#[derive(Type)]`과 `#[specta::specta]`가 런타임에 타입 정보를 수집하고, 빌드 시 TypeScript 타입 파일로 토해낸다. TS→JS의 타입 소거와 반대 방향 — Rust 타입이 TS 타입으로 *생성*된다.

이제 채널 문자열을 잘못 쓸 일이 없다. `commands.readFile` 이 IDE에서 자동완성되고, 인자 타입이 맞지 않으면 컴파일 에러가 난다.

> 📚 **Java/Kotlin 시선 — Java JNI ↔ Tauri `invoke` / React Native Bridge**
>
> Java에서 네이티브 코드(C/C++)를 호출하는 방법이 JNI(Java Native Interface)다. JNI는 악명 높다. 선언부를 직접 매핑해야 하고, 타입 안전성이 없으며, 잘못 쓰면 JVM 크래시다. JNA(Java Native Access)가 조금 낫지만 여전히 번거롭다.
>
> Tauri의 `invoke`는 JSON 직렬화를 통해 TS↔Rust 경계를 넘는다. JNI처럼 메모리 레벨 매핑은 없고, tauri-specta로 타입 계약을 자동 생성할 수 있다. React Native의 JSI(Java Script Interface)도 비슷한 위치 — JS와 C++ 사이의 브릿지를 타입 안전하게 만드는 문제를 푼다 (이 챕터 뒷절에서 자세히).

### Tauri v2의 추가된 것들

Tauri v2(2024년 10월 GA)에서 달라진 것이 있다. 가장 눈에 띄는 것은 **모바일 지원**이다. v2는 iOS와 Android 앱도 같은 코드베이스로 빌드할 수 있다. 다만 v2의 모바일 지원은 아직 성숙 단계이고, React Native 생태계에 비하면 작다. "같은 Rust 코어, 플랫폼별 WebView"라는 아이디어는 매력적이지만, 실전에서 부딪히는 플랫폼별 차이 처리는 아직 커뮤니티가 쌓아가는 중이다.

또 v2의 **보안 모델**이 강화됐다. 메인 설정 파일(`tauri.conf.json`)에서 명시적으로 허용한 API만 프론트에서 접근할 수 있다. Electron에서 `contextBridge`로 수동 관리하던 것을 Tauri는 설정으로 처리한다.

```json
// tauri.conf.json
{
  "plugins": {
    "fs": {
      "scope": {
        "allow": ["$APPDATA/**", "$DOWNLOAD/**"],
        "deny": ["$HOME/.ssh/**"]
      }
    }
  }
}
```

파일 시스템 접근 범위를 명시적으로 선언한다. 공격자가 렌더러에 스크립트를 주입해도 선언된 범위 밖에는 접근할 수 없다.

---

## Electron vs Tauri — 선택의 기준

솔직하게 정리해보자. 둘 중 어느 것이 낫다는 절대적 답은 없다. 상황에 따라 다르다. 다음 표가 그 판단의 기준이 된다.

| 기준 | Electron | Tauri v2 |
|------|----------|-----------|
| **바이너리 크기** | 150~200MB | 1~10MB |
| **메모리 사용** | 100MB+ (기본) | 30~80MB (WebView 공유) |
| **렌더링 엔진** | Chromium (번들, 일관성 ↑) | OS 내장 WebView (플랫폼별 차이 있음) |
| **백엔드 언어** | Node.js (JS/TS) | Rust (학습 곡선 있음) |
| **생태계 성숙도** | 매우 성숙 (10년+) | 성장 중 (v2 2024년) |
| **TS 타입 안전성** | electron-trpc, 수동 브릿지 | tauri-specta 자동 생성 |
| **보안 기본값** | 설정 필요 (contextBridge) | 설정 기반 명시적 허용 |
| **Windows 최소 지원** | Windows 7+ (구버전 Chromium) | Windows 10+ (WebView2) |
| **개발자 경험** | 성숙한 도구, 많은 예제 | 빠르게 개선 중 |
| **한국 사례** | 카카오·네이버 사내 도구 다수 | 토스 일부 신규 시도 |

**Electron이 더 나은 경우:**
- 팀에 Rust 경험자가 없고 빠르게 만들어야 할 때
- 기존 웹 코드베이스를 최대한 재활용하고 싶을 때
- Windows 구버전 지원이 필요할 때
- 생태계와 레퍼런스가 중요할 때

**Tauri가 더 나은 경우:**
- 바이너리 크기와 메모리가 중요한 도구일 때
- 팀에 Rust 역량이 있거나 배울 준비가 됐을 때
- 보안이 핵심인 앱(비밀번호 관리, 기업 보안 도구 등)
- 최신 기술 스택을 채택할 여건이 될 때

사내 도구라면 Electron이 빠른 선택일 수 있다. 외부 배포 소비자 앱이라면 Tauri의 작은 바이너리와 빠른 시작이 사용자 경험에서 차이를 만든다.

### 카카오·네이버 사내 도구 Electron 패턴

한국 대기업 개발 조직에서 Electron 선택은 꽤 실용적인 이유로 이뤄진다. 대부분의 팀이 이미 React 기반 웹 프론트엔드 코드를 갖고 있다. 사내 도구를 웹 앱으로 만들려다 보면 사내 파일 공유 시스템 접근, 시스템 알림, 트레이 아이콘 같은 기능이 브라우저에서는 제한된다. Electron은 이 갭을 최소한의 추가 학습으로 메운다.

카카오의 일부 내부 메신저 확장 도구, 네이버의 일부 개발자 도구가 이런 패턴으로 만들어진다고 알려져 있다. 공개 자료가 제한적이기는 하지만, 기술블로그와 개발자 발표에서 Electron 채택 사례를 종종 볼 수 있다.

흥미로운 점은 "사내 도구는 바이너리 크기보다 빠른 개발이 우선"이라는 조직의 실용적 판단이다. 사용자가 수천 명이 넘지 않는 사내 도구라면 200MB 바이너리도 큰 문제가 아니다. 대신 웹 팀이 추가 기술 없이 바로 기여할 수 있다는 게 더 큰 가치다.

---

## 모바일과 멀티 플랫폼 — TypeScript 시각의 모바일

### 한국 시장에서 React Native가 의미하는 것

당근마켓의 중고 거래 화면 일부, 토스의 일부 화면, 쿠팡이츠의 배달 화면 일부. 이 앱들이 완전한 네이티브(Swift/Kotlin)만으로 만들어진 건 아니다. React Native로 만들어진 화면이 섞여 있다. 그것이 지금 한국 모바일 개발의 현실이다.

"일부"라는 표현이 중요하다. 보통 "RN 부분 도입"은 이런 식이다. 메인 화면, 결제 화면, 지도 화면 같이 성능이 중요하거나 네이티브 API를 많이 쓰는 곳은 Swift/Kotlin. 이벤트 페이지, 정보 화면, 쿠폰 화면 같이 자주 바뀌고 복잡한 네이티브 기능이 없는 곳은 React Native. 그리고 React Native는 이 "자주 바뀌는 화면"에서 큰 강점을 발휘한다. OTA(Over-The-Air) 업데이트로 앱 스토어 심사 없이 바로 업데이트할 수 있다.

이 챕터가 모바일 앱 개발 전반을 다루는 건 아니다. TypeScript 시각에서 "React Native의 타입 경계가 어디인가"를 보는 것이 이 절의 목표다. 한국어 자료에서 이 시각이 특히 빈약하다.

### React Native + TypeScript의 기본 구조

React Native는 기본적으로 JavaScript로 동작한다. TypeScript는 완벽하게 지원된다. Expo를 쓰면 처음부터 TypeScript 프로젝트로 시작할 수 있다.

```bash
# Expo로 TS 프로젝트 시작
npx create-expo-app@latest my-app --template blank-typescript
```

```typescript
// App.tsx
import React, { useState } from 'react'
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native'

interface CounterProps {
  initialCount?: number
  label: string
}

function Counter({ initialCount = 0, label }: CounterProps) {
  const [count, setCount] = useState(initialCount)

  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <TouchableOpacity onPress={() => setCount(c => c + 1)}>
        <Text style={styles.button}>+1</Text>
      </TouchableOpacity>
      <Text style={styles.count}>{count}</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  label: { fontSize: 18, marginBottom: 10 },
  button: { fontSize: 24, color: 'blue' },
  count: { fontSize: 32, fontWeight: 'bold' },
})

export default function App() {
  return <Counter label="카운터" initialCount={0} />
}
```

웹 React와 거의 같다. `View`가 `div`, `Text`가 `span`, `TouchableOpacity`가 `button`에 대응한다. 그리고 `props`는 TypeScript 인터페이스로 타입을 정의한다.

**`@types/react-native`**는 React Native의 공식 TypeScript 타입 정의를 제공한다. 다만 최근 React Native는 자체적으로 TypeScript 타입을 포함하고 있어서, 별도 `@types/react-native`를 설치하지 않아도 되는 경우가 늘고 있다.

> 📚 **Java/Kotlin 시선 — Android Jetpack Compose ↔ React Native (UI 선언 모델)**
>
> Android 개발을 Kotlin + Jetpack Compose로 해봤다면 React Native의 선언형 UI가 낯설지 않을 것이다. Jetpack Compose도 같은 패러다임 — 상태가 바뀌면 UI가 재계산된다.

```kotlin
// Compose
@Composable
fun Counter(label: String, initialCount: Int = 0) {
    var count by remember { mutableStateOf(initialCount) }
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label)
        Button(onClick = { count++ }) { Text("+1") }
        Text(text = count.toString(), fontSize = 32.sp)
    }
}
```

```tsx
// React Native (TypeScript)
function Counter({ label, initialCount = 0 }: CounterProps) {
  const [count, setCount] = useState(initialCount)
  return (
    <View>
      <Text>{label}</Text>
      <TouchableOpacity onPress={() => setCount(c => c + 1)}>
        <Text>+1</Text>
      </TouchableOpacity>
      <Text>{count}</Text>
    </View>
  )
}
```

> 선언형 UI라는 패러다임은 같다. 차이는 렌더링 엔진 — Compose는 Canvas에 직접 그리고, React Native는 JS 로직을 실행하고 그 결과로 iOS/Android 네이티브 컴포넌트를 조작한다. 그래서 성능 특성이 다르고, 네이티브 API 접근 방식도 다르다.

### Expo SDK의 타입 모델

Expo는 React Native 위에 올라가는 SDK다. 카메라, 위치 정보, 파일 시스템, 알림 같은 네이티브 기능을 TS 인터페이스로 깔끔하게 제공한다.

```typescript
import * as Location from 'expo-location'
import * as FileSystem from 'expo-file-system'
import { Camera, CameraType } from 'expo-camera'

// 위치 정보 요청 — 타입이 명확하다
async function getCurrentLocation(): Promise<Location.LocationObject> {
  const { status } = await Location.requestForegroundPermissionsAsync()
  if (status !== 'granted') {
    throw new Error('위치 권한이 없습니다')
  }
  return Location.getCurrentPositionAsync({})
}

// 파일 작업
async function saveUserData(data: string): Promise<void> {
  const fileUri = FileSystem.documentDirectory + 'user-data.json'
  await FileSystem.writeAsStringAsync(fileUri, data)
}

// 카메라 권한 확인
async function requestCameraPermission(): Promise<boolean> {
  const { status } = await Camera.requestCameraPermissionsAsync()
  return status === 'granted'
}
```

`Location.LocationObject`, `Camera.requestCameraPermissionsAsync` — 네이티브 API가 TypeScript 타입으로 표현된다. 물론 내부적으로는 Expo SDK가 iOS Swift / Android Kotlin 코드를 감싸고 있지만, TypeScript 코드를 쓰는 개발자는 그 경계를 직접 다루지 않아도 된다.

이것이 Expo의 핵심 가치다. 네이티브 개발 없이 모바일 기능을 TS로 쓸 수 있는 추상화 레이어. 물론 이 추상화가 필요한 기능을 지원하지 않거나, 성능이 중요한 케이스에서는 한계가 온다. 그때 "네이티브 모듈"을 직접 만드는 길이 있다. 그리고 그 경계를 다루는 기술이 React Native의 신 아키텍처 — JSI와 Fabric이다.

### JSI/Fabric 신 아키텍처 — 타입 경계의 핵심

React Native의 구 아키텍처는 JavaScript 쓰레드와 네이티브 쓰레드가 **비동기 브릿지**로 소통했다. JS 코드가 버튼을 눌렀다고 알리면, 직렬화된 메시지가 브릿지를 건너 네이티브 쓰레드에 도착하고, 네이티브가 처리한 결과가 다시 브릿지를 건너 JS로 돌아왔다. 이 과정이 비동기이기 때문에 빠른 스크롤이나 복잡한 애니메이션에서 버벅임이 생겼다.

**JSI(JavaScript Interface)**는 이 브릿지를 제거한다. C++로 구현된 인터페이스 레이어로 JS 엔진(Hermes)과 네이티브 코드(C++/Swift/Kotlin)가 직접 동기적으로 소통한다. 직렬화가 없다. 복사가 없다. JS에서 네이티브 객체를 직접 참조할 수 있다.

**TurboModule**은 이 JSI를 활용해 네이티브 모듈을 만드는 새로운 방식이다. 그리고 여기서 TypeScript가 핵심 역할을 한다.

```typescript
// NativeCalculator.ts — TurboModule 타입 정의
import type { TurboModule } from 'react-native'
import { TurboModuleRegistry } from 'react-native'

export interface Spec extends TurboModule {
  // 이 스펙이 실제로 iOS .mm 파일과 Android .kt 파일로 코드 생성된다
  add(a: number, b: number): Promise<number>
  multiply(a: number, b: number): number  // 동기 메서드도 가능
}

export default TurboModuleRegistry.getEnforcing<Spec>('NativeCalculator')
```

이 `Spec` 인터페이스가 단순한 타입 정의가 아니다. **codegen**이라는 과정이 이 TypeScript 파일을 읽어서 C++, Objective-C, Kotlin 파일을 자동 생성한다.

```
NativeCalculator.ts (TypeScript)
    ↓ codegen
NativeCalculator.h (C++ 헤더)
NativeCalculatorSpec.mm (iOS/ObjC)
NativeCalculatorSpec.kt (Android/Kotlin)
```

```objc
// 자동 생성된 NativeCalculatorSpec.mm (iOS)
// (실제로는 더 복잡하지만 원리 설명용)
@interface RCTNativeCalculator : NSObject <NativeCalculatorSpec>
@end

@implementation RCTNativeCalculator
- (void)add:(double)a b:(double)b resolve:(RCTPromiseResolveBlock)resolve reject:(RCTPromiseRejectBlock)reject {
    resolve(@(a + b));
}
- (double)multiply:(double)a b:(double)b {
    return a * b;
}
@end
```

이것이 핵심이다. TypeScript의 `Spec` 인터페이스가 iOS Objective-C 코드와 Android Kotlin 코드의 시그니처를 강제한다. TypeScript에서 `add(a: number, b: number): Promise<number>` 라고 선언하면, 네이티브 구현도 반드시 그 계약을 지켜야 한다. 지키지 않으면 codegen이 컴파일 에러를 낸다.

이것은 5장의 "타입을 만드는 타입"이 언어 경계를 넘는 가장 극적인 예다. TypeScript 타입이 C++, Objective-C, Kotlin의 코드를 생성한다. Tauri에서 Rust 타입이 TypeScript 타입으로 흘러내려갔다면, TurboModule codegen에서는 TypeScript 타입이 네이티브 코드로 흘러내려간다. 방향이 반대다.

**Fabric**은 UI 레이어의 신 아키텍처다. React 컴포넌트 트리(JS)가 C++ 레이어(Shadow Tree)와 동기적으로 연결된다. 애니메이션과 제스처가 JS 쓰레드를 거치지 않고 직접 네이티브 레이어에서 처리될 수 있다. 결과적으로 60fps(또는 120fps) 애니메이션이 훨씬 안정적으로 돌아간다.

> 🔑 **TurboModule codegen과 Tauri specta의 평행**
>
> 두 기술이 비슷한 문제를 다른 방향에서 푼다.
>
> - **tauri-specta**: Rust 타입 → TypeScript 타입 (Rust가 원천)
> - **RN TurboModule codegen**: TypeScript 타입 → 네이티브 코드 (TypeScript가 원천)
>
> 두 경우 모두 "언어 경계에서 타입 계약을 자동으로 만든다"는 목표는 같다. 수동으로 양쪽을 맞추는 번거로움과 실수를 없애는 것이다.

### 한국 기업의 RN 부분 도입 — 현재진행형

토스, 당근, 쿠팡이츠의 RN 도입은 "우리 앱 전체를 RN으로 다시 짠다"가 아니었다. 그보다는 훨씬 실용적인 접근이었다.

**토스**는 금융 앱의 특성상 결제나 생체인증 화면은 네이티브로 유지하면서, 자주 바뀌는 이벤트 화면이나 일부 정보 화면을 RN으로 만든다. OTA 업데이트 덕분에 마케팅팀이 원하는 이벤트 화면을 앱 스토어 심사 없이 빠르게 바꿀 수 있다.

**당근**은 디자인 시스템을 공유하는 방식으로 웹·앱·데스크톱 플랫폼 간 일관성을 추구한다. RN 컴포넌트와 웹 React 컴포넌트가 같은 디자인 토큰을 참조하고, TypeScript로 props 타입을 공유한다.

**쿠팡이츠**는 배달 화면처럼 지도와 실시간 업데이트가 많은 부분은 네이티브, 메뉴 탐색이나 주문 내역 같은 콘텐츠 중심 화면은 RN으로 나누는 패턴을 쓴다.

이 패턴의 공통점은 "경계를 의식적으로 설계한다"는 것이다. 어느 화면이 RN이고 어느 화면이 네이티브인지, 어느 기능이 Expo SDK로 충분하고 어느 기능이 TurboModule이 필요한지. 이 경계 설계가 잘못되면 성능 문제와 유지보수 지옥이 기다린다.

### React Native vs 네이티브 개발 — 결정 표

Electron vs Tauri와 평행하게, React Native vs 네이티브 iOS/Android 개발의 트레이드오프도 표로 보자.

| 기준 | React Native (+ Expo) | 네이티브 (Swift/Kotlin) |
|------|----------------------|------------------------|
| **시작 시간** | 빠름 (한 코드베이스로 iOS/Android) | 플랫폼별로 따로 개발 |
| **바이너리 크기** | 더 크다 (JS 번들 포함) | 작다 |
| **성능** | 충분히 좋음, 구 아키텍처는 한계 있음 | 최상 |
| **애니메이션** | 신 아키텍처(Fabric)로 크게 개선 | 최상 |
| **네이티브 API 접근** | Expo SDK 또는 TurboModule 필요 | 직접 |
| **OTA 업데이트** | 가능 (JS 번들만 교체) | 불가 (앱 스토어 심사 필요) |
| **팀 구성** | JS/TS 개발자가 모바일 참여 가능 | iOS/Android 전문 개발자 필요 |
| **TS 지원** | 완전 지원, TurboModule codegen | Swift 자체 타입, Kotlin 자체 타입 |
| **한국 채택** | 토스·당근·쿠팡이츠 부분 도입 | 대부분의 한국 앱 메인 화면 |

**React Native가 더 나은 경우:**
- iOS와 Android를 동시에 만들어야 하는데 팀이 작을 때
- 자주 바뀌는 콘텐츠 화면 (OTA의 강점)
- 웹 React 팀이 모바일에도 기여해야 할 때
- 디자인 시스템을 웹과 공유하고 싶을 때

**네이티브가 더 나은 경우:**
- 결제, 생체인증 등 보안이 핵심인 화면
- 고성능 애니메이션, 게임, 카메라 실시간 처리
- 플랫폼 최신 API를 즉시 써야 할 때
- 앱의 핵심 가치가 플랫폼 특유 경험일 때

기억해두자. React Native는 "네이티브 대신"이 아니라 "네이티브와 함께"다. 잘 쓰는 팀은 경계를 의식적으로 설계하고 있다.

---

## 데스크톱과 모바일의 공통점 — TypeScript가 서는 자리

이 챕터를 관통하는 하나의 질문이 있다. **TypeScript의 정적 타입이 네이티브 경계까지 얼마나 닿을 수 있는가?**

Electron에서는 `contextBridge`와 `ipcMain.handle`의 문자열 채널이 경계다. electron-trpc가 그 경계를 넘어 `AppRouter` 타입을 공유한다.

Tauri에서는 `invoke('rust_command', args)` 가 경계다. tauri-specta가 그 경계를 넘어 Rust 타입을 TypeScript 타입으로 변환한다.

React Native에서는 JS 쓰레드와 네이티브 쓰레드 사이의 브릿지가 경계다. TurboModule codegen이 그 경계를 넘어 TypeScript `Spec` 인터페이스를 iOS/Android 네이티브 코드로 변환한다.

세 경우 모두 "경계를 수동으로 관리하면 타입이 없다"는 문제가 있었고, "타입 계약을 자동으로 생성하면 경계도 안전해진다"는 해법이 있었다. 도구 이름이 다를 뿐이다.

그리고 이것은 5장에서 배운 "타입을 만드는 타입"이 가장 극적으로 쓰이는 곳이다. 단순히 `Array<T>`를 `ReadonlyArray<T>`로 바꾸는 게 아니라, 한 언어의 타입 정보를 다른 언어의 코드로 뽑아내는 일이다.

---

## 마무리

데스크톱과 모바일 영역에서 TypeScript는 "웹의 언어"가 UI 레이어를 담당하고, 네이티브 경계에서 타입 계약을 자동으로 잇는 방식으로 자리를 잡았다.

Electron과 Tauri 중 어느 것을 선택할지는 팀의 역량, 앱의 성격, 배포 환경에 따라 다르다. "Electron은 낡았다, Tauri가 미래다"라는 단순한 결론보다는, 두 도구가 서로 다른 트레이드오프를 가진다는 것을 이해하고 선택하는 편이 낫다. Electron의 생태계 성숙도와 낮은 진입 장벽은 여전히 가치 있다.

React Native와 Expo는 TypeScript 개발자가 모바일에 기여하는 가장 현실적인 길이다. JSI/Fabric의 신 아키텍처와 TurboModule codegen은 TS 타입 계약이 네이티브 코드까지 닿는 방식을 계속 정교하게 만들고 있다. 토스, 당근, 쿠팡이츠의 RN 도입은 완성된 이야기가 아니라 현재진행형이다.

한 가지만 기억해두자. 경계를 의식하라. 웹과 데스크톱의 경계, JS와 네이티브의 경계, TypeScript와 Rust/C++의 경계. 그 경계에서 타입이 사라지지 않도록 도구를 선택하고 패턴을 설계하는 것 — 그것이 이 챕터가 말하려는 핵심이다.

다음 12장에서는 웹 프론트엔드로 초점을 옮긴다. React + TypeScript가 컴포넌트 props·이벤트·ref·상태를 타입의 결로 어떻게 표현하는지, 그리고 Vue·Svelte·Solid가 어떻게 다른 reactivity 모델로 같은 문제를 푸는지 살펴보자.

---

> 📖 **더 깊이 가려면**
>
> - **Electron 공식 문서** — Process Model, Security, contextBridge: https://www.electronjs.org/docs/latest/tutorial/process-model
> - **Tauri v2 공식 문서** — Concepts, invoke, Plugins: https://v2.tauri.app/
> - **tauri-specta** — Rust→TS 타입 내보내기: https://github.com/oscartbeaumont/specta (tauri-specta 패키지 포함)
> - **electron-trpc** — Electron + tRPC 조합: https://github.com/jsonnull/electron-trpc
> - **React Native 신 아키텍처** — JSI, TurboModules, Fabric: https://reactnative.dev/docs/the-new-architecture/landing-page
> - **Expo 공식 문서** — SDK 타입, EAS Build: https://docs.expo.dev/
> - **React Native TurboModule codegen** — https://reactnative.dev/docs/native-modules-intro (새 아키텍처 섹션)
