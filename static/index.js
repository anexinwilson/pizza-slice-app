// Function to update a pizza order
const updatePizzaOrder = (orderId) => {
    const form = document.getElementById("pizzaForm");  // Get the form element by pizzaForm forms ID
    const formData = new FormData(form);  // Collect all form data as key-value pairs
    fetch(`/pizza/${orderId}`, {  // Send PUT request to /pizza/<orderId>
        method: 'PUT',  // HTTP method used to update data
        body: new URLSearchParams(formData)  // Convert form data to URL-encoded format because flask needs this format to work
    }).then(response => response.json())  // Convert server response to JSON
      .then(data => {
          if (data.success) {  // Check if update was successful
              alert('Order updated successfully!');  // Show success message
              window.location.href = '/';  // Redirect to homepage
          } else {
              alert('Failed to update order: ' + data.message);  // Show error message if update failed
          }
      });
};

// Function to delete a pizza order
const deletePizzaOrder = (orderId) => {
    if (confirm('Are you sure you want to delete this order?')) {  // Ask user for confirmation
        fetch(`/pizza/${orderId}`, {  // Send DELETE request to /pizza/<orderId>
            method: 'DELETE'  // HTTP method used to delete data
        }).then(response => response.json())  // Convert server response to JSON
          .then(data => {
              if (data.success) {  // Check if delete was successful
                  alert('Order deleted successfully!');  // Show success message
                  window.location.href = '/';  // Redirect to homepage
              } else {
                  alert('Failed to delete order: ' + data.message);  // Show error message if delete failed
              }
          });
    }
};
