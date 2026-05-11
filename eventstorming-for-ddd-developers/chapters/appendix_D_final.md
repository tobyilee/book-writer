# 부록 D. Sprout Method 시나리오 — 워크숍 hotspot이 PR로 가는 구체 예

9장에서 약속한 한 시나리오다. 워크숍의 핫핑크 sticky 한 장이 *git churn 데이터*와 만나고, *Feathers의 Sprout Method*를 거쳐, 1~2주 분량의 PR 시리즈가 되는 과정을 따라가본다. 본문에서 이 부록을 분리한 이유가 있다 — 코드 스니펫과 PR 시퀀스가 길어진다. 9장의 호흡을 흩지 않으려면 이 자리에 두는 편이 낫다.

가상의 팀을 잡자. 한국의 중간 규모 쇼핑몰 *오레만들*. 주문·결제·배송·쿠폰을 다 자체 시스템에서 운영하고, Spring Boot 모놀리스 한 덩어리로 5년 운영 중이다. 코드베이스는 65,000라인. 백엔드 개발자 8명. 어제 첫 EventStorming 워크숍을 두 시간 돌렸다.

벽에 남은 핫핑크 중 한 장에 이렇게 적혀 있다.

> *쿠폰 적용 로직이 5군데에서 중복되고 누구도 정확히 모른다.*

이 한 장이 다음 두 주 동안 어디로 가는지를 보자.

## 1단계. 핫핑크와 git churn을 겹쳐 본다

워크숍 다음 날 아침, facilitator 역할을 맡은 박 시니어가 회의실에 다시 들어간다. 노트북을 켜고 `git log`를 돌린다. *최근 6개월 동안 가장 자주 변경된 파일* 상위 20개를 뽑는 한 줄 명령이다.

```bash
git log --since="6 months ago" --name-only --pretty=format: \
  | grep "\.java$" \
  | sort | uniq -c | sort -rn | head -20
```

결과를 출력해보니, 상위 10개 중 4개가 *쿠폰*과 관련이 있다.

```
  47  src/main/java/com/oremandle/order/OrderService.java
  41  src/main/java/com/oremandle/coupon/CouponService.java
  33  src/main/java/com/oremandle/payment/PaymentService.java
  29  src/main/java/com/oremandle/order/OrderItemValidator.java
  ...
```

`OrderService.placeOrder()`, `CouponService.applyCoupon()`, `PaymentService.calculateFinalAmount()`, `OrderItemValidator.validate()` — 네 군데서 *각자의 방식으로* 쿠폰을 다룬다. IDE에서 `coupon.apply(` 같은 호출 패턴을 검색하면 사실은 다섯 군데 이상 나온다. 어떤 자리는 *VIP 가산*을 처리하고, 어떤 자리는 *최소 주문 금액*만 따지고, 어떤 자리는 *카테고리 제외*를 자체적으로 한다. 같은 도메인 룰을 다섯 곳에서 *조금씩 다르게* 구현하고 있다.

이게 *워크숍 hotspot과 코드 hotspot이 겹친 자리*다. 도메인 전문가는 *"쿠폰이 헷갈린다"*고 짚었고, git은 *"이 파일들이 자주 흔들린다"*고 신호를 보낸다. 두 신호가 같은 자리를 가리킨다. 9장에서 그린 *동그라미*가 여기 찍힌다. 다음 두 스프린트의 *주제*가 정해졌다.

## 2단계. ADR 한 장으로 결정을 박아둔다

손대기 전, 박 시니어는 한 가지를 먼저 한다. ADR을 한 장 쓴다. 결정의 근거를 *지금* 박아둔다. 두 달 뒤 새 동료가 *"왜 이렇게 짠 거예요?"*를 물을 때 답이 되어줄 자리다.

`docs/adr/0007-unify-coupon-application.md` 한 장이 추가된다.

