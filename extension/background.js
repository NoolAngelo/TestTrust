chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

let examMode = false;
let warningCount = 0;
let examLogs = [];
let keyboardEvents = [];
let mouseEvents = [];

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'START_EXAM') {
    examMode = true;
    initializeExamMonitoring();
    startBasicMonitoring();
  } else if (request.type === 'STOP_EXAM') {
    examMode = false;
    stopExamMonitoring();
    stopBasicMonitoring();
  }
});

function initializeExamMonitoring() {
  try {
    // Add WebRTC screen capture detection
    detectScreenCapture();
    // Add virtual machine detection
    detectVirtualEnvironment();
    // Add network monitoring
    monitorNetworkRequests();
    // Add clipboard monitoring
    monitorClipboard();
    
    // Monitor tab switching
    chrome.tabs.onActivated.addListener(logTabSwitch);
    
    // Monitor keyboard events
    document.addEventListener('keydown', logKeyboardEvent);
    
    // Monitor mouse events
    document.addEventListener('mousedown', logMouseEvent);
    
    // Start screen monitoring
    startScreenMonitoring();
  } catch (error) {
    console.error("Error initializing exam monitoring:", error);
  }
}

function detectScreenCapture() {
  navigator.mediaDevices.getDisplayMedia().then(stream => {
    // Handle screen sharing detection
  }).catch(error => {
    console.error("Error detecting screen capture:", error);
  });
}

function stopExamMonitoring() {
  console.log('Exam monitoring stopped');
}

function startBasicMonitoring() {
  // Request camera access for basic face detection
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      // Basic attention monitoring
      setInterval(() => {
        if (!document.hasFocus()) {
          warningCount++;
          if (warningCount >= 3) {
            alert("Please focus on your exam!");
          }
        }
      }, 5000);
    })
    .catch(err => {
      console.error("Camera access denied:", err);
    });
}

function stopBasicMonitoring() {
  warningCount = 0;
  // Stop monitoring
}

function logTabSwitch(activeInfo) {
  examLogs.push({
    type: 'tab_switch',
    timestamp: new Date(),
    tabId: activeInfo.tabId
  });
}

function logKeyboardEvent(event) {
  if (event.altKey || event.ctrlKey) {
    keyboardEvents.push({
      type: 'keyboard',
      key: event.key,
      timestamp: new Date()
    });
  }
}

function logMouseEvent(event) {
  mouseEvents.push({
    type: 'mouse',
    x: event.clientX,
    y: event.clientY,
    timestamp: new Date()
  });
}

function monitorNetworkRequests() {
  try {
    // Implement network request monitoring
  } catch (error) {
    console.error("Error monitoring network requests:", error);
  }
}

function monitorClipboard() {
  try {
    // Implement clipboard monitoring
  } catch (error) {
    console.error("Error monitoring clipboard:", error);
  }
}

function secureStore(key, value) {
  try {
    const encrypted = encryptSensitiveData(value);
    chrome.storage.local.set({[key]: encrypted}, function() {
      if (chrome.runtime.lastError) {
        console.error("Error storing data:", chrome.runtime.lastError);
      }
    });
  } catch (error) {
    console.error("Encryption error:", error);
  }
}

function generateReport(examId) {
  return {
    examId,
    logs: examLogs,
    keyboard: keyboardEvents,
    mouse: mouseEvents,
    suspicious: detectSuspiciousActivity()
  };
}
