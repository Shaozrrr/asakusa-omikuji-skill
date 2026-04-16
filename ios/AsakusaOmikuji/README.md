# AsakusaOmikuji iOS

这是项目的 iOS 原生壳工程。

## 它做了什么

- 使用 `WKWebView` 加载打包进 App Bundle 的 `WebAssets`
- 用自定义 `asakusa://` scheme 提供本地静态资源
- 提供原生触感反馈
- 提供原生系统分享
- 自带 Launch Screen、AppIcon、Privacy Manifest

## 打开方式

1. 用 Xcode 打开 `AsakusaOmikuji.xcodeproj`
2. 选择你的 Team
3. 修改 Bundle Identifier
4. 选中真机或模拟器运行

## 资源同步

在网页层有更新时，重新执行：

```bash
python3 scripts/sync_ios_web_assets.py
python3 scripts/generate_app_icons.py
```

然后再回到 Xcode 运行或 Archive。
