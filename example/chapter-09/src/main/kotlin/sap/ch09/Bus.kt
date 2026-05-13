package sap.ch09

/**
 * SAP-1의 W-bus.
 * 한 번에 한 모듈만 버스에 값을 올리고, 다른 모듈이 그 값을 읽는다.
 * 본 챕터에서는 단순화된 8비트 값 보관소로 모델링한다 —
 * tri-state 충돌·timing은 14장(cycle-accurate)에서 다룬다.
 */
class Bus {
    var value: Int = 0
        set(v) { field = v and 0xFF }
}
