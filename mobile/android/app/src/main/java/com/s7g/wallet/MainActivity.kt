// S7G Mobile OTA — Android Stub
// App Store-compliant minimal shell + P2P bundle resolver
// The stub is <5MB, and all app features arrive via P2P OTA.

package com.s7g.wallet

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import android.webkit.JavascriptInterface
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import java.io.InputStream
import java.net.Socket
import java.security.MessageDigest

// Configuration — set at build time from pair seed
const val S7G_DISCOVERY_KEY = "3d021065344c95244b3ee925c9beb61cf1f94d2a588972161b1a7852f4f208ab"
const val S7G_SEEDER_HOST = "iroh-seeder.s7g.network"
const val S7G_SEEDER_PORT = 9090
const val S7G_BUNDLE_TIMEOUT_MS = 30000L

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.addJavascriptInterface(BridgeInterface(), "S7GBridge")
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean = false
        }
        setContentView(webView)
        
        showLoading()
        resolveBundle()
    }
    
    private fun showLoading() {
        val loadingHtml = """
        <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;
              background:#1a1a2e;color:#e94560;font-family:sans-serif;">
        <div style="text-align:center">
            <h2>S7G Wallet</h2>
            <p>Connecting to P2P network...</p>
            <progress></progress>
        </div>
        </body></html>
        """.trimIndent()
        webView.loadDataWithBaseURL(null, loadingHtml, "text/html", "UTF-8", null)
    }
    
    private fun resolveBundle() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // Connect to P2P seeder via TCP
                val socket = Socket()
                socket.connect(
                    java.net.InetSocketAddress(S7G_SEEDER_HOST, S7G_SEEDER_PORT),
                    S7G_BUNDLE_TIMEOUT_MS.toInt()
                )
                
                // Send discovery key as raw 32 bytes
                val keyBytes = hexStringToBytes(S7G_DISCOVERY_KEY)
                socket.getOutputStream().write(keyBytes)
                socket.getOutputStream().flush()
                
                // Read bundle data
                val bundleBytes = socket.getInputStream().readBytes()
                socket.close()
                
                // Load bundle in WebView
                withContext(Dispatchers.Main) {
                    val bundleString = String(bundleBytes, Charsets.UTF_8)
                    val html = """
                    <html><head><meta name="viewport" content="width=device-width,initial-scale=1">
                    <script>$bundleString</script></head><body></body></html>
                    """.trimIndent()
                    webView.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null)
                }
                
            } catch (e: Exception) {
                withContext(Dispatchers.Main) { showFallbackUI(e.message) }
            }
        }
    }
    
    private fun showFallbackUI(error: String?) {
        val fallbackHtml = """
        <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;
              background:#1a1a2e;color:#e94560;font-family:sans-serif;">
        <div style="text-align:center;max-width:300px">
            <h2>S7G Wallet</h2>
            <p style="color:#888">Unable to connect to P2P network.</p>
            <p style="color:#888;font-size:12px">${error ?: ""}</p>
            <button onclick="location.reload()" style="margin-top:20px;padding:10px 20px;
                  background:#e94560;color:white;border:none;border-radius:5px;">
                Retry
            </button>
        </div>
        </body></html>
        """.trimIndent()
        webView.loadDataWithBaseURL(null, fallbackHtml, "text/html", "UTF-8", null)
    }
    
    // JavaScript bridge for P2P operations
    inner class BridgeInterface {
        @JavascriptInterface
        fun getDiscoveryKey(): String = S7G_DISCOVERY_KEY
        
        @JavascriptInterface
        fun getStubVersion(): String = "1.0.0"
    }
    
    companion object {
        fun hexStringToBytes(hex: String): ByteArray {
            val len = hex.length / 2
            val bytes = ByteArray(len)
            for (i in 0 until len) {
                bytes[i] = Integer.parseInt(hex.substring(i * 2, i * 2 + 2), 16).toByte()
            }
            return bytes
        }
        
        fun sha256Hex(data: ByteArray): String {
            val digest = MessageDigest.getInstance("SHA-256")
            return digest.digest(data).joinToString("") { "%02x".format(it) }
        }
    }
}
