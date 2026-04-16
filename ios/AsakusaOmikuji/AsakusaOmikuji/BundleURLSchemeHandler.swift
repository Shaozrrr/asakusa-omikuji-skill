import Foundation
import WebKit

final class BundleURLSchemeHandler: NSObject, WKURLSchemeHandler {
    private let rootURL: URL

    override init() {
        guard let resourceURL = Bundle.main.resourceURL else {
            fatalError("Bundle resource URL is unavailable.")
        }

        self.rootURL = resourceURL.appendingPathComponent("WebAssets", isDirectory: true)
        super.init()
    }

    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let requestURL = urlSchemeTask.request.url else {
            urlSchemeTask.didFailWithError(BundleSchemeError.invalidURL)
            return
        }

        do {
            let fileURL = try resolveFileURL(for: requestURL)
            let data = try Data(contentsOf: fileURL)
            let response = URLResponse(
                url: requestURL,
                mimeType: mimeType(for: fileURL.pathExtension),
                expectedContentLength: data.count,
                textEncodingName: textEncodingName(for: fileURL.pathExtension)
            )
            urlSchemeTask.didReceive(response)
            urlSchemeTask.didReceive(data)
            urlSchemeTask.didFinish()
        } catch {
            urlSchemeTask.didFailWithError(error)
        }
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {
    }

    private func resolveFileURL(for url: URL) throws -> URL {
        let requestedPath = normalizedPath(url.path)

        let candidates: [String]
        if requestedPath.isEmpty || requestedPath == "app" {
            candidates = ["app/index.html", "index.html"]
        } else if requestedPath.hasSuffix("/") {
            candidates = [requestedPath + "index.html"]
        } else {
            candidates = [requestedPath]
        }

        for candidate in candidates {
            let fileURL = rootURL.appendingPathComponent(candidate)
            if FileManager.default.fileExists(atPath: fileURL.path) {
                return fileURL
            }
        }

        throw BundleSchemeError.missingResource(requestedPath)
    }

    private func normalizedPath(_ path: String) -> String {
        path.trimmingCharacters(in: CharacterSet(charactersIn: "/"))
    }

    private func mimeType(for ext: String) -> String {
        switch ext.lowercased() {
        case "html":
            return "text/html"
        case "css":
            return "text/css"
        case "js":
            return "text/javascript"
        case "json":
            return "application/json"
        case "svg":
            return "image/svg+xml"
        case "png":
            return "image/png"
        case "webmanifest":
            return "application/manifest+json"
        default:
            return "application/octet-stream"
        }
    }

    private func textEncodingName(for ext: String) -> String? {
        switch ext.lowercased() {
        case "html", "css", "js", "json", "webmanifest":
            return "utf-8"
        default:
            return nil
        }
    }
}

enum BundleSchemeError: LocalizedError {
    case invalidURL
    case missingResource(String)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "The native web container received an invalid URL."
        case .missingResource(let path):
            return "The bundled resource could not be found: \(path)"
        }
    }
}
