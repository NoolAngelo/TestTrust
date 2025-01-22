document.addEventListener('DOMContentLoaded', function() {
  const loginView = document.getElementById('loginView');
  const loggedInView = document.getElementById('loggedInView');
  const loginForm = document.getElementById('loginForm');
  const errorMessage = document.getElementById('errorMessage');
  const userEmail = document.getElementById('userEmail');
  const startExam = document.getElementById('startExam');
  const stopExam = document.getElementById('stopExam');
  const logoutBtn = document.getElementById('logout');

  // Check if user is already logged in
  chrome.storage.local.get(['isLoggedIn', 'userEmail'], function(result) {
    if (result.isLoggedIn) {
      showLoggedInView(result.userEmail);
    }
  });

  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Here you would typically make an API call to your backend
    // This is a mock authentication
    if (email && password) {
      chrome.storage.local.set({
        isLoggedIn: true,
        userEmail: email
      }, function() {
        showLoggedInView(email);
      });
    } else {
      errorMessage.style.display = 'block';
    }
  });

  startExam.addEventListener('click', function() {
    chrome.runtime.sendMessage({type: 'START_EXAM'});
    startExam.style.display = 'none';
    stopExam.style.display = 'block';
  });

  stopExam.addEventListener('click', function() {
    chrome.runtime.sendMessage({type: 'STOP_EXAM'});
    startExam.style.display = 'block';
    stopExam.style.display = 'none';
  });

  logoutBtn.addEventListener('click', function() {
    chrome.storage.local.clear(function() {
      showLoginView();
    });
  });

  function showLoggedInView(email) {
    loginView.style.display = 'none';
    loggedInView.style.display = 'block';
    userEmail.textContent = email;
  }

  function showLoginView() {
    loginView.style.display = 'block';
    loggedInView.style.display = 'none';
    loginForm.reset();
  }
});
