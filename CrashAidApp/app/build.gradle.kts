plugins {
    id("com.android.application")
    id("com.google.gms.google-services")  // Apply here
}

dependencies {
    // Firebase BOM - ensures compatible versions
    implementation(platform("com.google.firebase:firebase-bom:34.6.0"))

    // Firebase Messaging
    implementation("com.google.firebase:firebase-messaging")

    // Firebase Analytics (optional, recommended)
    implementation("com.google.firebase:firebase-analytics")
}
