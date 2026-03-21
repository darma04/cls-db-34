/**
 * ==========================================================================
 *  AUTH CLICK LOADER — Loading State untuk Tombol di Halaman Auth
 * ==========================================================================
 *  Digunakan di halaman verify_email yang TIDAK menggunakan form submit,
 *  melainkan link (<a>) untuk mengirim verifikasi email.
 *
 *  Saat tombol diklik → tampilkan spinner loading dan ubah text.
 * ==========================================================================
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {
  // Ambil referensi elemen tombol
  var btnSubmit = document.getElementById('btnSubmit');
  var btnText = document.getElementById('btnText');
  var btnLoader = document.getElementById('btnLoader');

  if (btnSubmit && btnText && btnLoader) {
    // Saat tombol diklik → tampilkan loading state
    btnSubmit.addEventListener('click', function () {
      btnSubmit.classList.add('disabled');
      btnText.textContent = 'Mengirim email...';
      btnLoader.classList.remove('visually-hidden');
    });
  }
});
