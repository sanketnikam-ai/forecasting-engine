let currentFilename = null;
let currentColumns = [];

// Upload area functionality
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

async function handleFileUpload(file) {
    if (!file.name.endsWith('.csv')) {
        alert('Please upload a CSV file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    showLoading();

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        hideLoading();

        if (response.ok) {
            currentFilename = data.filename;
            currentColumns = data.columns;
            displayFileInfo(data);
            showConfigSection();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        hideLoading();
        alert('Upload failed: ' + error.message);
    }
}

function displayFileInfo(data) {
    const fileInfo = document.getElementById('file-info');
    fileInfo.style.display = 'block';
    fileInfo.innerHTML = `
        <h3>📄 File Uploaded Successfully</h3>
        <p><strong>Filename:</strong> ${data.filename.split('_').slice(1).join('_')}</p>
        <p><strong>Rows:</strong> ${data.rows.toLocaleString()}</p>
        <p><strong>Columns:</strong> ${data.columns.join(', ')}</p>
    `;
}

function showConfigSection() {
    document.getElementById('config-section').style.display = 'block';
    
    // Populate column selects
    const dateCol = document.getElementById('date-col');
    const valueCol = document.getElementById('value-col');
    
    dateCol.innerHTML = '';
    valueCol.innerHTML = '';
    
    currentColumns.forEach(col => {
        dateCol.innerHTML += `<option value="${col}">${col}</option>`;
        valueCol.innerHTML += `<option value="${col}">${col}</option>`;
    });
    
    // Auto-select likely columns
    const dateLikeColumns = currentColumns.filter(col => 
        col.toLowerCase().includes('date') || col.toLowerCase().includes('time')
    );
    if (dateLikeColumns.length > 0) {
        dateCol.value = dateLikeColumns[0];
    }
    
    const valueLikeColumns = currentColumns.filter(col => 
        col.toLowerCase().includes('value') || 
        col.toLowerCase().includes('sales') ||
        col.toLowerCase().includes('price') ||
        col.toLowerCase().includes('amount')
    );
    if (valueLikeColumns.length > 0) {
        valueCol.value = valueLikeColumns[0];
    } else if (currentColumns.length > 1) {
        valueCol.value = currentColumns[1];
    }
}

// Run forecast
document.getElementById('run-forecast').addEventListener('click', async () => {
    const dateCol = document.getElementById('date-col').value;
    const valueCol = document.getElementById('value-col').value;
    const freq = document.getElementById('freq').value;
    const testSize = document.getElementById('test-size').value / 100;
    
    // Get selected methods
    const methodCheckboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked');
    const methods = Array.from(methodCheckboxes).map(cb => cb.value);
    
    if (methods.length === 0) {
        alert('Please select at least one forecasting method');
        return;
    }
    
    const requestData = {
        filename: currentFilename,
        date_col: dateCol,
        value_col: valueCol,
        freq: freq,
        test_size: testSize,
        methods: methods
    };
    
    showLoading();
    
    try {
        const response = await fetch('/api/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert('Forecast failed: ' + data.error);
        }
    } catch (error) {
        hideLoading();
        alert('Request failed: ' + error.message);
    }
});

function displayResults(data) {
    document.getElementById('results-section').style.display = 'block';
    
    // Display summary stats
    document.getElementById('best-model').textContent = data.best_model;
    document.getElementById('best-mape').textContent = data.best_metrics.MAPE.toFixed(2) + '%';
    document.getElementById('train-size').textContent = data.train_size.toLocaleString();
    document.getElementById('test-size-display').textContent = data.test_size.toLocaleString();
    
    // Display plot
    const plotImg = document.getElementById('forecast-plot');
    plotImg.src = data.plot;
    plotImg.style.display = 'block';
    
    // Display metrics table
    const tableBody = document.querySelector('#metrics-table tbody');
    tableBody.innerHTML = '';
    
    const metrics = data.metrics;
    const sortedMethods = Object.keys(metrics).sort((a, b) => 
        metrics[a].MAPE - metrics[b].MAPE
    );
    
    sortedMethods.forEach(method => {
        const row = document.createElement('tr');
        if (method === data.best_model) {
            row.classList.add('best-model');
        }
        row.innerHTML = `
            <td>${method} ${method === data.best_model ? '🏆' : ''}</td>
            <td>${metrics[method].MAE.toFixed(3)}</td>
            <td>${metrics[method].RMSE.toFixed(3)}</td>
            <td>${metrics[method].MAPE.toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
    
    // Setup download button
    document.getElementById('download-results').onclick = () => {
        window.location.href = `/api/download/${data.results_file}`;
    };
    
    // Scroll to results
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}
