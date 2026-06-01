/**
 * Safety Easy backend.
 * Deploy as a Web App: execute as owner, access allowed to anyone with the URL.
 * Authorization is enforced by the application session token below.
 */
const SHEET_ID = "18fG-3MpRqiDe2EjJcdqqG_i6BdCEYFjdUqS4uYi6F3k";
const SHEET_NAME = "Jobs";
const USERS_SHEET_NAME = "Users";
const DEFAULT_DRIVE_FOLDER_ID = "12FzCcoLz2w7ETwHwFuL4h278vkbKd0WB";
const SESSION_TTL_SECONDS = 21600;

function doGet(e) {
  try {
    var action = String((e && e.parameter && e.parameter.action) || "");
    var token = String((e && e.parameter && e.parameter.token) || "");
    var ss = SpreadsheetApp.openById(SHEET_ID);

    if (action === "getUsers") {
      return jsonSuccess({ data: getPublicUsers(ss) });
    }

    if (action === "getJobs") {
      requireSession(token);
      return jsonOutput(readJobs(ss));
    }

    return jsonError("Invalid GET action");
  } catch (error) {
    return jsonError(error.message || String(error));
  }
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonError("Empty request body");
    }

    var payload = JSON.parse(e.postData.contents);
    var action = String(payload.action || "");
    var rawData = payload.data || {};
    var ss = SpreadsheetApp.openById(SHEET_ID);

    if (action === "login") {
      return login(ss, rawData);
    }

    if (action === "getUsers") {
      return jsonSuccess({ data: getPublicUsers(ss) });
    }

    if (action === "verifySession") {
      var verifiedUser = requireSession(payload.token);
      return jsonSuccess({ user: verifiedUser });
    }

    var currentUser = requireSession(payload.token);
    var sheet = getJobsSheet(ss);

    if (action === "getJobs") {
      return jsonSuccess({ data: readJobs(ss) });
    }

    if (action === "create") {
      requireRole(currentUser, ["admin", "supervisor"]);
      return createJob(sheet, rawData);
    }

    if (action === "update") {
      return updateJob(sheet, rawData, currentUser);
    }

    if (action === "updateUser") {
      requireRole(currentUser, ["admin"]);
      return updateUser(ss, rawData);
    }

    if (action === "createUser") {
      requireRole(currentUser, ["admin"]);
      return createUser(ss, rawData);
    }

    if (action === "deleteUser") {
      requireRole(currentUser, ["admin"]);
      return deleteUser(ss, rawData);
    }

    if (action === "delete") {
      requireRole(currentUser, ["admin", "supervisor"]);
      return deleteJob(sheet, rawData);
    }

    return jsonError("Unsupported action");
  } catch (error) {
    return jsonError(error.message || String(error));
  }
}

function login(ss, rawData) {
  var userSheet = getUsersSheet(ss);
  var userData = userSheet.getDataRange().getValues();
  var enteredId = String(rawData.id || "").trim();
  var enteredPin = String(rawData.pin || "").trim();
  var enteredPinHash = hashPin(enteredPin);

  for (var i = 1; i < userData.length; i++) {
    var storedId = String(userData[i][0] || "").trim();
    var storedPin = String(userData[i][4] || "").trim();
    if (storedId !== enteredId) continue;
    if (userData[i][5] === false) break;

    var isLegacyPlainPin = storedPin.length > 0 && storedPin.length <= 8;
    var matched = isLegacyPlainPin ? storedPin === enteredPin : storedPin === enteredPinHash;
    if (!matched) break;

    // Transparently migrate legacy plain-text PINs on successful login.
    if (isLegacyPlainPin) {
      userSheet.getRange(i + 1, 5).setValue(enteredPinHash);
    }

    var user = {
      id: storedId,
      name: String(userData[i][1] || ""),
      role: String(userData[i][2] || "subordinate"),
      area: String(userData[i][3] || "")
    };
    var token = "AUTH_" + Utilities.getUuid();
    CacheService.getScriptCache().put(sessionKey(token), JSON.stringify(user), SESSION_TTL_SECONDS);
    return jsonSuccess({ token: token, user: user });
  }

  return jsonError("ชื่อผู้ใช้หรือรหัส PIN ไม่ถูกต้อง");
}

