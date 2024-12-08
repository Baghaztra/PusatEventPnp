import axios from "axios";

export async function eo(to, from, next) {
  const token = localStorage.getItem("token"); // Ambil token dari localStorage
  if (!token) {
    // Jika tidak ada token, arahkan ke HomePage
    return next({ name: "HomePage" });
  }

  try {
    // Panggil API untuk mendapatkan data profil
    const response = await axios.get(`${process.env.VUE_APP_BACKEND}/profile`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const userRole = response.data.role;

    // Periksa apakah userRole adalah admin
    if (userRole === "event organizer") {
      next(); // Lanjutkan ke halaman AdminDashboard
    } else {
      next({ name: "HomePage" }); // Jika bukan admin, kembalikan ke HomePage
    }
  } catch (error) {
    // Jika terjadi error (misalnya token tidak valid), arahkan ke HomePage
    console.error(error);
    next({ name: "HomePage" });
  }
}
