plugins {
    alias(libs.plugins.kotlin.jvm)
    application
}

application {
    mainClass.set("sap.ch09.HelloDemoKt")
}

tasks.register<JavaExec>("runFib") {
    group = "application"
    description = "SAP-2 Fibonacci 데모를 실행한다."
    mainClass.set("sap.ch09.FibDemoKt")
    classpath = sourceSets["main"].runtimeClasspath
}
