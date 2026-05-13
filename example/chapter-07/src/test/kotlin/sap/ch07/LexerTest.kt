package sap.ch07

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import sap.ch07.asm.Lexer
import sap.ch07.asm.Token

class LexerTest : DescribeSpec({
    describe("Lexer") {
        it("주석 무시") {
            val toks = Lexer.tokenize("; this is a comment\nLDA \$9")
                .filter { it !is Token.Newline }
            toks shouldBe listOf(Token.Mnemonic("LDA"), Token.Number(9))
        }
        it("라벨 인식") {
            val toks = Lexer.tokenize("start: LDA \$9").filter { it !is Token.Newline }
            (toks[0] as Token.Label).name shouldBe "start"
            toks[1] shouldBe Token.Mnemonic("LDA")
        }
        it("\$로 시작하는 hex") {
            val toks = Lexer.tokenize("\$2A").filter { it !is Token.Newline }
            toks shouldBe listOf(Token.Number(0x2A))
        }
        it("OUT, HLT는 operand 없음") {
            val toks = Lexer.tokenize("OUT\nHLT").filter { it !is Token.Newline }
            toks shouldBe listOf(Token.Mnemonic("OUT"), Token.Mnemonic("HLT"))
        }
    }
})
