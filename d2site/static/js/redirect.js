document.addEventListener('DOMContentLoaded', (event) => {
    const searchForm = document.getElementById('searchForm');
    searchForm.onsubmit = function(e) {
        e.preventDefault();
        const accountId = document.getElementById('accountId').value;
        window.location.href = `/player/${accountId}/`;
    };
});
