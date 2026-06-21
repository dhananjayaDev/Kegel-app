package com.kegelhealth.app

import android.annotation.SuppressLint
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val appUrl = "http://127.0.0.1:5000"

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        Python.getInstance().getModule("android_server").callAttr("start_server")

        webView = findViewById(R.id.webview)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                val url = request.url.toString()
                return if (url.startsWith(appUrl) || url.startsWith("http://127.0.0.1:5000")) {
                    false
                } else {
                    super.shouldOverrideUrlLoading(view, request)
                }
            }
        }

        waitForServer()
    }

    private fun waitForServer(attempt: Int = 0) {
        if (attempt > 60) {
            webView.loadData(
                "<h2>Server starting…</h2><p>Close and reopen the app if this persists.</p>",
                "text/html",
                "UTF-8",
            )
            return
        }

        Thread {
            val ready = try {
                java.net.Socket().use { socket ->
                    socket.connect(java.net.InetSocketAddress("127.0.0.1", 5000), 400)
                    true
                }
            } catch (_: Exception) {
                false
            }

            Handler(Looper.getMainLooper()).post {
                if (ready) {
                    webView.loadUrl(appUrl)
                } else {
                    Handler(Looper.getMainLooper()).postDelayed(
                        { waitForServer(attempt + 1) },
                        250,
                    )
                }
            }
        }.start()
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
