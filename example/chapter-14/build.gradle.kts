plugins {
    alias(libs.plugins.kotlin.jvm)
    application
    alias(libs.plugins.jmh)
}

application {
    mainClass.set("risc8.ch14.CycleDemoKt")
}

jmh {
    fork.set(1)
    iterations.set(3)
    warmupIterations.set(2)
    timeOnIteration.set("1s")
    warmup.set("1s")
}
