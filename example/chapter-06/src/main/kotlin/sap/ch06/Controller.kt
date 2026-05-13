package sap.ch06

enum class ControlSignal {
    LOAD_A,
    LOAD_B,
    LOAD_OUT,
    ALU_ADD,
    ALU_SUB,
    MEM_READ,
    HALT,
    PC_INC,
}

/**
 * 하드와이어드 시퀀서의 간소 모델.
 * (opcode, T-state) → 활성 control signal 집합으로 매핑한다.
 *
 * SAP-1 명령 사이클은 본래 6 T-state (fetch 3 + execute 3) 이지만,
 * 본 챕터는 "어떤 신호가 어느 T에 켜지는가"의 윤곽만 명시하고
 * cycle-accurate 시뮬레이션은 14장에서 본격적으로 다룬다.
 */
object Controller {
    fun signalsFor(opcode: Int, tState: Int): Set<ControlSignal> {
        // T1~T3 — 모든 명령에 공통인 fetch
        if (tState in 1..3) {
            return when (tState) {
                1 -> setOf(ControlSignal.MEM_READ)
                2 -> setOf(ControlSignal.PC_INC)
                3 -> emptySet()
                else -> emptySet()
            }
        }
        val op = (opcode shr 4) and 0xF
        return when (op) {
            // LDA — T4에서 메모리 → A
            0x0 -> if (tState == 4) {
                setOf(ControlSignal.MEM_READ, ControlSignal.LOAD_A)
            } else {
                emptySet()
            }
            // ADD — T4 메모리 → B, T5 A+B → A
            0x1 -> when (tState) {
                4 -> setOf(ControlSignal.MEM_READ, ControlSignal.LOAD_B)
                5 -> setOf(ControlSignal.ALU_ADD, ControlSignal.LOAD_A)
                else -> emptySet()
            }
            // SUB — T4 메모리 → B, T5 A-B → A
            0x2 -> when (tState) {
                4 -> setOf(ControlSignal.MEM_READ, ControlSignal.LOAD_B)
                5 -> setOf(ControlSignal.ALU_SUB, ControlSignal.LOAD_A)
                else -> emptySet()
            }
            // OUT — T4에서 A → OUT
            0xE -> if (tState == 4) setOf(ControlSignal.LOAD_OUT) else emptySet()
            // HLT — T4에서 정지
            0xF -> if (tState == 4) setOf(ControlSignal.HALT) else emptySet()
            else -> emptySet()
        }
    }
}
