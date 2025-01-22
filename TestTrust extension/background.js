chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

let examMode = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'START_EXAM') {
    examMode = true;
    initializeExamMonitoring();
  } else if (request.type === 'STOP_EXAM') {
    examMode = false;
    stopExamMonitoring();
  }
});

function initializeExamMonitoring() {
  console.log('Exam monitoring started');
}

function stopExamMonitoring() {
  console.log('Exam monitoring stopped');
}
