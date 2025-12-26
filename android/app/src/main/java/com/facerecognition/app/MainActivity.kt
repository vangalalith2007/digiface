package com.facerecognition.app

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.*
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.activity.OnBackPressedCallback

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val PERMISSION_REQUEST_CODE = 100
    
    // Flask server URL - Change this for production
    // private val SERVER_URL = "http://10.0.2.2:5000"  // For Android emulator
    private val SERVER_URL = "https://your-production-domain.com" // Update this!
    // For real device on same network, use: "http://YOUR_PC_IP:5000"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Check and request permissions
        if (checkPermissions()) {
            initializeWebView()
        } else {
            requestPermissions()
        }
    }

    private fun checkPermissions(): Boolean {
        val cameraPermission = ContextCompat.checkSelfPermission(
            this, Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
        
        val audioPermission = ContextCompat.checkSelfPermission(
            this, Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED
        
        return cameraPermission && audioPermission
    }

    private fun requestPermissions() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(
                Manifest.permission.CAMERA,
                Manifest.permission.RECORD_AUDIO
            ),
            PERMISSION_REQUEST_CODE
        )
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && 
                grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                initializeWebView()
            } else {
                Toast.makeText(
                    this,
                    "Camera and microphone permissions are required",
                    Toast.LENGTH_LONG
                ).show()
                finish()
            }
        }
    }

    private fun initializeWebView() {
        webView = WebView(this)
        setContentView(webView)
        
        // WebView settings
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            mediaPlaybackRequiresUserGesture = false
            allowFileAccess = true
            allowContentAccess = true
            
            // Enable zoom controls
            setSupportZoom(true)
            builtInZoomControls = true
            displayZoomControls = false
            
            // Cache settings
            cacheMode = WebSettings.LOAD_DEFAULT
            
            // Mixed content (for development)
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        // WebViewClient for handling page navigation
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                return false
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                Toast.makeText(
                    this@MainActivity,
                    "App loaded successfully",
                    Toast.LENGTH_SHORT
                ).show()
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                Toast.makeText(
                    this@MainActivity,
                    "Error loading page: ${error?.description}",
                    Toast.LENGTH_LONG
                ).show()
            }
        }

        // WebChromeClient for handling permissions and dialogs
        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                // Grant camera and microphone permissions to WebView
                request?.grant(request.resources)
            }

            override fun onConsoleMessage(consoleMessage: ConsoleMessage?): Boolean {
                // Log console messages for debugging
                consoleMessage?.let {
                    android.util.Log.d(
                        "WebView",
                        "${it.message()} -- From line ${it.lineNumber()} of ${it.sourceId()}"
                    )
                }
                return true
            }

            override fun onJsAlert(
                view: WebView?,
                url: String?,
                message: String?,
                result: JsResult?
            ): Boolean {
                // Handle JavaScript alerts
                Toast.makeText(this@MainActivity, message, Toast.LENGTH_LONG).show()
                result?.confirm()
                return true
            }
        }

        // Optional: Add JavaScript interface for native features
        webView.addJavascriptInterface(AndroidBridge(), "Android")

        // Load the Flask server URL
        webView.loadUrl(SERVER_URL)

        // Handle back button presses using OnBackPressedDispatcher
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    // Disable this callback and trigger the default back behavior
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })
    }

    // JavaScript Bridge for native features
    inner class AndroidBridge {
        @JavascriptInterface
        fun showToast(message: String) {
            runOnUiThread {
                Toast.makeText(this@MainActivity, message, Toast.LENGTH_SHORT).show()
            }
        }

        @JavascriptInterface
        fun getDeviceInfo(): String {
            return """
                {
                    "model": "${android.os.Build.MODEL}",
                    "manufacturer": "${android.os.Build.MANUFACTURER}",
                    "version": "${android.os.Build.VERSION.RELEASE}",
                    "sdk": ${android.os.Build.VERSION.SDK_INT}
                }
            """.trimIndent()
        }
    }


    override fun onDestroy() {
        super.onDestroy()
        webView.destroy()
    }
}
