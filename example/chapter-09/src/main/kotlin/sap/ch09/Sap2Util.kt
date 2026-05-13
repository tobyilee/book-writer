package sap.ch09

import sap.ch09.asm.Sap2Assembler

/** 테스트·데모 헬퍼: 소스 한 덩어리를 받아 어셈블·로드·실행하고 머신을 반환한다. */
fun assembleAndRun(source: String, maxSteps: Int = 1_000_000): Sap2 {
    val bytes = Sap2Assembler.assemble(source)
    val sap2 = Sap2()
    sap2.loadProgram(bytes)
    sap2.run(maxSteps)
    return sap2
}
