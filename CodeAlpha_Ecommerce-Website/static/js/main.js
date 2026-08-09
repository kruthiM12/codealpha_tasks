/* ==========================================================================
   IndianKart Vanilla JavaScript - Interactive Enhancements
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
  
  // 1. Auto dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    const closeBtn = alert.querySelector('.close-alert');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
      });
    }
    setTimeout(function () {
      if (alert && alert.parentNode) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
      }
    }, 5000);
  });

  // 2. Quantity selector controls (+ and - buttons)
  document.querySelectorAll('.qty-controls').forEach(function (control) {
    const decBtn = control.querySelector('.qty-btn.minus');
    const incBtn = control.querySelector('.qty-btn.plus');
    const input = control.querySelector('.qty-input');

    if (decBtn && incBtn && input) {
      decBtn.addEventListener('click', function () {
        let val = parseInt(input.value) || 1;
        if (val > 1) {
          input.value = val - 1;
          input.dispatchEvent(new Event('change'));
        }
      });

      incBtn.addEventListener('click', function () {
        let val = parseInt(input.value) || 1;
        let max = parseInt(input.getAttribute('max')) || 99;
        if (val < max) {
          input.value = val + 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    }
  });

  // 3. Quick AJAX Add to Cart (Enhances UX without page refresh)
  document.querySelectorAll('.btn-add-to-cart-ajax').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.getAttribute('data-product-id');
      const url = `/cart/add/${productId}/`;
      const originalText = this.innerHTML;
      this.innerHTML = 'Adding...';
      this.disabled = true;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Update cart badge
          const badge = document.querySelector('.cart-count');
          if (badge) {
            badge.textContent = data.cart_count;
          }
          this.innerHTML = '✓ Added';
          this.style.backgroundColor = '#2E7D32';
          setTimeout(() => {
            this.innerHTML = originalText;
            this.style.backgroundColor = '';
            this.disabled = false;
          }, 1500);
        }
      })
      .catch(err => {
        console.error('Error adding to cart:', err);
        this.innerHTML = originalText;
        this.disabled = false;
      });
    });
  });

});

// Helper function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
