plugins {
    id("com.android.application")
    id("com.chaquo.python")
}

android {
    namespace = "com.kegelhealth.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.kegelhealth.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        ndk {
            abiFilters += listOf("arm64-v8a", "x86_64")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        viewBinding = true
    }
}

chaquopy {
    defaultConfig {
        version = "3.11"
        val buildPy = System.getenv("CHAQUO_PYTHON")
        if (!buildPy.isNullOrBlank()) {
            val buildArgs = System.getenv("CHAQUO_PYTHON_ARGS")
            if (!buildArgs.isNullOrBlank()) {
                buildPython(buildPy, *buildArgs.split(" ").filter { it.isNotBlank() }.toTypedArray())
            } else {
                buildPython(buildPy)
            }
        } else {
            buildPython("py", "-3.11")
        }
        pip {
            install("-r", "src/main/python/requirements.txt")
        }
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.webkit:webkit:1.11.0")
}
