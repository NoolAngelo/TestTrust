document.addEventListener('DOMContentLoaded', function() {
  const roleSelectionView = document.getElementById('roleSelectionView');
  const loginView = document.getElementById('loginView');
  const loggedInView = document.getElementById('loggedInView');
  const loginForm = document.getElementById('loginForm');
  const errorMessage = document.getElementById('errorMessage');
  const userEmail = document.getElementById('userEmail');
  const startExam = document.getElementById('startExam');
  const stopExam = document.getElementById('stopExam');
  const logoutBtn = document.getElementById('logout');
  const studentBtn = document.getElementById('studentBtn');
  const teacherBtn = document.getElementById('teacherBtn');

  chrome.storage.local.get(['isLoggedIn', 'userEmail'], function(result) {
    if (result.isLoggedIn) {
      showLoggedInView(result.userEmail);
    }
  });

  studentBtn.addEventListener('click', function() {
    showLoginView('student');
  });

  teacherBtn.addEventListener('click', function() {
    showLoginView('teacher');
  });

  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

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
      showRoleSelectionView();
    });
  });

  function showLoggedInView(email) {
    roleSelectionView.style.display = 'none';
    loginView.style.display = 'none';
    loggedInView.style.display = 'block';
    userEmail.textContent = email;
  }

  function showLoginView(role) {
    roleSelectionView.style.display = 'none';
    loginView.style.display = 'block';
    loginForm.dataset.role = role;
  }

  function showRoleSelectionView() {
    roleSelectionView.style.display = 'block';
    loginView.style.display = 'none';
    loggedInView.style.display = 'none';
    loginForm.reset();
  }
});
