package risc8.ch13

/**
 * 어셈블 결과 — 명령어 워드 배열과 라벨 심볼 테이블.
 */
data class AssembledProgram(val words: IntArray, val symbols: Map<String, Int>) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is AssembledProgram) return false
        return words.contentEquals(other.words) && symbols == other.symbols
    }

    override fun hashCode(): Int = words.contentHashCode() * 31 + symbols.hashCode()
}

/**
 * RISC-8 두-패스 어셈블러.
 *
 * - 한 줄에 하나의 명령어. `;` 이후는 주석.
 * - 라벨은 `name:` 형태. 한 줄에 여러 라벨 가능. 라벨만 있는 줄도 가능.
 * - 분기/점프 타깃에 라벨이 오면 PC-상대 오프셋으로 자동 계산한다.
 *   (BEQ/BNE는 3-bit signed, JAL은 6-bit signed)
 * - 즉치 숫자는 10진수 또는 `0x` 접두사 16진수, 음수는 부호 그대로.
 */
object Assembler {
    fun assemble(source: String): AssembledProgram {
        val rawLines = source.lineSequence()
            .map { it.substringBefore(';').trim() }
            .filter { it.isNotEmpty() }
            .toList()

        // Pass 1 — 라벨 주소 수집.
        val symbols = mutableMapOf<String, Int>()
        var addr = 0
        val emittable = mutableListOf<Pair<Int, String>>()
        for (line in rawLines) {
            val (labels, rest) = stripLabels(line)
            for (label in labels) symbols[label] = addr
            if (rest.isNotBlank()) {
                emittable.add(addr to rest)
                addr++
            }
        }

        // Pass 2 — 실제 인코딩.
        val words = IntArray(emittable.size)
        for ((i, entry) in emittable.withIndex()) {
            val (insnAddr, line) = entry
            words[i] = encodeLine(line, insnAddr, symbols)
        }
        return AssembledProgram(words, symbols.toMap())
    }

    private fun stripLabels(line: String): Pair<List<String>, String> {
        val labels = mutableListOf<String>()
        var rest = line
        while (true) {
            val colon = rest.indexOf(':')
            if (colon < 0) break
            val candidate = rest.substring(0, colon).trim()
            if (candidate.isEmpty() || candidate.contains(' ') || candidate.contains(',')) break
            labels.add(candidate)
            rest = rest.substring(colon + 1).trim()
        }
        return labels to rest
    }

    private fun encodeLine(line: String, insnAddr: Int, symbols: Map<String, Int>): Int {
        val tokens = line.split(Regex("[,\\s]+")).filter { it.isNotEmpty() }
        require(tokens.isNotEmpty()) { "empty line passed to encodeLine" }
        val mn = tokens[0].uppercase()

        fun reg(s: String): Int {
            val cleaned = s.uppercase().removePrefix("R")
            val n = cleaned.toIntOrNull() ?: error("invalid register: $s")
            require(n in 0..7) { "register out of range (R0..R7): $s" }
            return n
        }

        fun num(s: String): Int = when {
            symbols.containsKey(s) -> symbols[s]!!
            s.startsWith("0x") || s.startsWith("0X") -> s.substring(2).toInt(16)
            s.startsWith("-0x") || s.startsWith("-0X") -> -s.substring(3).toInt(16)
            else -> s.toInt()
        }

        // 분기 타깃이 라벨이면 PC-relative offset으로, 숫자면 그대로 즉치로 쓴다.
        fun branchOff(tok: String): Int =
            if (symbols.containsKey(tok)) symbols[tok]!! - insnAddr - 1 else num(tok)

        return when (mn) {
            "NOP" -> Instruction.Nop().encode()
            "ADD" -> Instruction.Add(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "SUB" -> Instruction.Sub(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "AND" -> Instruction.And(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "OR" -> Instruction.Or(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "XOR" -> Instruction.Xor(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "SHL" -> Instruction.Shl(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "SHR" -> Instruction.Shr(reg(tokens[1]), reg(tokens[2]), reg(tokens[3])).encode()
            "ADDI" -> Instruction.AddI(reg(tokens[1]), reg(tokens[2]), num(tokens[3])).encode()
            "ANDI" -> Instruction.AndI(reg(tokens[1]), reg(tokens[2]), num(tokens[3])).encode()
            "LB" -> Instruction.Lb(reg(tokens[1]), reg(tokens[2]), num(tokens[3])).encode()
            "SB" -> Instruction.Sb(reg(tokens[1]), reg(tokens[2]), num(tokens[3])).encode()
            "BEQ" -> Instruction.Beq(reg(tokens[1]), reg(tokens[2]), branchOff(tokens[3])).encode()
            "BNE" -> Instruction.Bne(reg(tokens[1]), reg(tokens[2]), branchOff(tokens[3])).encode()
            "JAL" -> Instruction.Jal(reg(tokens[1]), branchOff(tokens[2])).encode()
            "JR" -> Instruction.Jr(reg(tokens[1]), reg(tokens[2]), num(tokens[3])).encode()
            "LI" -> Instruction.Li(reg(tokens[1]), num(tokens[2])).encode()
            "ECALL" -> Instruction.Ecall().encode()
            "EBREAK" -> Instruction.Ebreak().encode()
            "HALT" -> Instruction.Halt().encode()
            else -> error("Unknown mnemonic: $mn (line: $line)")
        }
    }
}
