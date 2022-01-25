$(() => {
    const animeNameInput = $("#animeNameInput");
    const addAnimeButton = $("#addAnimeBtn");
    const submitListButton = $("#submitListBtn");
    const addedAnimeList = $("#addedAnimeList");
    let animeList = [];

    addAnimeButton.click(() => {
        const input = animeNameInput.val();
        const animeItem = $("<li></li>");
        
        animeItem.text(input);
        animeList.push(input);

        addedAnimeList.append(animeItem);
        animeNameInput.val('');
    });

    submitListButton.click(() => {
        $.post("/create-list", {'animeList[]': animeList});
    });
});
