# 🔍 Google Search Console 設定指南

## 方法 1：Google Analytics 自動驗證（最簡單，推薦）✅

你已經有 Google Analytics (G-32X6WDJM63)，呢個方法最簡單：

1. 去 https://search.google.com/search-console/
2. 用 `alan.yoshiki@gmail.com` 登入
3. 喺 "URL prefix" 輸入：`https://alan9820.github.io/alan-yoshiki/`
4. 揀 **"Google Analytics"** 驗證方法
5. 撳 "Verify" — 由於 GA 已經喺度，**5 秒內完成** ✅

## 方法 2：HTML file upload

1. 去 https://search.google.com/search-console/
2. 揀 "URL prefix" → `https://alan9820.github.io/alan-yoshiki/`
3. 揀 **"HTML file"** 驗證方法
4. Google 會畀你一個 `google[hash].html` file
5. **將 file 放入 `workspace/alan-yoshiki/` 根目錄**（即係呢個 file 旁邊）
6. 推送：
   ```bash
   cd /home/alan9820/.openclaw/workspace/alan-yoshiki
   git add google[hash].html
   git commit -m "Add Google Search Console verification"
   git push
   ```
7. 等 1-2 分鐘 GitHub Pages deploy 完成
8. 返去 Search Console 撳 "Verify"

## 方法 3：HTML meta tag（已準備好）

我已經喺 index.html 加入 template，**你只需要將 Google 畀你嘅 content 替換**：

```html
<meta name="google-site-verification" content="YOUR_VERIFICATION_CODE_HERE" />
```

Google 註冊時會提供 code，你 paste 入去就得。

---

## ✅ 註冊完之後提交 Sitemap

無論用邊個方法，註冊完之後：

1. 喺 Search Console 左 menu 揀 **"Sitemaps"**
2. 輸入：`sitemap.xml`
3. 撳 "Submit"
4. 等 Google 處理（24-48 小時開始 indexing）

**你嘅 sitemap 已經 live:** https://alan9820.github.io/alan-yoshiki/sitemap.xml

---

## 📊 之後可以做嘅優化

註冊完 Search Console 之後：
- 監控 indexing status
- 睇 search queries
- 搵出 broken links / mobile issues
- Request indexing for 新文章