```markdown
# ADR-0007. 쿠폰 적용 로직을 단일 도메인 모듈로 통합한다

## 맥락
EventStorming 워크숍(2026-05-08)에서 도메인 전문가가 *쿠폰 적용 흐름이
부서마다 다르게 해석된다*고 짚었다. git churn 분석 결과, 쿠폰 관련 로직이
5개 클래스에 흩어져 있고, 최근 6개월 동안 41~47회 변경되었다. 같은 룰이
다섯 자리에서 *조금씩 다르게* 구현되어 있어, 마케팅 부서의 요청이 올 때마다
어느 한 곳을 고치고 나머지가 깨지는 패턴이 반복된다.

## 결정
쿠폰 적용 로직을 `coupon` 모듈 안의 단일 도메인 서비스로 통합한다.
- 새 인터페이스 `CouponApplicationPolicy`를 도입한다.
- 기존 5개 호출자는 한 번에 옮기지 않고 *Sprout Method*로 점진 이관한다.
- 이관 완료 후 옛 로직은 deprecated 표시 → 1 스프린트 뒤 제거.

## 결과
- 단일 진실 자리(single source of truth)가 생긴다.
- 마케팅 요청 시 한 곳만 변경한다.
- 이관 기간 중 *두 구현이 동시에 존재*하므로 임시 복잡도가 늘어난다.
  (의도된 비용, 2주 이내 해소 예정.)
```

이 한 장이 작은데, 결정적이다. 두 달 뒤 마케팅에서 *VIP 누적 정책 변경*을 요청할 때, 이 ADR을 보면 *어디를 손대야 할지*가 명확해진다. ADR이 없으면 같은 토론을 두 달마다 다시 한다.

## 3단계. seam을 찾는다 — Feathers의 첫 질문

이제 코드로 간다. 가장 churn이 높은 자리, `OrderService.placeOrder()`부터 들여다보자. 메서드가 180줄이다. 한가운데에 쿠폰 적용 로직이 박혀 있다.

```java
@Service
public class OrderService {

  // ... 의존성 주입들 ...

  @Transactional
  public Order placeOrder(PlaceOrderCommand cmd) {
    // ... 주문 검증 50줄 ...

    // ↓ 여기가 쿠폰 적용 로직 (대략 40줄)
    Money discount = Money.ZERO;
    if (cmd.couponId() != null) {
      Coupon coupon = couponRepository.findById(cmd.couponId())
          .orElseThrow(() -> new IllegalArgumentException("쿠폰 없음"));
      if (coupon.expiredAt().isBefore(LocalDateTime.now())) {
        throw new CouponExpiredException();
      }
      if (cmd.totalAmount().isLessThan(coupon.minimumOrderAmount())) {
        throw new MinimumAmountNotMetException();
      }
      // VIP 가산 (다른 자리에는 없는 룰)
      if (cmd.customerGrade() == CustomerGrade.VIP) {
        discount = coupon.discountAmount().multiply(1.1);
      } else {
        discount = coupon.discountAmount();
      }
    }
    // ↑ 쿠폰 적용 끝

    // ... 결제 호출, 이벤트 발행 등 90줄 ...
  }
}
```

Feathers의 첫 질문은 *seam이 있는가*다. 답은 *없다*. 쿠폰 로직이 메서드 안에 *직접 박혀* 있어, 이 자리에서 동작을 바꾸려면 메서드 자체를 손대야 한다. 테스트는 *전체 placeOrder를 호출*해서 검증해야 하니, 쿠폰만 단위 테스트하기는 어렵다.

Feathers의 해답이 *Sprout Method*다. 원본을 *직접 고치지 말고*, 옆에 새 메서드를 하나 sprouting(움튼다)한다.

## 4단계. Sprout — 새 인터페이스를 옆에 만든다

박 시니어는 첫 PR에서 *코드를 거의 안 고친다*. 새 자리를 *만들기만* 한다.

```java
// 새 파일: coupon/domain/CouponApplicationPolicy.java
package com.oremandle.coupon.domain;

public interface CouponApplicationPolicy {
  CouponApplicationResult apply(
      CouponId couponId,
      Money totalAmount,
      CustomerGrade grade
  );
}

// 새 파일: coupon/domain/CouponApplicationResult.java
public record CouponApplicationResult(
    Money discount,
    boolean applied,
    String reason
) {}
```

그리고 *기본 구현* 하나를 만든다. 이 구현이 *통합된 룰*의 첫 자리다.

