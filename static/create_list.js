$(() => {
    const animeNameInput = $("#animeNameInput");
    const addAnimeButton = $("#addAnimeBtn");
    const addedAnimeList = $("#addedAnimeList");

    addAnimeButton.click(() => {
        const input = animeNameInput.val();
        const animeItem = $("<li></li>");
        animeItem.text(input);

        addedAnimeList.append(animeItem);
        animeNameInput.val('');
    });
});
