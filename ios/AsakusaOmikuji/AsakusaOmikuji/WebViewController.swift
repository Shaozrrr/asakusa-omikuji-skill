import SafariServices
import UIKit
import WebKit

final class WebViewController: UIViewController {
    private let schemeHandler = BundleURLSchemeHandler()
    private lazy var webView: WKWebView = {
        let userContentController = WKUserContentController()
        userContentController.add(self, name: "haptics")
        userContentController.add(self, name: "share")

        let configuration = WKWebViewConfiguration()
        configuration.setURLSchemeHandler(schemeHandler, forURLScheme: "asakusa")
        configuration.userContentController = userContentController
        configuration.defaultWebpagePreferences.allowsContentJavaScript = true

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.scrollView.alwaysBounceVertical = false
        webView.backgroundColor = UIColor(red: 20 / 255, green: 17 / 255, blue: 17 / 255, alpha: 1)
        webView.isOpaque = false
        webView.customUserAgent = "AsakusaOmikujiApp/1.0"
        return webView
    }()

    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = UIColor(red: 20 / 255, green: 17 / 255, blue: 17 / 255, alpha: 1)
        view.addSubview(webView)

        NSLayoutConstraint.activate([
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            webView.topAnchor.constraint(equalTo: view.topAnchor),
            webView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])

        loadApp()
    }

    override var preferredStatusBarStyle: UIStatusBarStyle {
        .lightContent
    }

    private func loadApp() {
        guard let url = URL(string: "asakusa://app/app/index.html") else {
            return
        }

        webView.load(URLRequest(url: url))
    }

    private func performHaptic(_ type: String) {
        switch type {
        case "selection":
            UISelectionFeedbackGenerator().selectionChanged()
        case "success":
            UINotificationFeedbackGenerator().notificationOccurred(.success)
        case "warning":
            UINotificationFeedbackGenerator().notificationOccurred(.warning)
        case "impactMedium":
            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
        default:
            UIImpactFeedbackGenerator(style: .light).impactOccurred()
        }
    }

    private func presentShareSheet(text: String) {
        let controller = UIActivityViewController(activityItems: [text], applicationActivities: nil)
        if let popover = controller.popoverPresentationController {
            popover.sourceView = view
            popover.sourceRect = CGRect(
                x: view.bounds.midX,
                y: view.bounds.maxY - 44,
                width: 1,
                height: 1
            )
        }
        present(controller, animated: true)
    }
}

extension WebViewController: WKScriptMessageHandler {
    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        switch message.name {
        case "haptics":
            if let payload = message.body as? [String: Any],
               let type = payload["type"] as? String {
                performHaptic(type)
            }
        case "share":
            if let payload = message.body as? [String: Any],
               let text = payload["text"] as? String {
                presentShareSheet(text: text)
            }
        default:
            break
        }
    }
}

extension WebViewController: WKNavigationDelegate {
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction) async -> WKNavigationActionPolicy {
        guard let url = navigationAction.request.url else {
            return .cancel
        }

        if ["http", "https"].contains(url.scheme?.lowercased() ?? "") {
            present(SFSafariViewController(url: url), animated: true)
            return .cancel
        }

        return .allow
    }
}