function requireSession(token) {
  var cleanToken = String(token || "").trim();
  if (!cleanToken) throw new Error("กรุณาเข้าสู่ระบบใหม่");

  var cache = CacheService.getScriptCache();
  var value = cache.get(sessionKey(cleanToken));
  if (!value) throw new Error("เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่");

  // Sliding expiry while the user is active.
  cache.put(sessionKey(cleanToken), value, SESSION_TTL_SECONDS);
  return JSON.parse(value);
}

function requireRole(user, allowedRoles) {
  if (!user || allowedRoles.indexOf(user.role) === -1) {
    throw new Error("คุณไม่มีสิทธิ์ดำเนินการนี้");
  }
}

function sessionKey(token) {
  return "SESSION_" + token;
}

function hashPin(pin) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(pin || ""))
    .map(function(b) {
      var hex = (b < 0 ? b + 256 : b).toString(16);
      return hex.length < 2 ? "0" + hex : hex;
    })
    .join("");
}

function getPublicUsers(ss) {
  var data = getUsersSheet(ss).getDataRange().getValues();
  var users = [];
  for (var i = 1; i < data.length; i++) {
    if (!data[i][0] || data[i][5] === false) continue;
    users.push({
      id: String(data[i][0]),
      name: cleanText(data[i][1]),
      role: String(data[i][2] || "subordinate"),
      area: cleanText(data[i][3])
    });
  }
  return users;
}

function readJobs(ss) {
  var data = getJobsSheet(ss).getDataRange().getValues();
  var jobs = [];
  for (var i = 1; i < data.length; i++) {
    if (!data[i][0]) continue;
    jobs.push(rowToJob(data[i]));
  }
  return jobs;
}

function rowToJob(row) {
  return {
    id: String(row[0] || ""),
    area: cleanText(row[1]),
    reporter: cleanText(row[2]),
    assignee: cleanText(row[3]),
    issue: cleanText(row[4]),
    suggestion: cleanText(row[5]),
    taskType: String(row[6] || "safety"),
    status: String(row[7] || "pending"),
    photoBefore: String(row[8] || ""),
    photoAfter: String(row[9] || ""),
    createdAt: String(row[10] || ""),
    resolvedAt: String(row[11] || ""),
    resolvedBy: cleanText(row[12]),
    notes: cleanText(row[13]),
    approvedAt: String(row[14] || ""),
    approvedBy: cleanText(row[15])
  };
}

function createJob(sheet, rawData) {
  requireFields(rawData, ["id", "area", "reporter", "assignee", "issue", "suggestion", "createdAt"]);
  var existingRow = findRowById(sheet, rawData.id);
  if (existingRow !== -1) {
    return jsonSuccess({ id: rawData.id, alreadyExists: true });
  }

  var beforeUrl = persistPhoto(rawData.photoBefore, "BEFORE_" + rawData.id);
  sheet.appendRow([
    rawData.id,
    cleanText(rawData.area),
    cleanText(rawData.reporter),
    cleanText(rawData.assignee),
    cleanText(rawData.issue),
    cleanText(rawData.suggestion),
    rawData.taskType || "safety",
    rawData.status || "pending",
    beforeUrl,
    "",
    rawData.createdAt,
    "",
    "",
    "",
    "",
    ""
  ]);
  return jsonSuccess({ id: rawData.id, photoBeforeUrl: beforeUrl });
}

