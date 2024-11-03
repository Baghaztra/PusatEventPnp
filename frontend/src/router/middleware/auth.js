export function auth(to, from, next) {
  const isAuthenticated = !!localStorage.getItem("token"); // Cek apakah token ada di localStorage

  // Jika tujuan adalah halaman login dan sudah terautentikasi
  if (to.name === "LoginPage" && isAuthenticated) {
    next({ name: "HomePage" }); // Redirect ke halaman home
  }
  // Jika tujuan adalah halaman admin dan belum terautentikasi
  else if (
    (to.name === "AdminDashboard" || to.name === "AdminAccounts" || to.name === "EventsAccounts") &&
    !isAuthenticated
  ) {
    next({ name: "LoginPage" }); // Redirect ke halaman login
  } else {
    next(); // Lanjutkan ke route yang diminta
  }
}
