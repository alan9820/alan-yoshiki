/**
 * Millionaire Leaderboard API v4 (FINAL)
 * 
 * Sheet ID: 1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q
 * 
 * Now uses getActiveSheet() — works with any default tab name (Sheet1, etc)
 * Also auto-creates header row if sheet is empty.
 */

const SHEET_ID = '1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q';

function getSheet() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getActiveSheet();
  // If empty, add header row
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Name', 'Score', 'Timestamp']);
  }
  return sheet;
}

function doGet(e) {
  try {
    const sheet = getSheet();
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
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      count: leaderboard.length,
      leaderboard: leaderboard.slice(0, 100)
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false, error: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const name = (body.name || 'Anonymous').toString().substring(0, 50);
    const score = parseInt(body.score) || 0;
    const sheet = getSheet();
    sheet.appendRow([name, score, new Date().toISOString()]);
    return ContentService.createTextOutput(JSON.stringify({
      success: true, entry: { name, score }
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false, error: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
