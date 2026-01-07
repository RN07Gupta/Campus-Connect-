document.getElementById('registerForm')?.addEventListener('submit', function(e){
  e.preventDefault();
  alert('Registration successful! (frontend only)');
});

document.getElementById('loginForm')?.addEventListener('submit', function(e){
  e.preventDefault();
  const role = document.getElementById('role').value;
  if(role === 'admin'){
    window.location.href = 'admin_dashboard.html';
  } else {
    window.location.href = 'student_dashboard.html';
  }
});