```java
// 새 파일: coupon/domain/DefaultCouponApplicationPolicy.java
@Component
public class DefaultCouponApplicationPolicy implements CouponApplicationPolicy {

  private final CouponRepository repository;

  public DefaultCouponApplicationPolicy(CouponRepository repository) {
    this.repository = repository;
  }

  @Override
  public CouponApplicationResult apply(
      CouponId couponId,
      Money totalAmount,
      CustomerGrade grade
  ) {
    if (couponId == null) {
      return new CouponApplicationResult(Money.ZERO, false, "쿠폰 없음");
    }
    Coupon coupon = repository.findById(couponId)
        .orElseThrow(() -> new IllegalArgumentException("쿠폰 없음"));
    if (coupon.expiredAt().isBefore(LocalDateTime.now())) {
      throw new CouponExpiredException();
    }
    if (totalAmount.isLessThan(coupon.minimumOrderAmount())) {
      throw new MinimumAmountNotMetException();
    }
    Money discount = (grade == CustomerGrade.VIP)
        ? coupon.discountAmount().multiply(1.1)
        : coupon.discountAmount();
    return new CouponApplicationResult(discount, true, "적용됨");
  }
}
```

새 클래스이니 *테스트가 가능*하다. 의존성은 `CouponRepository` 하나뿐이고, 이건 mock으로 쉽게 대체된다.

```java
// 새 파일: coupon/domain/DefaultCouponApplicationPolicyTest.java
class DefaultCouponApplicationPolicyTest {

  private final CouponRepository repository = mock(CouponRepository.class);
  private final DefaultCouponApplicationPolicy policy =
      new DefaultCouponApplicationPolicy(repository);

  @Test
  void VIP_고객이면_10퍼센트_가산이_적용된다() {
    Coupon coupon = aCoupon().discount(Money.of(1000)).build();
    when(repository.findById(any())).thenReturn(Optional.of(coupon));

    CouponApplicationResult result = policy.apply(
        coupon.id(), Money.of(20000), CustomerGrade.VIP
    );

    assertThat(result.discount()).isEqualTo(Money.of(1100));
  }

  // ... 나머지 케이스들 ...
}
```

이 PR이 머지된 시점에 *프로덕션 동작은 한 톨도 안 바뀐다*. `DefaultCouponApplicationPolicy`는 만들어져 있을 뿐, *아무도 호출하지 않는다*. 하지만 *호출 가능한 자리*가 생겼다. 다음 PR부터 점진적으로 옮길 수 있다. 위험은 0이고, 안전망이 깔린다.

## 5단계. 첫 호출자를 옮긴다 — 한 줄 변경

두 번째 PR에서 `OrderService.placeOrder()` 안의 쿠폰 블록을 *한 줄 호출*로 바꾼다.

```java
@Service
public class OrderService {

  private final CouponApplicationPolicy couponPolicy;  // 주입 추가

  @Transactional
  public Order placeOrder(PlaceOrderCommand cmd) {
    // ... 주문 검증 50줄 (변경 없음) ...

    // ↓ 쿠폰 적용 (40줄 → 1줄)
    CouponApplicationResult coupon = couponPolicy.apply(
        cmd.couponId(), cmd.totalAmount(), cmd.customerGrade()
    );
    Money discount = coupon.discount();
    // ↑ 끝

    // ... 결제 호출, 이벤트 발행 등 90줄 (변경 없음) ...
  }
}
```

40줄이 1줄이 됐다. 메서드는 약 140줄로 줄었다. *behavior는 그대로*다. 단위 테스트는 기존 `OrderServiceTest`에서 *쿠폰 부분만* `CouponApplicationPolicy` mock으로 대체하면 된다 — 더 단순해진다.

세 번째 PR은 `PaymentService.calculateFinalAmount()`를 같은 방식으로 옮긴다. 네 번째는 `OrderItemValidator`, 다섯 번째는 나머지. 한 PR이 *한 자리만* 손대니, 코드 리뷰가 가볍고 롤백 단위가 명확하다.

## 6단계. 룰의 차이를 *드러내며* 통합한다

여기서 흥미로운 일이 벌어진다. 다섯 자리를 옮기다 보면 *각자 다른 룰을 갖고 있었다*는 사실이 코드에서 드러난다.

- `OrderService` — VIP 가산을 한다.
- `PaymentService` — VIP 가산을 *안 한다*. 최소 주문 금액만 본다.
- `OrderItemValidator` — 카테고리 제외 룰을 *독자적으로* 한다.
- `CouponService` — 가장 단순. 만료만 본다.
- 나머지 한 자리 — 최소 주문 금액을 *낮게* 계산한다 (배송비 포함).

