package sap.ch10

/**
 * SAP-1 마이크로코드 ROM의 마이크로 신호 정의.
 *
 * ch05의 `Controller`(하드와이어드 시퀀서)와 같은 자리에 놓인 개념이지만,
 * 시각이 다르다 — 하드와이어드는 게이트로 신호를 만들고, 마이크로코드는 ROM에서 워드를 읽는다.
 * 그래서 enum 이름도 `ControlSignal`(하드와이어드)과 분리해 `MicroSignal`로 부른다.
 *
 * Malvino의 SAP-1은 12~13개 제어선을 한 바이트의 control word로 묶고
 * T-state(T1~T6) × opcode(LDA/ADD/SUB/OUT/HLT) 매트릭스에 저장한다.
 * 본 책은 그 매트릭스를 enum + lookup 테이블로 옮긴다.
 */
enum class MicroSignal {
    PC_OUT, MAR_LOAD, MEM_OUT, IR_LOAD,
    IR_OUT, A_LOAD, A_OUT,
    B_LOAD, ALU_OUT, ALU_SUB_MODE,
    OUT_LOAD, PC_INC, HALT,
}

/**
 * SAP-1 6-state 마이크로코드 테이블.
 *
 * T1~T3은 모든 명령어가 공유하는 fetch 사이클이고,
 * T4~T6은 opcode마다 다른 execute 사이클이다.
 *
 * 호출자는 (현재 IR의 opcode, 현재 T-state)를 던지고, 활성 마이크로 신호 집합을 받는다.
 * 실제 하드웨어라면 이 set의 비트들이 한 클럭 사이클 동안 동시에 HIGH가 된다.
 */
object MicroRom {
    fun signalsFor(opcode: Int, tState: Int): Set<MicroSignal> {
        // Fetch — 모든 명령어 공통
        when (tState) {
            1 -> return setOf(MicroSignal.PC_OUT, MicroSignal.MAR_LOAD)
            2 -> return setOf(MicroSignal.PC_INC)
            3 -> return setOf(MicroSignal.MEM_OUT, MicroSignal.IR_LOAD)
        }
        // Execute — opcode 상위 4비트로 분기
        val op = (opcode shr 4) and 0xF
        return when (op) {
            0x0 -> when (tState) { // LDA
                4 -> setOf(MicroSignal.IR_OUT, MicroSignal.MAR_LOAD)
                5 -> setOf(MicroSignal.MEM_OUT, MicroSignal.A_LOAD)
                else -> emptySet()
            }
            0x1 -> when (tState) { // ADD
                4 -> setOf(MicroSignal.IR_OUT, MicroSignal.MAR_LOAD)
                5 -> setOf(MicroSignal.MEM_OUT, MicroSignal.B_LOAD)
                6 -> setOf(MicroSignal.ALU_OUT, MicroSignal.A_LOAD)
                else -> emptySet()
            }
            0x2 -> when (tState) { // SUB
                4 -> setOf(MicroSignal.IR_OUT, MicroSignal.MAR_LOAD)
                5 -> setOf(MicroSignal.MEM_OUT, MicroSignal.B_LOAD)
                6 -> setOf(MicroSignal.ALU_OUT, MicroSignal.ALU_SUB_MODE, MicroSignal.A_LOAD)
                else -> emptySet()
            }
            0xE -> when (tState) { // OUT
                4 -> setOf(MicroSignal.A_OUT, MicroSignal.OUT_LOAD)
                else -> emptySet()
            }
            0xF -> when (tState) { // HLT
                4 -> setOf(MicroSignal.HALT)
                else -> emptySet()
            }
            else -> emptySet()
        }
    }
}
