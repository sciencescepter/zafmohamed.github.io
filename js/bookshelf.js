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
    const card = el('article', book.favourite ? 'card book-card is-favourite fade-up' : 'card book-card fade-up');
    if (book.favourite) {
        const badge = el('span', 'book-badge', 'Favourite');
        badge.prepend(el('span', 'book-badge-star', '★'));
        card.append(badge);
    }
    card.append(el('h3', 'card-title', book.title), el('p', 'book-author', book.author));
    if (book.note) card.append(el('p', 'card-text', book.note));
    return card;
}

if (BOOKS.length === 0) {
    emptyState.hidden = false;
} else {
    const extra = BOOKS.map((book) => book.category).filter((c) => !CATEGORIES.includes(c));
    const categories = [...new Set([...CATEGORIES, ...extra])];

    categories.forEach((category) => {
        const books = BOOKS.filter((book) => book.category === category)
            .sort((a, b) => Number(Boolean(b.favourite)) - Number(Boolean(a.favourite)));
        if (books.length === 0) return;

        const grid = el('div', 'grid');
        books.forEach((book) => grid.append(renderBookCard(book)));

        const heading = el('h2', 'subsection-title fade-up', category);
        heading.append(el('span', 'book-count', String(books.length)));
        bookList.append(heading, grid);
    });
}
