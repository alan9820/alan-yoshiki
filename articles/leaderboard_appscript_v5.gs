/**
 * Millionaire Leaderboard + Activity Monitor API v5 (FINAL)
 *
 * Combined: leaderboard (POST/GET) + activity events (POST only)
 * Replaces previous leaderboard endpoint + webhook.site activity monitor.
 *
 * Sheet ID: 1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q
 * Tabs: 'Leaderboard' (auto-create) + 'Activity' (auto-create)
 *
 * Rate-limit: 同一 name 5 min 內只准 POST 一次 leaderboard entry.
 *            同一 IP (best-effort) 1 min 內只准 POST 5 次 leaderboard.
 *
 * NOTE: Apps Script can't reliably enforce IP rate-limits (no client IP),
 *       so we use name+timestamp guard + simple global throttle via CacheService.
 */

const SHEET_ID = '1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q';
const SHEET_TAB = 'Leaderboard';
const ACTIVITY_TAB = 'Activity';
const LEADERBOARD_CACHE_KEY = 'lb_recent';
const ACTIVITY_CACHE_KEY = 'act_recent';

// ============================================
// Helpers
// ============================================
function getSheet_(tabName) {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(tabName);
  if (!sheet) {
    sheet = ss.insertSheet(tabName);
  }
  if (sheet.getLastRow() === 0) {
    if (tabName === SHEET_TAB) {
      sheet.appendRow(['Name', 'Score', 'Timestamp']);
    } else if (tabName === ACTIVITY_TAB) {
      sheet.appendRow(['Action', 'Player', 'Level', 'Money', 'Category', 'Correct', 'Reason', 'Timestamp']);
    }
  }
  return sheet;
}

function rateLimited_(key, windowSec, maxCount) {
  const cache = CacheService.getScriptCache();
  const raw = cache.get(key);
  const now = Date.now();
  let arr = [];
  if (raw) {
    try { arr = JSON.parse(raw).filter(t => now - t < windowSec * 1000); } catch (e) {}
  }
  if (arr.length >= maxCount) return true;
  arr.push(now);
  cache.put(key, JSON.stringify(arr), windowSec);
  return false;
}

function ok_(data) {
  return ContentService.createTextOutput(JSON.stringify(Object.assign({ success: true }, data)))
    .setMimeType(ContentService.MimeType.JSON);
}
function err_(msg) {
  return ContentService.createTextOutput(JSON.stringify({ success: false, error: msg }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================================
// Leaderboard API
// ============================================
function doGet(e) {
  try {
    const sheet = getSheet_(SHEET_TAB);
    const data = sheet.getDataRange().getValues();
    const leaderboard = [];
    for (let i = 1; i < data.length; i++) {
      leaderboard.push({
        name: data[i][0],
        score: parseInt(data[i][1]) || 0,
        ts: data[i][2] || new Date().toISOString()
      });
    }
    leaderboard.sort((a, b) => b.score - a.score);
    return ok_({ count: leaderboard.length, leaderboard: leaderboard.slice(0, 100) });
  } catch (e) { return err_(e.message); }
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents || '{}');
    const type = body.type || 'leaderboard';

    if (type === 'activity') {
      return handleActivity_(body);
    } else {
      return handleLeaderboard_(body);
    }
  } catch (e) { return err_('bad_request: ' + e.message); }
}

function handleLeaderboard_(body) {
  const name = (body.name || 'Anonymous').toString().substring(0, 50).trim();
  if (!name) return err_('name required');
  const score = parseInt(body.score) || 0;
  if (score < 0 || score > 1000000) return err_('invalid score');

  // Rate-limit: 同一 name 5 min 內只准 POST 一次
  const nameKey = 'lb_name_' + name.toLowerCase();
  if (rateLimited_(nameKey, 300, 1)) {
    return err_('rate_limited: same name within 5min');
  }

  // Global throttle: 1 min 內 30 個 POST (防止大 spam)
  if (rateLimited_(LEADERBOARD_CACHE_KEY, 60, 30)) {
    return err_('rate_limited: too many requests');
  }

  const sheet = getSheet_(SHEET_TAB);
  sheet.appendRow([name, score, new Date().toISOString()]);
  return ok_({ entry: { name, score } });
}

function handleActivity_(body) {
  // 收 activity event, 寫入 Activity tab (replaces webhook.site)
  // 唔做 rate-limit 因為 page unload 都會發 → 默許 noisy
  const sheet = getSheet_(ACTIVITY_TAB);
  sheet.appendRow([
    (body.action || '').toString().substring(0, 32),
    (body.player_name || '').toString().substring(0, 32),
    body.level || '',
    body.level_money || body.final_money || '',
    (body.category || '').toString().substring(0, 16),
    body.correct || '',
    (body.reason || '').toString().substring(0, 32),
    body.ts || new Date().toISOString()
  ]);
  return ok_({ logged: true });
}