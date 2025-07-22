document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', async () => {
        const category = card.getAttribute('data-category');
        const tcText = document.getElementById('tc-input').value;
        const tone = document.getElementById('tone').value;
        const ageGroup = document.getElementById('age-group').value;
        const output = document.getElementById('summary-output');
        output.textContent = 'Summarizing...';
        try {
            const response = await fetch('http://localhost:8000/summarize/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tc_text: tcText,
                    category: category,
                    tone: tone,
                    age_group: ageGroup
                })
            });
            const data = await response.json();
            output.textContent = data.summary || 'No summary available.';
        } catch (err) {
            output.textContent = 'Error: ' + err.message;
        }
    });
}); 