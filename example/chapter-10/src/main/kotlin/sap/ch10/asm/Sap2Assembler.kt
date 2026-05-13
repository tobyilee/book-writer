package sap.ch10.asm

/**
 * SAP-2용 2-pass 어셈블러.
 * 입력은 텍스트(레이블·즉값·문자 리터럴 지원), 출력은 IntArray(0..255) 바이트 시퀀스.
 *
 * 문법 요약:
 *   label:        ; 레이블 선언
 *   LDI A, 42    ; 즉값 로드. 십진/0x16진/$16진/'문자' 허용
 *   MOV A, B
 *   JMP loop     ; 레이블은 절대 16비트 주소로 해석
 *   ; 세미콜론 이후는 주석
 */
object Sap2Assembler {

    fun assemble(source: String): IntArray {
        val cleaned = source.lineSequence()
            .map { it.substringBefore(';').trim() }
            .filter { it.isNotEmpty() }
            .toList()

        val symbols = mutableMapOf<String, Int>()
        val emitJobs = mutableListOf<Pair<Int, List<String>>>() // (address, tokens-without-labels)

        // Pass 1: 주소 산정 + 레이블 등록
        var addr = 0
        for (line in cleaned) {
            var rest = tokenize(line)
            while (rest.isNotEmpty() && rest[0].endsWith(":")) {
                val labelName = rest[0].dropLast(1)
                require(labelName.isNotEmpty()) { "Empty label name in: $line" }
                require(!symbols.containsKey(labelName)) { "Duplicate label: $labelName" }
                symbols[labelName] = addr
                rest = rest.drop(1)
            }
            if (rest.isEmpty()) continue
            emitJobs.add(addr to rest)
            addr += sizeOf(rest)
        }

        // Pass 2: 바이트 방출
        val bytes = mutableListOf<Int>()
        for ((startAddr, tokens) in emitJobs) {
            while (bytes.size < startAddr) bytes.add(0)
            bytes.addAll(emit(tokens, symbols).toList())
        }
        return bytes.toIntArray()
    }

    private fun tokenize(line: String): List<String> {
        val result = mutableListOf<String>()
        val sb = StringBuilder()
        var inQuote = false
        for (c in line) {
            when {
                c == '\'' -> {
                    sb.append(c)
                    inQuote = !inQuote
                }
                inQuote -> sb.append(c)
                c == ',' || c.isWhitespace() -> {
                    if (sb.isNotEmpty()) { result.add(sb.toString()); sb.clear() }
                }
                else -> sb.append(c)
            }
        }
        if (sb.isNotEmpty()) result.add(sb.toString())
        return result
    }

    private fun parseNum(s: String, symbols: Map<String, Int>): Int {
        return when {
            s.length == 3 && s.startsWith("'") && s.endsWith("'") -> s[1].code
            s.startsWith("0x") || s.startsWith("0X") -> s.substring(2).toInt(16)
            s.startsWith("$") -> s.drop(1).toInt(16)
            s.toIntOrNull() != null -> s.toInt()
            symbols.containsKey(s) -> symbols[s]!!
            else -> error("Cannot parse number/symbol: $s")
        }
    }

    private fun sizeOf(tokens: List<String>): Int {
        val mn = tokens[0].uppercase()
        return when (mn) {
            "NOP", "RET", "HLT" -> 1
            "MOV" -> 1
            "ADD", "SUB" -> 1
            "INC", "DEC" -> 1
            "LDI" -> 2
            "JMP", "JZ", "JNZ", "CALL" -> 3
            "IN", "OUT" -> 2
            else -> error("Unknown mnemonic: $mn")
        }
    }

    private fun emit(tokens: List<String>, symbols: Map<String, Int>): IntArray {
        val mn = tokens[0].uppercase()
        return when (mn) {
            "NOP" -> intArrayOf(0x00)
            "LDI" -> {
                val reg = tokens[1].uppercase()
                val imm = parseNum(tokens[2], symbols) and 0xFF
                val op = when (reg) {
                    "A" -> 0x01
                    "B" -> 0x02
                    "C" -> 0x03
                    else -> error("LDI register must be A/B/C, got $reg")
                }
                intArrayOf(op, imm)
            }
            "MOV" -> {
                val dst = tokens[1].uppercase()
                val src = tokens[2].uppercase()
                val op = when ("$dst,$src") {
                    "A,B" -> 0x10
                    "A,C" -> 0x11
                    "B,A" -> 0x12
                    "C,A" -> 0x13
                    "B,C" -> 0x14
                    "C,B" -> 0x15
                    else -> error("Unknown MOV pair: $dst,$src")
                }
                intArrayOf(op)
            }
            "ADD" -> intArrayOf(
                when (tokens[1].uppercase()) {
                    "B" -> 0x20
                    "C" -> 0x21
                    else -> error("ADD operand must be B or C, got ${tokens[1]}")
                },
            )
            "SUB" -> intArrayOf(
                when (tokens[1].uppercase()) {
                    "B" -> 0x22
                    else -> error("SUB operand must be B, got ${tokens[1]}")
                },
            )
            "INC" -> intArrayOf(
                when (tokens[1].uppercase()) {
                    "A" -> 0x30
                    "B" -> 0x31
                    "C" -> 0x32
                    else -> error("INC operand must be A/B/C, got ${tokens[1]}")
                },
            )
            "DEC" -> intArrayOf(
                when (tokens[1].uppercase()) {
                    "A" -> 0x33
                    "C" -> 0x34
                    else -> error("DEC operand must be A or C, got ${tokens[1]}")
                },
            )
            "JMP" -> jumpBytes(0x40, tokens[1], symbols)
            "JZ" -> jumpBytes(0x41, tokens[1], symbols)
            "JNZ" -> jumpBytes(0x42, tokens[1], symbols)
            "CALL" -> jumpBytes(0x50, tokens[1], symbols)
            "RET" -> intArrayOf(0x51)
            "IN" -> intArrayOf(0x60, parseNum(tokens[1], symbols) and 0xF)
            "OUT" -> intArrayOf(0x61, parseNum(tokens[1], symbols) and 0xF)
            "HLT" -> intArrayOf(0xFF)
            else -> error("Unknown mnemonic: $mn")
        }
    }

    private fun jumpBytes(op: Int, target: String, symbols: Map<String, Int>): IntArray {
        val addr = parseNum(target, symbols) and 0xFFFF
        return intArrayOf(op, addr and 0xFF, (addr shr 8) and 0xFF)
    }
}
