package sap.ch08.asm

sealed class Token {
    data class Label(val name: String) : Token()        // "start:"
    data class Mnemonic(val name: String) : Token()     // "LDA", "ADD", "OUT", "HLT"
    data class Number(val value: Int) : Token()         // 9, $2A, 0xA
    data class Identifier(val name: String) : Token()   // bare addr labels like "9:" or symbol refs
    data object Newline : Token()
}

object Lexer {
    private val mnemonics = setOf("LDA", "ADD", "SUB", "OUT", "HLT")

    fun tokenize(source: String): List<Token> {
        val tokens = mutableListOf<Token>()
        for (rawLine in source.lineSequence()) {
            val line = rawLine.substringBefore(';').trim()
            if (line.isEmpty()) continue

            // Split on whitespace and ','
            val parts = mutableListOf<String>()
            var i = 0
            while (i < line.length) {
                val c = line[i]
                when {
                    c.isWhitespace() -> i++
                    c == ',' -> i++
                    else -> {
                        val start = i
                        while (i < line.length && !line[i].isWhitespace() && line[i] != ',') i++
                        parts.add(line.substring(start, i))
                    }
                }
            }

            for (part in parts) {
                when {
                    part.endsWith(":") -> {
                        val name = part.dropLast(1)
                        tokens.add(Token.Label(name))
                    }
                    part.startsWith("$") -> {
                        tokens.add(Token.Number(part.drop(1).toInt(16)))
                    }
                    part.uppercase() in mnemonics -> {
                        tokens.add(Token.Mnemonic(part.uppercase()))
                    }
                    part.all { it.isDigit() } -> tokens.add(Token.Number(part.toInt()))
                    else -> tokens.add(Token.Identifier(part))
                }
            }
            tokens.add(Token.Newline)
        }
        return tokens
    }
}
