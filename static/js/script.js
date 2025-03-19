document.addEventListener('DOMContentLoaded', function() {
    // URL parametrelerini oku
    const urlParams = new URLSearchParams(window.location.search);
    const textParam = urlParams.get('text');
    
    // Eğer URL'de metin parametresi varsa, textarea'ya ekle
    if (textParam) {
        const newsTextarea = document.getElementById('news-text');
        newsTextarea.value = decodeURIComponent(textParam);
    }
    const newsForm = document.getElementById('news-form');
    const resultsContainer = document.getElementById('results-container');
    const mainCategory = document.getElementById('main-category');
    const mainConfidence = document.getElementById('main-confidence');
    const allCategoriesContainer = document.getElementById('all-categories');
    
    // Kategori renklerini tanımlama
    const categoryColors = {
        'siyaset': '#dc3545',
        'dunya': '#6c757d',
        'ekonomi': '#28a745',
        'kultur': '#fd7e14',
        'saglik': '#20c997',
        'spor': '#0dcaf0',
        'teknoloji': '#6610f2'
    };
    
    newsForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const newsText = document.getElementById('news-text').value.trim();
        if (!newsText) {
            alert('Lütfen bir haber metni girin!');
            return;
        }
        
        try {
            // Form gönderiminden sonra butonu devre dışı bırak ve yükleniyor göster
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> İşleniyor...';
            
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: newsText }),
            });
            
            const result = await response.json();
            
            // Butonu eski haline getir
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
            
            if (result.error) {
                alert('Hata: ' + result.error);
                return;
            }
            
            // Ana kategoriyi göster
            mainCategory.textContent = result.category;
            mainConfidence.textContent = (result.confidence * 100).toFixed(1);
            
            // Tüm kategorileri göster
            allCategoriesContainer.innerHTML = '';
            
            // Kategorileri olasılık değerine göre sırala
            const sortedCategories = Object.entries(result.all_probabilities)
                .sort((a, b) => b[1] - a[1]);
            
            // Her kategori için kart oluştur
            sortedCategories.forEach(([category, probability]) => {
                const confidencePercent = (probability * 100).toFixed(1);
                const card = document.createElement('div');
                card.className = 'col-md-4 mb-3';
                
                // Ana kategori için farklı stil
                const isMainCategory = category === result.category;
                const cardClass = isMainCategory ? 'bg-primary text-white' : '';
                
                card.innerHTML = `
                    <div class="card result-card ${cardClass} category-${category.toLowerCase()}">
                        <div class="card-body">
                            <h5 class="card-title">${category}</h5>
                            <p class="card-text">${confidencePercent}%</p>
                            <div class="progress confidence-bar">
                                <div class="progress-bar" role="progressbar" 
                                    style="width: ${confidencePercent}%; background-color: ${categoryColors[category.toLowerCase()] || '#007bff'}"></div>
                            </div>
                        </div>
                    </div>
                `;
                
                allCategoriesContainer.appendChild(card);
            });
            
            // Sonuçları göster
            resultsContainer.style.display = 'block';
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            console.error('Error:', error);
            alert('İstek sırasında bir hata oluştu!');
        }
    });
});