이걸 *모르고* 통합하면 *어떤 동작이 사라지거나 추가*된다. Sprout Method의 진가가 여기서 나온다. 한 자리씩 옮기면서, *이 자리가 추가로 하던 일*을 발견하면 `CouponApplicationPolicy`에 *옵션 파라미터*로 흡수하거나, *Strategy*로 분기 자리를 만든다.

여기서 박 시니어가 결정해야 할 자리는 *비즈니스 결정*이다. 다섯 자리의 룰이 *우연히 다른 것*인지, *의도적으로 다른 것*인지. 도메인 전문가에게 한 번 더 묻는다. 답이 *우연히 다르다*면 *한 룰*로 통합하고, *의도적으로 다르다*면 *명시적인 옵션*으로 표현한다.

이 대화가 EventStorming 워크숍의 *연장선*이다. 핫핑크 sticky 한 장이 *2주 뒤 도메인 전문가와 다시 만나는 대화*로 자라난다. 워크숍이 1회성이 아니라 *지속되는 도메인 학습*이 되는 자리다.

## 7단계. 옛 코드를 deprecated 처리 → 다음 스프린트에 제거

다섯 자리를 다 옮기고 나면, 옛 쿠폰 로직(있었다면 utility class에 모여 있을 수도 있다)에는 *호출자가 없다*. IDE의 *Find Usages*에서 0건이 나온다. `@Deprecated` 어노테이션을 박고, *1 스프린트 뒤 제거 예정* 주석을 단다.

```java
@Deprecated(forRemoval = true, since = "2026-05-22")
public class CouponLegacyUtil {
  // ... 옛 정적 메서드들 ...
}
```

한 스프린트가 지나, 누군가 *Remove unused* PR을 올린다. 마지막 한 줄로 옛 코드가 사라진다. *워크숍의 핫핑크 한 장*이 2주에 걸쳐 1개 클래스로 응축됐다.

## 마지막. 회고 — 무엇이 좋았나

박 시니어가 2주 뒤 팀 회고에서 한 마디 한다. *"이번 쿠폰 정리, EventStorming에서 시작됐어요. 그날 핫핑크 한 장이 이렇게 됐어요."* 슬랙에 전후 비교 스크린샷을 올린다. 5군데 흩어진 코드와, 한 모듈에 모인 코드. 메서드 길이가 180줄에서 140줄로 줄어든 통계.

이 한 마디가 *다음 워크숍을 정당화*한다. *"한 번 더 해볼까요?"*라는 제안이 가벼워진다. EventStorming은 그렇게 *팀의 의식*이 된다 — 한 워크숍의 핫핑크가 코드 변경의 *씨앗*이라는 경험이 한 번이라도 쌓이면.

## 짚어둘 점 몇 가지

이 시나리오는 *가상*이다. 오레만들이라는 회사는 없다. 한국 팀이 실제로 *공개적으로* 이런 사후 작업을 글로 정리한 사례가 아직 적다(reference §12에서 짚은 한계 중 하나). 이 부록은 *후속 판본에서 한국 사례 인터뷰가 확보되면* 그 사례로 교체될 자리다.

다만 코드 자체의 변환 패턴은 *완전히 일반적*이다. Sprout Method는 Feathers가 *Working Effectively with Legacy Code*에 정리한 그대로다. ADR은 Michael Nygard가 *Documenting Architecture Decisions*에서 제안한 그 양식이다. git churn 분석은 Tornhill의 *Your Code as a Crime Scene*에서 자세히 다룬다. 우리 팀의 핫핑크가 다른 도메인이더라도, *이 7단계 시퀀스*는 거의 그대로 옮길 수 있다.

워크숍의 모든 핫핑크가 이렇게 큰 PR 시리즈가 되지는 않는다. 어떤 핫핑크는 ADR 한 장으로 끝나고, 어떤 핫핑크는 *다음 워크숍의 입구*로만 남는다. 하지만 *큰 변환이 가능하다*는 경험이 한 번이라도 쌓이면, 워크숍의 가치는 팀 안에서 자라기 시작한다. 이 부록은 그 *첫 번째 경험*을 미리 그려본 청사진이다.