function updateJob(sheet, rawData, currentUser) {
  requireFields(rawData, ["id"]);
  var rowIndex = findRowById(sheet, rawData.id);
  if (rowIndex === -1) throw new Error("Case ID not found in sheet: " + rawData.id);

  if (rawData.taskType !== undefined) {
    requireRole(currentUser, ["admin"]);
    var taskType = String(rawData.taskType);
    if (taskType !== "safety" && taskType !== "5s") throw new Error("Invalid taskType");
    sheet.getRange(rowIndex, 7).setValue(taskType);
  }

  if (rawData.area !== undefined || rawData.assignee !== undefined) {
    requireRole(currentUser, ["admin", "supervisor"]);
    if (rawData.area !== undefined) sheet.getRange(rowIndex, 2).setValue(cleanText(rawData.area));
    if (rawData.assignee !== undefined) sheet.getRange(rowIndex, 4).setValue(cleanText(rawData.assignee));
  }

  var response = { id: rawData.id };
  if (rawData.status === "resolved") {
    requireRole(currentUser, ["admin", "supervisor", "subordinate"]);
    var assignedTo = String(sheet.getRange(rowIndex, 4).getValue() || "");
    var currentTaskType = String(sheet.getRange(rowIndex, 7).getValue() || "safety");
    if (currentUser.role === "subordinate" && currentTaskType !== "safety" && normalizeName(assignedTo) !== normalizeName(currentUser.name)) {
      throw new Error("คุณส่งผลการแก้ไขได้เฉพาะงานที่มอบหมายให้คุณ");
    }
    var afterUrl = persistPhoto(rawData.photoAfter, "AFTER_" + rawData.id);
    sheet.getRange(rowIndex, 8).setValue("resolved");
    sheet.getRange(rowIndex, 10).setValue(afterUrl);
    sheet.getRange(rowIndex, 12).setValue(rawData.resolvedAt || "");
    sheet.getRange(rowIndex, 13).setValue(rawData.resolvedBy || currentUser.name);
    sheet.getRange(rowIndex, 14).setValue(cleanText(rawData.notes || "แก้ไขความปลอดภัยหน้างานเรียบร้อย"));
    response.photoAfterUrl = afterUrl;
  } else if (rawData.status === "approved") {
    requireRole(currentUser, ["admin", "supervisor", "subordinate"]);
    var assignedToApprove = String(sheet.getRange(rowIndex, 4).getValue() || "");
    if (currentUser.role === "subordinate" && normalizeName(assignedToApprove) !== normalizeName(currentUser.name)) {
      throw new Error("คุณปิดงานได้เฉพาะงานที่มอบหมายให้คุณ");
    }
    sheet.getRange(rowIndex, 8).setValue("approved");
    sheet.getRange(rowIndex, 15).setValue(rawData.approvedAt || "");
    sheet.getRange(rowIndex, 16).setValue(rawData.approvedBy || currentUser.name);
  } else if (rawData.status === "rejected") {
    requireRole(currentUser, ["admin", "supervisor"]);
    var reason = String(rawData.rejectionReason || "").trim();
    if (!reason) throw new Error("กรุณาระบุเหตุผลที่ตีกลับงาน");
    sheet.getRange(rowIndex, 8).setValue("pending");
    sheet.getRange(rowIndex, 10).setValue("");
    sheet.getRange(rowIndex, 12).setValue("");
    sheet.getRange(rowIndex, 13).setValue("");
    sheet.getRange(rowIndex, 14).setValue("ตีกลับ: " + cleanText(reason));
    sheet.getRange(rowIndex, 15).setValue("");
    sheet.getRange(rowIndex, 16).setValue("");
  }
  return jsonSuccess(response);
}

function updateUser(ss, rawData) {
  requireFields(rawData, ["id"]);
  var sheet = getUsersSheet(ss);
  var rowIndex = findRowById(sheet, rawData.id);
  if (rowIndex === -1) throw new Error("User ID not found: " + rawData.id);

  if (rawData.area !== undefined) sheet.getRange(rowIndex, 4).setValue(cleanText(rawData.area));
  if (rawData.pin !== undefined) sheet.getRange(rowIndex, 5).setValue(hashPin(rawData.pin));
  return jsonSuccess({ message: "User updated successfully" });
}

function createUser(ss, rawData) {
  requireFields(rawData, ["id", "name", "role", "area", "pin"]);
  var sheet = getUsersSheet(ss);
  if (findRowById(sheet, rawData.id) !== -1) throw new Error("User ID already exists: " + rawData.id);
  sheet.appendRow([rawData.id, cleanText(rawData.name), rawData.role, cleanText(rawData.area), hashPin(rawData.pin), true]);
  return jsonSuccess({ id: rawData.id });
}

