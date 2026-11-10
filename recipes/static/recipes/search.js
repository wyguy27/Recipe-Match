const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('results-container');

async function fetchSearchResults(query) {
    if (!query) {
        resultsContainer.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(
            `/api/recipe-search/?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error('Failed to fetch recipes');
        }

        const data = await response.json();

        displayResults(data);

    } catch (error) {
        console.error("Error fetching search data:", error);
        resultsContainer.innerHTML = '<p class="error">Something went wrong.</p>';
    }
}

searchInput.addEventListener('input', () => {
    fetchSearchResults(searchInput.value);
});