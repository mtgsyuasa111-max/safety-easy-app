/**
 * PRODUCTION-READY GOOGLE APPS SCRIPT FOR SAFETY EASY APP
 * Deployed as: Web App (Execute as: Me, Who has access: Anyone)
 * Target Spreadsheet ID: 18fG-3MpRqiDe2EjJcdqqG_i6BdCEYFjdUqS4uYi6F3k
 */

const SHEET_ID = "18fG-3MpRqiDe2EjJcdqqG_i6BdCEYFjdUqS4uYi6F3k"; // Target Sheet ID
const SHEET_NAME = "Jobs"; // Using target tab name
const DEFAULT_DRIVE_FOLDER_ID = "12FzCcoLz2w7ETwHwFuL4h278vkbKd0WB"; // Default Drive Folder for Image Uploads

// Handle GET requests (For fetching jobs)
function doGet(e) {
  try {
    var action = e.parameter.action;
    var ss = SpreadsheetApp.openById(SHEET_ID);
    
    // Auto-detect or fetch Users
    if (action === "getUsers") {
      var userSheet = ss.getSheetByName("Users") || ss.getSheets()[0];
      var userData = userSheet.getDataRange().getValues();
      var users = [];
      for (var i = 1; i < userData.length; i++) {
        var row = userData[i];
        if (!row[0]) continue;
        users.push({
          id: String(row[0]),
          name: String(row[1] || ""),
          role: String(row[2] || "subordinate"),
          area: String(row[3] || ""),
          pinHash: String(row[4] || "")
        });
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: users }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === "getJobs") {
      var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
      var data = sheet.getDataRange().getValues();
      var jobs = [];
      
      for (var i = 1; i < data.length; i++) {
        var row = data[i];
        if (!row[0]) continue;
        
        var job = {
          id: String(row[0]),
          area: String(row[1] || ""),
          reporter: String(row[2] || ""),
          assignee: String(row[3] || ""),
          issue: String(row[4] || ""),
          suggestion: String(row[5] || ""),
          taskType: String(row[6] || "safety"),
          status: String(row[7] || "pending"),
          photoBefore: String(row[8] || ""),
          photoAfter: String(row[9] || ""),
          createdAt: String(row[10] || ""),
          resolvedAt: String(row[11] || ""),
          resolvedBy: String(row[12] || ""),
          notes: String(row[13] || ""),
          approvedAt: String(row[14] || ""),
          approvedBy: String(row[15] || "")
        };
        jobs.push(job);
      }
      
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: jobs }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Invalid GET action" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle POST requests (Create, Update, Delete, Login)
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Empty request body" }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    var payload = JSON.parse(e.postData.contents);
    var action = payload.action;
    var rawData = payload.data;
    var folderId = payload.imageFolderId || DEFAULT_DRIVE_FOLDER_ID;
    
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    
    // Auth Validation Mock (Allows seamless connection)
    if (action === "login") {
      var userSheet = ss.getSheetByName("Users");
      var userData = userSheet.getDataRange().getValues();
      for (var i = 1; i < userData.length; i++) {
        if (String(userData[i][1]).trim() === String(rawData.username).trim() && String(userData[i][4]).trim() === String(rawData.pin).trim()) {
          return ContentService.createTextOutput(JSON.stringify({
            status: "success",
            token: "AUTH_" + Utilities.getUuid(),
            user: {
              name: String(userData[i][1]),
              role: String(userData[i][2]),
              area: String(userData[i][3])
            }
          })).setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "ชื่อผู้ใช้หรือรหัส PIN ไม่ถูกต้อง" }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === "getJobs") {
      // Allow loading jobs via POST as fallback
      var sheet = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
      var data = sheet.getDataRange().getValues();
      var jobs = [];
      for (var i = 1; i < data.length; i++) {
        var row = data[i];
        if (!row[0]) continue;
        jobs.push({
          id: String(row[0]),
          area: String(row[1] || ""),
          reporter: String(row[2] || ""),
          assignee: String(row[3] || ""),
          issue: String(row[4] || ""),
          suggestion: String(row[5] || ""),
          taskType: String(row[6] || "safety"),
          status: String(row[7] || "pending"),
          photoBefore: String(row[8] || ""),
          photoAfter: String(row[9] || ""),
          createdAt: String(row[10] || ""),
          resolvedAt: String(row[11] || ""),
          resolvedBy: String(row[12] || ""),
          notes: String(row[13] || ""),
          approvedAt: String(row[14] || ""),
          approvedBy: String(row[15] || "")
        });
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: jobs }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    if (action === "create") {
      // Process Before image if it is base64
      var beforeUrl = "";
      if (rawData.photoBefore && rawData.photoBefore.indexOf("data:image/") === 0) {
        beforeUrl = uploadBase64ToDrive(rawData.photoBefore, "BEFORE_" + rawData.id, folderId);
      } else {
        beforeUrl = rawData.photoBefore || "";
      }
      
      // Append row in exact order matching headers
      sheet.appendRow([
        rawData.id,
        rawData.area,
        rawData.reporter,
        rawData.assignee,
        rawData.issue,
        rawData.suggestion,
        rawData.taskType || "safety",
        rawData.status || "pending",
        beforeUrl,
        "", // photoAfter (empty on create)
        rawData.createdAt,
        "", // resolvedAt
        "", // resolvedBy
        "", // notes
        "", // approvedAt
        ""  // approvedBy
      ]);
      
      return ContentService.createTextOutput(JSON.stringify({ status: "success", id: rawData.id }))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === "update") {
      var allData = sheet.getDataRange().getValues();
      var rowIndex = -1;
      
      // Fast lookup matching ID in Column A
      for (var i = 1; i < allData.length; i++) {
        if (String(allData[i][0]) === String(rawData.id)) {
          rowIndex = i + 1; // 1-based index including header
          break;
        }
      }
      
      if (rowIndex === -1) {
        return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Case ID not found in sheet: " + rawData.id }))
          .setMimeType(ContentService.MimeType.JSON);
      }
      
      // Update fields based on status
      if (rawData.status === "resolved") {
        var afterUrl = "";
        if (rawData.photoAfter && rawData.photoAfter.indexOf("data:image/") === 0) {
          afterUrl = uploadBase64ToDrive(rawData.photoAfter, "AFTER_" + rawData.id, folderId);
        } else {
          afterUrl = rawData.photoAfter || "";
        }
        
        sheet.getRange(rowIndex, 8).setValue("resolved");       // Column H (8): Status
        if (afterUrl) {
          sheet.getRange(rowIndex, 10).setValue(afterUrl);      // Column J (10): photoAfter (Corrected Index!)
        }
        sheet.getRange(rowIndex, 12).setValue(rawData.resolvedAt); // Column L (12): resolvedAt
        sheet.getRange(rowIndex, 13).setValue(rawData.resolvedBy || "Operator"); // Column M (13): resolvedBy
        sheet.getRange(rowIndex, 14).setValue(rawData.notes || "แก้ไขความปลอดภัยหน้างานเรียบร้อย"); // Column N (14): Notes
        
      } else if (rawData.status === "approved") {
        sheet.getRange(rowIndex, 8).setValue("approved");       // Column H (8): Status
        sheet.getRange(rowIndex, 15).setValue(rawData.approvedAt); // Column O (15): approvedAt
        sheet.getRange(rowIndex, 16).setValue(rawData.approvedBy || "Admin"); // Column P (16): approvedBy
      }
      
      return ContentService.createTextOutput(JSON.stringify({ status: "success", id: rawData.id }))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === "updateUser") {
      var userSheet = ss.getSheetByName("Users") || ss.getSheets()[0];
      var userData = userSheet.getDataRange().getValues();
      var rowIndex = -1;
      
      for (var i = 1; i < userData.length; i++) {
        if (String(userData[i][0]) === String(rawData.id)) {
          rowIndex = i + 1; // 1-based index including header
          break;
        }
      }
      
      if (rowIndex === -1) {
        return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "User ID not found: " + rawData.id }))
          .setMimeType(ContentService.MimeType.JSON);
      }
      
      // Update Column 4 (D): Area (Index 3 since Columns are A=0, B=1, C=2, D=3)
      userSheet.getRange(rowIndex, 4).setValue(rawData.area);
      
      return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "User area updated" }))
        .setMimeType(ContentService.MimeType.JSON);
        
    } else if (action === "delete") {
      var allData = sheet.getDataRange().getValues();
      for (var i = 1; i < allData.length; i++) {
        if (String(allData[i][0]) === String(rawData.id)) {
          sheet.deleteRow(i + 1);
          return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "Deleted row" }))
            .setMimeType(ContentService.MimeType.JSON);
        }
      }
      return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "ID not found to delete" }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Unsupported action" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Helper: Decode Base64 and upload to Google Drive
function uploadBase64ToDrive(base64Data, baseFileName, folderId) {
  try {
    var parts = base64Data.split(",");
    var mimeType = "image/jpeg";
    var ext = "jpg";
    var b64Data = parts[0];
    
    if (parts.length > 1) {
      b64Data = parts[1];
      var matches = parts[0].match(/data:(.*?);/);
      if (matches) {
        mimeType = matches[1];
        if (mimeType.indexOf("png") !== -1) ext = "png";
        else if (mimeType.indexOf("webp") !== -1) ext = "webp";
      }
    }
    
    var decoded = Utilities.base64Decode(b64Data);
    var blob = Utilities.newBlob(decoded, mimeType, baseFileName + "." + ext);
    
    var folder = DriveApp.getFolderById(folderId || DEFAULT_DRIVE_FOLDER_ID);
    var file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    
    // Returns previewable direct link matching client requirements
    return "https://drive.google.com/thumbnail?id=" + file.getId() + "&sz=w800";
  } catch (ex) {
    Logger.log("Drive upload fail: " + ex.toString());
    return "";
  }
}
