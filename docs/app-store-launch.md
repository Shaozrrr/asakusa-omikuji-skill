# App Store 上架清单

这份项目现在已经补到了可以继续往 `TestFlight -> App Store Review` 推进的阶段，但还差几步苹果账号侧和 Xcode 侧的动作。

## 先说风险点

- 苹果审核的 `4.2 Minimum Functionality` 不鼓励“只是网站套壳”的 app。
- 苹果审核的 `4.3 Spam` 里明确提到过 `fortune telling` 这类容易同质化的品类。

所以这版 iOS 工程额外补了几件事，来降低它被当作纯套壳的概率：

- 本地打包签文和界面资源，不依赖外部网页才能运行
- 原生 `WKWebView` 壳，而不是浏览器壳
- 原生触感反馈
- 原生系统分享
- 原生启动页、AppIcon、隐私清单

## 你还需要准备什么

1. Apple Developer Program 账号
2. 一个正式的 Bundle ID
3. App Store Connect 里的 App 隐私问卷
4. iPhone 截图与可选的预览视频
5. 一轮 TestFlight 内测
6. 给审核团队的 Review Notes

## 建议的 App Store 定位

不要把它写成“算命工具”。

更安全的表述是：

- 一款以浅草观音灵签为灵感的东方签文化体验 app
- 强调仪式感、节奏、审美与签文阅读体验
- 强调留白与节制，而不是反复刷签

## 提审前必做

1. 在 Xcode 里把 `PRODUCT_BUNDLE_IDENTIFIER` 改成你自己的正式包名
2. 在 `Signing & Capabilities` 里选中你的团队
3. 真机跑一遍，确认 `WebAssets` 正常加载
4. 检查分享、重请、收起签纸、今日收束这些按钮都有效
5. 在 App Store Connect 里如实填写“未收集数据”或你的真实数据情况
6. 准备一句简短的 Review Notes，说明这是本地签文体验 app，而不是外链网页壳

## 推荐的 Review Notes 草稿

> This app provides a self-contained omikuji experience inspired by Asakusa temple lots.  
> All core content is bundled locally in the app, and the app includes native haptics, native sharing, and a custom iOS container instead of redirecting users to an external website.

## 上架顺序

1. 用 Xcode Archive 一次
2. 上传到 App Store Connect
3. 先发 TestFlight
4. 邀请 3-5 个用户试用
5. 根据反馈修正文案、截图和按钮细节
6. 再提交正式审核
