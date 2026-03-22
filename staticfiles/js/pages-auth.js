/**
 * ==========================================================================
 *  PAGES AUTHENTICATION — Validasi Form Halaman Auth
 * ==========================================================================
 *  Script ini menangani validasi form pada halaman autentikasi:
 *  - Login (field: email-username, password)
 *  - Register (field: username, email, password, terms)
 *  - Forgot Password (field: email)
 *  - Reset Password (field: password, confirm-password)
 *
 *  CATATAN: Script ini TIDAK menggunakan library FormValidation.
 *  Menggunakan validasi JavaScript murni (vanilla JS) untuk
 *  kompatibilitas maksimal di semua device (desktop & mobile).
 * ==========================================================================
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {
  // ===== REFERENSI ELEMEN =====
  var formAuthentication = document.getElementById('formAuthentication');

  // Jika form #formAuthentication tidak ada di halaman → skip
  if (!formAuthentication) {
    return;
  }

  // ===== DEFINISI VALIDASI PER FIELD =====
  // Setiap field punya: selector, rules (array fungsi validasi)
  // Hanya field yang ADA di form yang akan divalidasi
  var validationRules = {
    // Field login: email-username
    'email-username': {
      rules: [
        { check: function (v) { return v.trim().length > 0; }, message: 'Silakan masukkan email atau username' },
        { check: function (v) { return v.trim().length >= 3; }, message: 'Minimal 3 karakter' }
      ]
    },
    // Field register: username
    'username': {
      rules: [
        { check: function (v) { return v.trim().length > 0; }, message: 'Silakan masukkan username' },
        { check: function (v) { return v.trim().length >= 4; }, message: 'Username minimal 4 karakter' }
      ]
    },
    // Field register & forgot password: email
    'email': {
      rules: [
        { check: function (v) { return v.trim().length > 0; }, message: 'Silakan masukkan email Anda' },
        {
          check: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); },
          message: 'Silakan masukkan alamat email yang valid'
        }
      ]
    },
    // Field login, register, reset password: password
    'password': {
      rules: [
        { check: function (v) { return v.length > 0; }, message: 'Silakan masukkan kata sandi' },
        { check: function (v) { return v.length >= 4; }, message: 'Kata sandi minimal 4 karakter' }
      ]
    },
    // Field reset password: confirm-password
    'confirm-password': {
      rules: [
        { check: function (v) { return v.length > 0; }, message: 'Silakan konfirmasi kata sandi' },
        { check: function (v) { return v.length >= 4; }, message: 'Kata sandi minimal 4 karakter' },
        {
          check: function (v) {
            var pw = formAuthentication.querySelector('[name="password"]');
            return pw && v === pw.value;
          },
          message: 'Kata sandi dan konfirmasi tidak sama'
        }
      ]
    },
    // Field register: terms (checkbox)
    'terms': {
      isCheckbox: true,
      rules: [
        {
          check: function (v, el) { return el.checked; },
          message: 'Anda harus menyetujui syarat & ketentuan'
        }
      ]
    }
  };

  // ===== FUNGSI HELPER =====

  /**
   * Cari wrapper element (parent terdekat yang merupakan container field).
   * Digunakan untuk menempatkan pesan error di tempat yang tepat.
   */
  function findFieldWrapper(inputEl) {
    // Cari .mb-4, .mb-3, atau .mb-5 terdekat
    var wrapper = inputEl.closest('.mb-4') || inputEl.closest('.mb-3') || inputEl.closest('.mb-5');
    if (wrapper) return wrapper;
    // Fallback: parent element
    return inputEl.parentElement;
  }

  /**
   * Tampilkan pesan error di bawah field.
   * Menambahkan class Bootstrap 5 untuk styling.
   */
  function showError(inputEl, message) {
    var wrapper = findFieldWrapper(inputEl);
    // Hapus error sebelumnya (jika ada)
    clearError(inputEl);

    // Tambahkan class invalid pada input
    inputEl.classList.add('is-invalid');
    inputEl.classList.remove('is-valid');

    // Buat elemen pesan error
    var errorDiv = document.createElement('div');
    errorDiv.className = 'fv-plugins-message-container invalid-feedback';
    errorDiv.setAttribute('data-field', inputEl.name);
    errorDiv.style.display = 'block';
    errorDiv.innerHTML = '<div class="fv-help-block"><span>' + message + '</span></div>';

    // Tempatkan pesan error setelah wrapper
    wrapper.appendChild(errorDiv);
  }

  /**
   * Hapus pesan error dari field.
   */
  function clearError(inputEl) {
    inputEl.classList.remove('is-invalid');

    var wrapper = findFieldWrapper(inputEl);
    if (wrapper) {
      // Hapus semua pesan error sebelumnya
      var existingErrors = wrapper.querySelectorAll('[data-field="' + inputEl.name + '"]');
      existingErrors.forEach(function (el) {
        el.remove();
      });
    }
  }

  /**
   * Validasi satu field berdasarkan rules yang didefinisikan.
   * Mengembalikan true jika valid, false jika ada error.
   */
  function validateField(fieldName, rules) {
    var inputEl = formAuthentication.querySelector('[name="' + fieldName + '"]');
    if (!inputEl) return true; // Field tidak ada → skip, dianggap valid

    var value = inputEl.value || '';

    for (var i = 0; i < rules.length; i++) {
      if (!rules[i].check(value, inputEl)) {
        showError(inputEl, rules[i].message);
        return false;
      }
    }

    // Field valid → hapus error dan tandai valid
    clearError(inputEl);
    inputEl.classList.add('is-valid');
    return true;
  }

  /**
   * Validasi semua field yang ada di form.
   * Mengembalikan true jika SEMUA valid, false jika ada error.
   */
  function validateForm() {
    var isValid = true;

    // Iterasi semua rule
    for (var fieldName in validationRules) {
      if (!validationRules.hasOwnProperty(fieldName)) continue;

      // Cek apakah field ada di form
      var inputEl = formAuthentication.querySelector('[name="' + fieldName + '"]');
      if (!inputEl) continue; // Field tidak ada → skip

      var config = validationRules[fieldName];
      var fieldValid = validateField(fieldName, config.rules);

      if (!fieldValid) {
        isValid = false;
      }
    }

    return isValid;
  }

  /**
   * Tampilkan loading state pada tombol submit.
   */
  function showLoadingState() {
    var btnSubmit = document.getElementById('btnSubmit');
    var btnText = document.getElementById('btnText');
    var btnLoader = document.getElementById('btnLoader');

    if (btnSubmit) btnSubmit.disabled = true;
    if (btnText) btnText.textContent = 'Memproses...';
    if (btnLoader) btnLoader.classList.remove('visually-hidden');
  }

  // ===== SETUP EVENT LISTENERS =====

  // --- Real-time validation: validasi saat user meninggalkan field (blur) ---
  for (var fieldName in validationRules) {
    if (!validationRules.hasOwnProperty(fieldName)) continue;

    var inputEl = formAuthentication.querySelector('[name="' + fieldName + '"]');
    if (!inputEl) continue;

    // Closure untuk menangkap fieldName dan config
    (function (name, config) {
      var el = formAuthentication.querySelector('[name="' + name + '"]');
      if (el) {
        // Validasi saat blur (user pindah dari field)
        el.addEventListener('blur', function () {
          validateField(name, config.rules);
        });

        // Untuk checkbox, validasi saat change
        if (config.isCheckbox) {
          el.addEventListener('change', function () {
            validateField(name, config.rules);
          });
        }

        // Hapus error saat user mulai mengetik (input event)
        el.addEventListener('input', function () {
          clearError(el);
        });
      }
    })(fieldName, validationRules[fieldName]);
  }

  // --- Form submit handler ---
  formAuthentication.addEventListener('submit', function (e) {
    // Cegah submit default dulu, validasi dulu
    e.preventDefault();

    // Jalankan validasi semua field
    var isValid = validateForm();

    if (isValid) {
      // Form valid → tampilkan loading state dan submit
      showLoadingState();
      // Submit form secara native (memanggil form.submit() yang
      // TIDAK trigger event listener 'submit' lagi)
      formAuthentication.submit();
    } else {
      // Form tidak valid → fokuskan field pertama yang error
      var firstError = formAuthentication.querySelector('.is-invalid');
      if (firstError) {
        firstError.focus();
        // Scroll ke field error (penting untuk mobile)
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  });

  // ===== NUMERAL MASKING =====
  // Untuk input angka (jika ada di halaman)
  var numeralMask = document.querySelectorAll('.numeral-mask');
  if (numeralMask.length) {
    numeralMask.forEach(function (maskEl) {
      new Cleave(maskEl, { numeral: true });
    });
  }
});
