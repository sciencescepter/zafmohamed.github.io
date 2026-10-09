// Renders BOOKS (from js/data/books.js) into the bookshelf page, grouped by
// category. Load before js/main.js so the new cards get the scroll reveal.

const bookList = document.getElementById('book-list');
const emptyState = document.getElementById('book-empty');

function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
}

function renderBookCard(book) {
    const card = el('article', 'card fade-up');
    card.append(
        el('h3', 'card-title', book.title),
        el('p', 'book-author', book.author),
        el('p', 'card-text', book.note)
    );
    return card;
}

if (BOOKS.length === 0) {
    emptyState.hidden = false;
} else {
    const categories = [...new Set(BOOKS.map((book) => book.category))];

    categories.forEach((category) => {
        const grid = el('div', 'grid');
        BOOKS.filter((book) => book.category === category)
            .forEach((book) => grid.append(renderBookCard(book)));

        bookList.append(el('h2', 'subsection-title fade-up', category), grid);
    });
}