function deleteUser(ss, rawData) {
  requireFields(rawData, ["id"]);
  var sheet = getUsersSheet(ss);
  var rowIndex = findRowById(sheet, rawData.id);
  if (rowIndex === -1) throw new Error("User ID not found: " + rawData.id);
  sheet.deleteRow(rowIndex);
  return jsonSuccess({ message: "User deleted successfully" });
}

function deleteJob(sheet, rawData) {
  requireFields(rawData, ["id"]);
  var rowIndex = findRowById(sheet, rawData.id);
  if (rowIndex === -1) throw new Error("ID not found to delete");
  sheet.deleteRow(rowIndex);
  return jsonSuccess({ message: "Deleted row" });
}

function persistPhoto(photoValue, baseFileName) {
  var value = String(photoValue || "").trim();
  if (!value) throw new Error("กรุณาแนบรูปภาพ");
  if (value.indexOf("data:image/") === 0) return uploadBase64ToDrive(value, baseFileName);
  if (/^https:\/\/drive\.google\.com\//i.test(value)) return value;
  throw new Error("รูปภาพต้องอัปโหลดจากกล้องหรือเป็น URL จาก Google Drive");
}

function uploadBase64ToDrive(base64Data, baseFileName) {
  var parts = String(base64Data || "").split(",");
  if (parts.length !== 2) throw new Error("รูปภาพ Base64 ไม่ถูกต้อง");

  var mimeMatch = parts[0].match(/^data:(image\/(?:jpeg|png|webp));base64$/i);
  if (!mimeMatch) throw new Error("รองรับเฉพาะรูป JPG, PNG หรือ WEBP");

  var mimeType = mimeMatch[1].toLowerCase();
  var ext = mimeType.indexOf("png") !== -1 ? "png" : mimeType.indexOf("webp") !== -1 ? "webp" : "jpg";
  var decoded = Utilities.base64Decode(parts[1]);
  var blob = Utilities.newBlob(decoded, mimeType, baseFileName + "." + ext);
  var file = DriveApp.getFolderById(DEFAULT_DRIVE_FOLDER_ID).createFile(blob);
  try {
    // Folder permissions are inherited by the new file. Avoid the slow
    // per-file sharing update so the client receives its response promptly.
  } catch (error) {
    // Keep the Drive upload when Workspace policy blocks explicit public sharing.
    Logger.log("Drive public sharing skipped: " + error.message);
    return "https://drive.google.com/thumbnail?id=" + file.getId() + "&sz=w1200";
    file.setTrashed(true);
    throw new Error("อัปโหลดรูปได้แต่เปิดสิทธิ์ให้เครื่องอื่นดูไม่ได้: " + error.message);
  }
  return "https://drive.google.com/thumbnail?id=" + file.getId() + "&sz=w1200";
}

function findRowById(sheet, id) {
  var values = sheet.getDataRange().getValues();
  for (var i = 1; i < values.length; i++) {
    if (String(values[i][0]) === String(id)) return i + 1;
  }
  return -1;
}

function requireFields(data, fields) {
  fields.forEach(function(field) {
    if (data[field] === undefined || data[field] === null || String(data[field]).trim() === "") {
      throw new Error("Missing required field: " + field);
    }
  });
}

function cleanText(value) {
  return String(value || "")
    .replace(/[<>&"'`]/g, "")
    .trim();
}

function normalizeName(name) {
  if (!name) return "";
  return String(name)
    .replace(/\s+/g, "")
    .replace(/[ศ์ค์]/g, "")
    .trim();
}

function getJobsSheet(ss) {
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) throw new Error("Jobs sheet not found");
  return sheet;
}

function getUsersSheet(ss) {
  var sheet = ss.getSheetByName(USERS_SHEET_NAME);
  if (!sheet) throw new Error("Users sheet not found");
  return sheet;
}

function jsonSuccess(extra) {
  var result = { status: "success" };
  Object.keys(extra || {}).forEach(function(key) { result[key] = extra[key]; });
  return jsonOutput(result);
}

function jsonError(message) {
  return jsonOutput({ status: "error", message: String(message || "Unknown error") });
}

function jsonOutput(value) {
  return ContentService.createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}
