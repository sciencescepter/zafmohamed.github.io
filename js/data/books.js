// Book recommendations shown on books.html.
//
// To add a book, copy a line into the BOOKS list and edit it:
//
//   { title: 'Book Title', author: 'Author Name', category: 'Psychology' },
//
// Optional extras:
//   favourite: true                                  adds a "Favourite" badge
//   note: 'A sentence on why you recommend it.'      shown under the author
//
// Favourites are listed first within each category.

// Categories appear on the page in this order. Empty ones are hidden, and a
// category used in BOOKS but missing here is added at the end.
const CATEGORIES = [
    'Psychology',
    'Philosophy',
    'Probability & Decision-Making',
    'Business & Investing',
    'Biographies & Memoirs',
    'Fiction',
    'Fantasy',
    'Science Fiction',
    'Comics & Manga',
    'Poetry',
];

const BOOKS = [
    // Psychology
    { title: 'Thinking, Fast and Slow', author: 'Daniel Kahneman', category: 'Psychology' },
    { title: 'Predictably Irrational', author: 'Dan Ariely', category: 'Psychology' },
    { title: 'Influence', author: 'Robert Cialdini', category: 'Psychology' },
    { title: 'How to Win Friends and Influence People', author: 'Dale Carnegie', category: 'Psychology' },

    // Philosophy
    { title: 'Freedom from the Known', author: 'J. Krishnamurti', category: 'Philosophy' },
    { title: 'Meditations on First Philosophy', author: 'René Descartes', category: 'Philosophy' },

    // Probability & Decision-Making
    { title: 'Incerto', author: 'Nassim Nicholas Taleb', category: 'Probability & Decision-Making' },
    { title: 'Every Shot Counts', author: 'Mark Broadie', category: 'Probability & Decision-Making' },

    // Business & Investing
    { title: 'Zero to One', author: 'Peter Thiel', category: 'Business & Investing' },
    { title: "Poor Charlie's Almanack", author: 'Charlie Munger', category: 'Business & Investing' },

    // Biographies & Memoirs
    { title: 'When Breath Becomes Air', author: 'Paul Kalanithi', category: 'Biographies & Memoirs', favourite: true },
    { title: 'The Book of Elon', author: 'Eric Jorgenson', category: 'Biographies & Memoirs' },
    { title: 'Tuesdays with Morrie', author: 'Mitch Albom', category: 'Biographies & Memoirs' },

    // Fantasy
    { title: 'The Name of the Wind', author: 'Patrick Rothfuss', category: 'Fantasy', favourite: true },
    { title: 'The Priory of the Orange Tree', author: 'Samantha Shannon', category: 'Fantasy' },

    // Comics & Manga
    { title: 'One Piece', author: 'Eiichiro Oda', category: 'Comics & Manga', favourite: true },
    { title: 'The Sandman', author: 'Neil Gaiman', category: 'Comics & Manga' },

    // Poetry
    { title: 'Inferno', author: 'Dante Alighieri', category: 'Poetry' },
];
