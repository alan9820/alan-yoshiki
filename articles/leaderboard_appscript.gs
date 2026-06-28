/**
 * Millionaire Leaderboard API
 * - GET: returns top 100 leaderboard
 * - POST: adds new entry {name, score}
 */

const SHEET_NAME = 'Leaderboard';

function doGet(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME) 
                  || SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
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
      success: false,
      error: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const name = (body.name || 'Anonymous').toString().substring(0, 50);
    const score = parseInt(body.score) || 0;
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME)
                  || SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.appendRow([name, score, new Date().toISOString()]);
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      entry: { name, score }
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: err.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
