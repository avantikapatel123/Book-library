// 🔥 Auto load books on page load
document.addEventListener('DOMContentLoaded', function() {
    loadBooks();
});

async function loadBooks() {
    const loading = document.getElementById('loading');
    const booksContainer = document.getElementById('books');
    
    // Show loading
    loading.style.display = 'flex';
    booksContainer.innerHTML = '';
    
    try {
        const res = await fetch('/books');
        const books = await res.json();
        
        // Hide loading
        loading.style.display = 'none';
        
        // Create cards
        books.forEach(book => {
            const card = createBookCard(book);
            booksContainer.appendChild(card);
        });
        
    } catch (error) {
        loading.innerHTML = '❌ Error loading books. <br> <button onclick="loadBooks()" class="btn">Try Again</button>';
    }
}

function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'card';
    
    card.innerHTML = `
        <img src="${book.cover}" alt="${book.title}" 
             onerror="this.src='https://via.placeholder.com/280x400/ff6b6b/ffffff?text=No+Image'">
        <div class="overlay">
            <h3>${book.title}</h3>
            <p><strong>👤 ${book.author}</strong></p>
            <p>${book.description}</p>
            <div class="btn-group">
                ${book.preview ? 
                    `<a href="${book.preview}" target="_blank" class="btn btn-secondary">👁️ Preview</a>` : 
                    '<button class="btn btn-secondary" disabled>No Preview</button>'
                }
                <button class="btn btn-primary" onclick="loadBooks()">🔄 New Book</button>
            </div>
        </div>
    `;
    
    return card;
}