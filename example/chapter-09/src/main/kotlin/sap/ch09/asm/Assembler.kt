package sap.ch09.asm

data class AssembledProgram(
    val bytes: IntArray,
    val symbols: Map<String, Int>,
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is AssembledProgram) return false
        return bytes.contentEquals(other.bytes) && symbols == other.symbols
    }

    override fun hashCode(): Int = 31 * bytes.contentHashCode() + symbols.hashCode()
}

object Assembler {
    // SAP-1 5 instructions
    private val opcodes = mapOf(
        "LDA" to 0x0,
        "ADD" to 0x1,
        "SUB" to 0x2,
        "OUT" to 0xE,
        "HLT" to 0xF,
    )
    private val noOperand = setOf("OUT", "HLT")

    /**
     * 2-pass assembler for SAP-1.
     * Pass 1: build symbol table from labels.
     * Pass 2: emit bytes, resolving forward references.
     */
    fun assemble(source: String): AssembledProgram {
        val tokens = Lexer.tokenize(source)
        val lines: List<List<Token>> = tokens
            .fold(mutableListOf<MutableList<Token>>(mutableListOf())) { acc, t ->
                if (t is Token.Newline) {
                    if (acc.last().isNotEmpty()) acc.add(mutableListOf())
                } else {
                    acc.last().add(t)
                }
                acc
            }
            .filter { it.isNotEmpty() }

        // Pass 1: address each line by current address; collect labels
        val symbols = mutableMapOf<String, Int>()
        val annotated = mutableListOf<Pair<Int, List<Token>>>()
        var addr = 0
        for (line in lines) {
            val lineTokens = line.toMutableList()
            while (lineTokens.isNotEmpty() && lineTokens.first() is Token.Label) {
                val labelName = (lineTokens.removeAt(0) as Token.Label).name
                // numeric label like "9:" → that's an address directive (place next datum at this address)
                val numericAddr = labelName.toIntOrNull(16)
                if (numericAddr != null && lineTokens.size == 1 && lineTokens[0] is Token.Number) {
                    addr = numericAddr
                } else {
                    symbols[labelName] = addr
                }
            }
            if (lineTokens.isEmpty()) continue
            annotated.add(addr to lineTokens)
            addr += sizeOf(lineTokens)
        }

        // Pass 2: emit bytes
        val bytes = IntArray(16)
        for ((startAddr, lineTokens) in annotated) {
            val emitted = emit(lineTokens, symbols)
            for ((i, b) in emitted.withIndex()) {
                if (startAddr + i < 16) bytes[startAddr + i] = b
            }
        }
        return AssembledProgram(bytes, symbols)
    }

    private fun sizeOf(tokens: List<Token>): Int {
        if (tokens.isEmpty()) return 0
        return when (tokens[0]) {
            is Token.Mnemonic -> 1  // SAP-1: opcode + addr packed in single byte
            is Token.Number -> 1    // data byte
            else -> 1
        }
    }

    private fun emit(tokens: List<Token>, symbols: Map<String, Int>): IntArray {
        if (tokens.isEmpty()) return IntArray(0)
        return when (val first = tokens[0]) {
            is Token.Number -> intArrayOf(first.value and 0xFF)
            is Token.Mnemonic -> {
                val op = opcodes[first.name] ?: error("Unknown mnemonic: ${first.name}")
                val operandAddr = if (first.name in noOperand) {
                    0
                } else {
                    when (val operand = tokens.getOrNull(1)) {
                        is Token.Number -> operand.value and 0xF
                        is Token.Identifier -> symbols[operand.name]
                            ?: error("Unknown label: ${operand.name}")
                        else -> error("${first.name} requires an operand")
                    }
                }
                intArrayOf((op shl 4) or operandAddr)
            }
            else -> error("Unexpected token: $first")
        }
    }
}
