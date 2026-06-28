/**
 * Millionaire Leaderboard API v3 (READY TO DEPLOY)
 * 
 * Sheet ID: 1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q
 * URL: https://docs.google.com/spreadsheets/d/1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q/edit
 */

const SHEET_ID = '1H_jThO7TxA5IY8hvv82udsHW828JWc51dXl2vZD5n_Q';
const SHEET_NAME = 'Leaderboard';

function doGet(e) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
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
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
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
