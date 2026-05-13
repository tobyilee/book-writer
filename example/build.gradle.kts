plugins {
    alias(libs.plugins.kotlin.jvm) apply false
}

subprojects {
    // 코드 챕터에만 Kotlin/test 설정 적용 (README only 챕터는 plugin 안 붙음)
    plugins.withId("org.jetbrains.kotlin.jvm") {
        repositories { mavenCentral() }

        dependencies {
            "testImplementation"("io.kotest:kotest-runner-junit5:5.9.1")
            "testImplementation"("io.kotest:kotest-assertions-core:5.9.1")
            "testImplementation"("io.kotest:kotest-property:5.9.1")
        }

        extensions.configure<org.jetbrains.kotlin.gradle.dsl.KotlinJvmProjectExtension> {
            jvmToolchain(17)
        }

        tasks.withType<Test>().configureEach {
            useJUnitPlatform()
        }
    }
}
