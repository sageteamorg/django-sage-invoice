document.addEventListener('DOMContentLoaded', () => {
    // Cached elements for better performance
    const receiptCheckbox = document.getElementById('id_receipt');
    const logoField = document.querySelector('.field-logo');
    const signatureField = document.querySelector('.field-signature');
    const stampField = document.querySelector('.field-stamp');
    const templateChoiceField = document.getElementById('id_template_choice');

    /**
     * Toggles visibility of signature and stamp fields based on receipt checkbox state.
     * Ensures the logo is always visible. Also fetches template choices dynamically based on receipt checkbox state.
     */
    const toggleDesignElements = () => {
        const isReceipt = receiptCheckbox.checked;

        // Ensure the logo is always visible
        logoField.style.display = ''; // Always show logo

        // Toggle visibility of fields based on receipt checkbox state
        signatureField.style.display = isReceipt ? 'none' : ''; // Hide signature for receipts
        stampField.style.display = isReceipt ? 'none' : ''; // Hide stamp for receipts

        // Fetch and update template choices dynamically
        fetchTemplateChoices(isReceipt);
    };

    /**
     * Fetches template choices from the server using AJAX and updates the template choice field.
     * @param {boolean} isReceipt - Whether the receipt checkbox is checked.
     */
    const fetchTemplateChoices = (isReceipt) => {
        const check = isReceipt ? 'True' : 'False'; // Ensure correct format
        const url = `/showcase/template-choices/${check}`; // Updated URL pattern

        console.log(`Fetching URL: ${url}`); // Debugging URL

        fetch(url)
            .then(response => {
                // Log the response status and URL for debugging
                console.log(`Response Status: ${response.status}`);
                console.log(`Content-Type: ${response.headers.get('content-type')}`);

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // Check if the response is JSON
                if (!response.headers.get('content-type')?.includes('application/json')) {
                    return response.text().then(text => {
                        console.error('Error: Expected JSON but received:', text);
                        throw new Error('Received non-JSON response');
                    });
                }

                return response.json();
            })
            .then(data => {
                console.log('Fetched Data:', data);

                // Ensure data is an array
                if (!Array.isArray(data)) {
                    throw new Error('Fetched data is not an array');
                }

                // Clear existing options in template choice field
                templateChoiceField.innerHTML = '';

                data.forEach(choice => {
                    if (choice.value && choice.label) {
                        const option = document.createElement('option');
                        option.value = choice.value;
                        option.textContent = choice.label;
                        templateChoiceField.appendChild(option);
                    } else {
                        console.error('Invalid choice format:', choice);
                    }
                });
            })
            .catch(error => console.error('Error fetching template choices:', error));
    };

    // Initialize visibility and options on page load
    toggleDesignElements();
    receiptCheckbox.addEventListener('change', toggleDesignElements);
});
