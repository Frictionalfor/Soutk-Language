document.getElementById('runBtn').addEventListener('click', function() {
    const code = document.getElementById('code').value;
    const outputDiv = document.getElementById('output');
    // Simulate Soutk output (for demo purposes)
    if (!code.trim()) {
        outputDiv.textContent = 'Please enter Soutk code to run.';
        return;
    }
    // Demo: Just echo the code for now
    outputDiv.textContent = 'Output (simulated):\n' + code;
    // For real Soutk execution, connect to a backend API
});
