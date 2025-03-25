const updatePizzaOrder = (orderId) => {
    const form = document.getElementById("pizzaForm");
    const formData = new FormData(form);
    fetch(`/pizza/${orderId}`, {
        method: 'PUT',
        body: new URLSearchParams(formData)
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Order updated successfully!');
              window.location.href = '/';
          } else {
              alert('Failed to update order: ' + data.message);
          }
      });
};


const deletePizzaOrder = (orderId) => {
    if (confirm('Are you sure you want to delete this order?')) {
        fetch(`/pizza/${orderId}`, {
            method: 'DELETE'
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Order deleted successfully!');
                  window.location.href = '/';
              } else {
                  alert('Failed to delete order: ' + data.message);
              }
          });
    }
};
