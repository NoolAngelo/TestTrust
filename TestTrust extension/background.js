chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

let examMode = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'START_EXAM') {
    examMode = true;
    // Initialize exam monitoring
    initializeExamMonitoring();
  } else if (request.type === 'STOP_EXAM') {
    examMode = false;
    // Clean up monitoring
    stopExamMonitoring();
  }
});

function initializeExamMonitoring() {
  // Implement your exam monitoring logic here
  console.log('Exam monitoring started');
}

function stopExamMonitoring() {
  // Clean up monitoring resources
  console.log('Exam monitoring stopped');
}
