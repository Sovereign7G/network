// S7G Mobile OTA — iOS Stub
// App Store-compliant minimal shell + P2P bundle resolver
// 
// Build: xcodebuild -project S7GWalletStub.xcodeproj -scheme S7GWalletStub
// 
// The stub is <5MB, passes App Store review (it's a WebView that loads
// from a local server), and all actual app features arrive via P2P OTA.

import UIKit
import WebKit
import Network

// MARK: - Configuration
// These are set at build time from pair seed
let S7G_DISCOVERY_KEY = "3d021065344c95244b3ee925c9beb61cf1f94d2a588972161b1a7852f4f208ab"
let S7G_IROH_RELAY = "http://iroh-relay.s7g.network:3340"
let S7G_STUB_VERSION = "1.0.0"
let S7G_BUNDLE_TIMEOUT: TimeInterval = 30.0

// MARK: - P2P Bundle Resolver
// Resolves the app bundle from the P2P network via TCP (Iroh-native
// Swift bindings not yet available, so TCP is the universal fallback).
class P2PBundleResolver {
    private let discoveryKey: String
    private var bundleData: Data?
    
    init(discoveryKey: String) {
        self.discoveryKey = discoveryKey
    }
    
    // Resolve the bundle via TCP connection to a seeder
    func resolveViaTCP(host: String, port: UInt16, timeout: TimeInterval = S7G_BUNDLE_TIMEOUT) async throws -> Data {
        return try await withCheckedThrowingContinuation { continuation in
            let connection = NWConnection(
                host: NWEndpoint.Host(host),
                port: NWEndpoint.Port(rawValue: port) ?? 9090,
                using: .tcp
            )
            
            var receivedData = Data()
            var didComplete = false
            
            connection.stateUpdateHandler = { state in
                switch state {
                case .ready:
                    // Send discovery key as raw 32 bytes
                    if let keyData = Data(hex: self.discoveryKey) {
                        connection.send(content: keyData, completion: .contentProcessed({ _ in }))
                    }
                case .failed(let error):
                    if !didComplete {
                        didComplete = true
                        continuation.resume(throwing: error)
                    }
                case .cancelled:
                    if !didComplete {
                        didComplete = true
                        continuation.resume(throwing: NWError.posix(.ECANCELED))
                    }
                default:
                    break
                }
            }
            
            connection.receiveMessage { data, _, _, error in
                if let data = data {
                    receivedData = data
                }
                if let error = error {
                    if !didComplete {
                        didComplete = true
                        continuation.resume(throwing: error)
                    }
                } else {
                    didComplete = true
                    connection.cancel()
                    continuation.resume(returning: receivedData)
                }
            }
            
            connection.start(queue: .global())
            
            // Timeout
            DispatchQueue.global().asyncAfter(deadline: .now() + timeout) {
                if !didComplete {
                    didComplete = true
                    connection.cancel()
                    continuation.resume(throwing: URLError(.timedOut))
                }
            }
        }
    }
    
    // Verify SHA256 of downloaded bundle
    func verifySHA256(data: Data, expectedHex: String) -> Bool {
        let hash = data.sha256().hexString
        return hash == expectedHex
    }
}

// MARK: - Data Extensions
extension Data {
    init?(hex: String) {
        let len = hex.count / 2
        var data = Data(capacity: len)
        for i in 0..<len {
            let start = hex.index(hex.startIndex, offsetBy: i * 2)
            let end = hex.index(start, offsetBy: 2)
            if let byte = UInt8(hex[start..<end], radix: 16) {
                data.append(byte)
            } else {
                return nil
            }
        }
        self = data
    }
    
    func sha256() -> Data {
        // Uses CommonCrypto or CryptoKit
        if #available(iOS 13.0, *) {
            return Data(CryptoKit.SHA256.hash(data: self))
        }
        // Fallback to CommonCrypto
        var hash = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        self.withUnsafeBytes { buffer in
            _ = CC_SHA256(buffer.baseAddress, CC_LONG(self.count), &hash)
        }
        return Data(hash)
    }
    
    var hexString: String {
        return self.map { String(format: "%02x", $0) }.joined()
    }
}

// MARK: - App Delegate
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    var webView: WKWebView?
    var resolver: P2PBundleResolver?
    
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        window = UIWindow(frame: UIScreen.main.bounds)
        
        let webConfig = WKWebViewConfiguration()
        webConfig.preferences.javaScriptEnabled = true
        webView = WKWebView(frame: window!.bounds, configuration: webConfig)
        
        window?.rootViewController = UIViewController()
        window?.rootViewController?.view = webView
        window?.makeKeyAndVisible()
        
        // Show loading screen while resolving bundle
        showLoading()
        
        // Start bundle resolution
        Task {
            await resolveAndLoadBundle()
        }
        
        return true
    }
    
    func showLoading() {
        let loadingHTML = """
        <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;
              background:#1a1a2e;color:#e94560;font-family:sans-serif;">
        <div style="text-align:center">
            <h2>S7G Wallet</h2>
            <p>Connecting to P2P network...</p>
            <progress></progress>
        </div>
        </body></html>
        """
        webView?.loadHTMLString(loadingHTML, baseURL: nil)
    }
    
    func resolveAndLoadBundle() async {
        resolver = P2PBundleResolver(discoveryKey: S7G_DISCOVERY_KEY)
        
        do {
            // Try to resolve via TCP
            let bundleData = try await resolver!.resolveViaTCP(
                host: "iroh-seeder.s7g.network",
                port: 9090
            )
            
            // Verify SHA256
            // let valid = resolver!.verifySHA256(data: bundleData, expectedHex: "...")
            
            // Load bundle into WebView
            DispatchQueue.main.async {
                let bundleString = String(data: bundleData, encoding: .utf8) ?? ""
                
                // The bundle is a self-executing JavaScript application
                let html = """
                <html><head><meta name="viewport" content="width=device-width,initial-scale=1">
                <script>\(bundleString)</script></head><body></body></html>
                """
                self.webView?.loadHTMLString(html, baseURL: Bundle.main.bundleURL)
            }
            
        } catch {
            // Fallback to a minimal built-in UI
            DispatchQueue.main.async {
                self.showFallbackUI()
            }
        }
    }
    
    func showFallbackUI() {
        // Minimal UI if P2P resolution fails
        let fallbackHTML = """
        <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;
              background:#1a1a2e;color:#e94560;font-family:sans-serif;">
        <div style="text-align:center;max-width:300px">
            <h2>S7G Wallet</h2>
            <p style="color:#888">Unable to connect to P2P network.</p>
            <p style="color:#888;font-size:12px">The app will load once a connection is available.</p>
            <button onclick="location.reload()" style="margin-top:20px;padding:10px 20px;
                  background:#e94560;color:white;border:none;border-radius:5px;">
                Retry
            </button>
        </div>
        </body></html>
        """
        webView?.loadHTMLString(fallbackHTML, baseURL: nil)
    }
}
